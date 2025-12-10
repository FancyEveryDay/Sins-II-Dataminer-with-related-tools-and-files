import glob, json

SPECIAL_DEV_TRACK_DICT = {"max_military_structure_slots" : "Military Orbit Slots",
                          "max_civilian_structure_slots" : "Civilian Orbit Slots",
                          "structure_builder_count" : "Constructors",
                          "max_health_points" : "Maximum Health",
                          "health_points_restore_rate" : "Health Regen Rate",
                          "credits_income_rate": "Base Credit Income",
                          "credits_income_rate_per_population" : "Credit Income per 100 Population",
                          "civilian_research_rate_scalar": "Civilian Research Rate",
                          "civilian_research_rate_per_population_scalar": "Civilian Research Rate per 100 Population",
                          "civilian_research_points_per_population": "Civilian Research Points per 100 Population",
                          "military_research_rate_scalar": "Military Research Rate",
                          "military_research_rate_per_population_scalar": "Military Research Rate per 100 Population",
                          "military_research_points_per_population": "Military Research Poins per 100 Population",
                            }   

def main():
    wiki_planet = {}

    with open('.env', 'r') as env:
        SINS_DIRECTORY = json.load(env)['sins2File']

    with open(SINS_DIRECTORY + r'\uniforms\planet.uniforms', 'r') as file:
        PLANET_UNIFORMS = json.load(file)

    with open(SINS_DIRECTORY + r'\localized_text\en.localized_text', 'r') as file:
        LOCALIZED_TEXT = json.load(file)

    # Get base dev track levels

    with open(SINS_DIRECTORY + r'\entities\advent_rebel.player', 'r') as file:
        examplePlayer = json.load(file)


    planetBaseDevLevels = {}
    for planet in (examplePlayer['planet_types']):
        #print(f"{planet["planet_type"]}")
        
        planetBaseDevLevels[planet["planet_type"]] = {"planet_item_capacity" : planet["tracks"]["logistics"][0].get("max_planet_component_slots")}
        
        for track, levels in planet["tracks"].items():
            count = -1
            for i in levels:
                # try:
                #     prereq = i["prerequisites"]
                # except : prereq = False
                # if prereq == False:
                count += 1

            planetBaseDevLevels[planet["planet_type"]][track] = count

    # Create PlayerDict

    playerFiles = glob.glob(SINS_DIRECTORY + r'\entities\**.player')

    playerDict = {}

    for address in playerFiles:
        with open(address, 'r') as file:
            playerDict[address] = json.load(file)

    # Get info from planet.unit file
    planet_unit_glob = glob.glob(SINS_DIRECTORY + r'\entities\**_planet.unit')

    planetUnit = {}

    for p in planet_unit_glob:
        try:

            # Get planet data from .json, prints an alert and continues if an entity contains no planet data
            with open(p, 'r') as file:
                planetJson = json.load(file)
            
            try:
                planet = planetJson['planet']
            except KeyError:
                print(f"{p.split("\\")[-1]} is not colonizable, contains no planet data.")
                continue
            
            name = LOCALIZED_TEXT.get(planetJson['planet']['planet_type'] + "_planet_name").capitalize()
            planetUnit[name] = {}

            # Get Asteroids
            asteroidDict = {"crystal" :  planet['non_random_crystal_asteroids']['tiers'][0]['count'][0],
                            "random crystal" :  planet['random_crystal_asteroids']['tiers'][0]['count'][0],
                            "metal" :  planet['non_random_metal_asteroids']['tiers'][0]['count'][0],
                            "random metal" :  planet['random_metal_asteroids']['tiers'][0]['count'][0]
                            }
            # Get SttC resources
            strippedResourcesDict = {}
            for asset, n in planet['destroyed_planet']['stripped_assets'].items():
                strippedResourcesDict[asset] = n

            for asset in planet['destroyed_planet']['stripped_exotics']:
                strippedResourcesDict[LOCALIZED_TEXT[f"exotic.{asset["exotic_type"]}.name"]] = asset["count"]

            planetUnit[name]['asteroids'] = asteroidDict
            planetUnit[name]['stripped_to_the_core_resources'] = strippedResourcesDict
        except KeyError as e:
            print(f"Exception when loading {p}\n\t Key Error: {e}")

    # Format planet entries and add them to dictionary
    for planet in PLANET_UNIFORMS['planet_types']:
        planet : dict

        print(f"Processing {planet['name']}")


        # Get name that matches wiki-formatting
        name = LOCALIZED_TEXT.get(planet['name'] + "_planet_name").capitalize()


        # Add development track summaries
        planet['base_dev_tracks'] = planetBaseDevLevels[planet['name']]


        # Simplify survey field
        for index, i in enumerate(planet['surveying_track_levels']):
            i['random_exotics'] = {}
            i['guaranteed_exotics'] = {}

            for j in i['exotics']['bonus_exotic_chances']:
                i['random_exotics'][LOCALIZED_TEXT[f"exotic.{j['exotic_type']}.name"]] = j['chance']
            
            for j in i['exotics']['guaranteed_counts']:
                i['guaranteed_exotics'][LOCALIZED_TEXT[f"exotic.{j['exotic_type']}.name"]] = j['count'][0]
            i.pop('exotics')


            # planet['surveying_track_levels'][index] = {'bonus_exotic_chances' : planet['surveying_track_levels'][index]['exotics']['bonus_exotic_chances'],
            #                                         'guaranteed_counts' : planet['surveying_track_levels'][index]['exotics']['guaranteed_counts']}

            planet['base_dev_tracks']['survey'] = index + 1


        # Add planet .unit file data
        planet['asteroids'] = planetUnit[name]['asteroids']
        planet['stripped_to_the_core_resources'] = planetUnit[name]['stripped_to_the_core_resources']


        # Add planet quality
        numSum = 0
        for _, num in planet['base_dev_tracks'].items():
            if _ == 'focus':
                if num > 0 and num//3 < 1:
                    numSum += 1
                else:
                    numSum += num//3
            else:
                numSum += num

        numSum += round(planet['population']['population_maximum']/100)

        if numSum < 20:
            quality = 'Poor'
        elif numSum < 26:
            quality = 'Fair'
        elif numSum < 31:
            quality = 'Rich'
        else:
            quality = 'Super Rich'        
        planet['quality'] = f"{quality} ({int(round(numSum, 0 ))} Quality Points)"


        # Add full dev tracks
        popList = []
        planet['tracks'] = {}
        for fileName, race in playerDict.items():

            raceName = LOCALIZED_TEXT["player_race_name." + race['race']]

            if not race.get('planet_types'):
                print(f'No planet data in {fileName}')
                popList.append(fileName)
            else:
                try:
                    for i in race['planet_types']:
                        i : dict
                        if i['planet_type'] == planet['name']:
                            planetTracks = dict(i)

                            # Remove unwanted values
                            planetTracks.pop('planet_type')
                            planetTracks.pop('maintenance_cost_rates')
                            planetTracks.pop('can_ever_be_colonized')
                            
                            # Reduce unnecessary data depth
                            for track, trackList in planetTracks['tracks'].items():
                                
                                # Rename values in each track level to match ingame
                                for level_i ,level in enumerate(trackList):
                                    newLevel = {}
                                    for resource, value in level.items():
                                        # Special-case credit incom bc idfk. If no special case looks for localized text.
                                        ingameText = SPECIAL_DEV_TRACK_DICT.get(resource, resource)
                                        ingameText = LOCALIZED_TEXT.get('tooltip.upgrade_planet_track.' + ingameText + '_label', ingameText)

                                        if "per 100" in ingameText.lower():
                                            value = round(value*100, 3)
                                        
                                        # Removing a specific unwanted value
                                        if ingameText == "Planet Item Slots":
                                            continue
                                        
                                        newLevel[ingameText] = value
                                    trackList[level_i] = dict(sorted(newLevel.items()))

                                planetTracks[track] = trackList

                            # Remove unwanted dict and unwanted values
                            planetTracks.pop('tracks')

                            planet['tracks'][raceName] = planetTracks
                except KeyError:
                    print(f'Failed to Parse <{name}> track data for <{fileName}>')
        

        # Cleanup - Removes non-conforming player files from the dict on first iteration.
        for pop in popList:
            playerDict.pop(pop)
        

        # Remove extra stuff
        planet.pop('tooltip_icon')


        # Add planet entry to dictionary
        wiki_planet[name] = planet


    # Create wiki_planet file from dictionary
    with open('WikiFiles\\Wikiplanet.json', 'w') as file:
        json.dump(wiki_planet, file, indent=1)

    print(f"WikiPlanet.json saved")

if __name__ == "__main__":
    main()