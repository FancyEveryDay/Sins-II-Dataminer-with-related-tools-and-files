import glob, json, pprint

with open('.env', 'r') as env:
    SINS_DIRECTORY = json.load(env)['sins2File']

ENTITIES = SINS_DIRECTORY + r'\entities'

with open(SINS_DIRECTORY + r'\localized_text\en.localized_text', 'r') as file:
    LOCALIZED_TEXT = json.load(file)

def getUniqueLists(subject : str, wiki_player : dict, playerDict : dict, itemDict : dict):
    """Checks for general and unique subject items and creates generic lists at the race level, and unique lists at the faction level.
    
    playerDict is a dict of factions while wiki_player is the dict of races."""

    global LOCALIZED_TEXT

    for faction, itemList in playerDict.items():
        race = itemList['race']
        raceIsDLC = itemList.get('name').find("dlc_") > 0
        uniquePlanetItemList = itemList['unique_' + subject] = []
        print(f"Finding unique {subject} for {faction}")
        unique_count = 0
        general_count = 0
    
        for item in itemList.get( subject, []):
            item_is_copy = False

            for f, i in playerDict.items():
                race2IsDLC = (itemList.get('name').find("dlc_") < 0 and i.get('name').find("dlc_") > -1)
                if race != i.get('race') or (f == faction) or (race2IsDLC):
                    continue

                for j in i.get( subject, [] ):
                    if item == j:
                        item_is_copy = True
                        break
                        
                # If the item is a copy, add it to the general subject dict of the race.
                if item_is_copy == True and not raceIsDLC:
                    general_count += 1
                    try: 
                        string = f'{race} {LOCALIZED_TEXT[itemDict[item]]}'
                    except:
                        string = item
                        print(f"Oopsie with {item} namestring on finding item is copy")

                    if string not in wiki_player[race][ subject ]:
                        wiki_player[race][ subject ].append(string)

                    break
            
            # If item is not a copy, add it to the unique_subject dict of the faction.
            if item_is_copy == False:
                unique_count += 1
                try: 
                    string = f'{race} {LOCALIZED_TEXT[itemDict[item]]}'
                    uniquePlanetItemList.append(string)
                    # print("\t" + string)
                except: 
                    string = item
                    uniquePlanetItemList.append(string)
                    #print("\t" + string)

        # Print counts for the funsies
        print(f"\tFound {unique_count} unique items")
        print(f"\tFound {general_count} general items")

    # Pop general subjects from factions, throws an exception if the unique_subject is not in faction dict. 
    for faction, itemList in playerDict.items():
        itemList.pop(subject)
        itemList.get('unique_' + subject).sort()

    # Checks for general subjects in Race dict. Throws an exception otherwise.
    for race, itemList in wiki_player.items():
        itemList.get( subject ).sort()

def itemDict(fileType):

    global ENTITIES

    subjectGlob = glob.glob(f'{ENTITIES}\\**{fileType}')

    itemDict = {}

    for i in subjectGlob:
        with open(i, 'r') as file:
            subject = json.load(file)

        name = i.split("\\")[-1].replace(fileType, "")
        itemDict[name] = subject.get('name', name + "_name")

    return itemDict

def main():

    wiki_player = {}
    playerDict = {}

    playerGlob = glob.glob(f'{ENTITIES}\\**.player')

    for fileName in playerGlob:
        fileName : str
        with open(fileName, 'r') as file:
            faction = json.load(file)

        try:
            race = LOCALIZED_TEXT.get("player_race." + faction['race'] ,faction['race'].capitalize())
            name = "player_faction_name." + fileName.split("\\")[-1].split('.')[0]
            raceFaction = LOCALIZED_TEXT[name]

        except KeyError:
            continue

        playerDict[raceFaction] = {'research_subjects' : faction["research"]["research_subjects"],
                                'planet_components' : faction["planet_components"],
                                'ship_components' : faction["ship_components"],
                                'buildable_units' : faction["buildable_units"],
                                'structures' : faction["structures"],
                            'name' : name,
                            'race' : race
                            }

    for faction, factionDict in playerDict.items():
        if wiki_player.get(factionDict.get('race')) == None:
            wiki_player[factionDict.get('race')] = {'research_subjects' : [],
                                                    'planet_components' : [],
                                                    'ship_components' : [],
                                                    'buildable_units' : [],
                                                    'structures' : [],
                                                    }
            # print(factionDict.get('race'))

        wiki_player[factionDict.get('race')][faction] = factionDict
        # print('\t' + faction)

    nameDict = {'research_subjects' : '.research_subject',
                'planet_components' : '.unit_item',
                'ship_components' : '.unit_item',
                'buildable_units' : '.unit',
                'structures' : '.unit',
                }


    for key, itemGroup in nameDict.items():
        key : str
        itemGroup : str
        
        getUniqueLists(subject= key, wiki_player= wiki_player, playerDict= playerDict, itemDict= itemDict(itemGroup))

    with open("WikiFiles\\Wikiplayer.json", "w") as file:
        json.dump(wiki_player, file, indent = 1)


if __name__ == "__main__":
    main()
