import json, pprint, glob
from pathlib import Path
from wikiUtilities import LOCALIZED_TEXT, UNIFORMS, ENTITIES, WIKIFILES_DICT

with open(UNIFORMS / 'gui.uniforms', 'r') as file:
    GUI_UNIFORMS = json.load(file)

def getTierNumerals(tier):
        tier = str(tier)

        tierDict = {'0' : 'I',
                    '1' : 'II',
                    '2' : 'III',
                    '3' : 'IV',
                    '4' : 'V'
                    }
        return tierDict[tier]

def unpackPrice(price : dict):
    price = (price.get('credits', 0), price.get('metal', 0), price.get('crystal', 0))
    
    # 'price': {'credits': 850.0,
    #             'crystal': 650.0,
    #             'metal': 275.0},
    return price

def getModifierName(modifierID, modifierType):
    # modifierClasses = ["unit_modifiers",
    #                 "weapon_modifiers",
    #                 "planet_modifiers",
    #                 "empire_modifiers",
    #                 "npc_modifiers",
    #                 "unit_factory_modifiers",
    #                 "exotic_factory_modifiers"]

    # if modifierType == "unit_factory_modifiers":
    #     return LOCALIZED_TEXT.get(f"unit_factory_modifier.{modifierID}", modifierID)
    
    if modifierType == "exotic_factory_modifiers":
        return LOCALIZED_TEXT.get(f"exotic_factory_modifier.{modifierID}", modifierID)
    
    # if modifierType == "npc_modifiers":
    #     return LOCALIZED_TEXT.get(f"npc_modifier.{modifierID}", modifierID)
    
    if modifierType == "planet_modifiers":
        return LOCALIZED_TEXT.get(GUI_UNIFORMS["modifier"]["planet_modifier_names"].get(modifierID), modifierID)
    
    return LOCALIZED_TEXT.get( f"unit_modifier.{modifierID}",
                        LOCALIZED_TEXT.get(f"empire_modifier.{modifierID}",
                        LOCALIZED_TEXT.get(f"weapon_modifier.{modifierID}",
                        LOCALIZED_TEXT.get(f"planet_modifier.{modifierID}",
                        LOCALIZED_TEXT.get(f"npc_modifier.{modifierID}",
                        LOCALIZED_TEXT.get(f"unit_factory_modifier.{modifierID}",
                        LOCALIZED_TEXT.get(f"exotic_factory_modifier.{modifierID}",
                        modifierID )))))))
     
    

def formatNumberValue(number):
    if str(number)[-1] == "0":
        number = int(number)
    return abs(number)

def getTags(modifier):

    tagTypeList = ['tags',
                   'planet_types',
                   ]

    for tagType in tagTypeList:
        tags = modifier.get(tagType, '')

        if tags != '':
            break

    if tags != '':
        temp = ""
        for i, tag in enumerate(tags):
            if i < len(tags) - 1: 
                temp = temp.replace(" Planet", "") + f"{LOCALIZED_TEXT.get(f"{tag}_planet_name" , LOCALIZED_TEXT.get(f"weapon_tag_name.{tag}" , tag.replace("_", " ").capitalize()))}, "
            elif i == len(tags) - 1 and i == 0:
                temp = f"{LOCALIZED_TEXT.get(f"{tag}_planet_name" , LOCALIZED_TEXT.get(f"weapon_tag_name.{tag}" , tag.replace("_", " ").capitalize()))}"
            elif i == len(tags) - 1 and i == 1:
                temp = temp[:-2].replace(" Planet", "") + f" and {LOCALIZED_TEXT.get(f"{tag}_planet_name" , LOCALIZED_TEXT.get(f"weapon_tag_name.{tag}" , tag.replace("_", " ").capitalize()))}"
            else:
                temp = temp.replace(" Planet", "") + f"and {LOCALIZED_TEXT.get(f"{tag}_planet_name" , LOCALIZED_TEXT.get(f"weapon_tag_name.{tag}" , tag.replace("_", " ").capitalize()))}"
        tags = temp
    else:
        tags = False

    return tags

def createPrereqSearch(prereqsDict):
    prereqsDict2 = dict(prereqsDict)
    prereqSearch = {}

    for entity, entityDict in prereqsDict2.items():
        for key, item in entityDict.items():
            for i in item:
                if len(i) < 1:
                    continue
                elif i[0] not in prereqSearch.keys():
                    prereqSearch[i[0]] = []

                if len(item) > 1:
                    prereqSearch[i[0]].append( { entity + '_upgrade' : key } )
                else:
                    prereqSearch[i[0]].append( { entity : key } )

    return prereqSearch

def main(prereqsDict):
    subjectGlob = ENTITIES.glob('*.research_subject')

    prereqSearch = createPrereqSearch(prereqsDict)

    subjectDict = {}

    for i in subjectGlob:
        with open(i, 'r') as file:
            subject = json.load(file)

        # Get Basic Info
        nameCall = subject.pop('name')

        #print(f"Processing {nameCall} for Wiki Research file")

        name = LOCALIZED_TEXT.get(nameCall)
        subject['name'] = name

        subject['id'] = i.name.split('.')[0]

        subject['field'] = subject['field'].split('_')[1].capitalize()

        if name == None:
            print(f"{i} has no name")
            name = i.name.replace(".research_subject", "")

        if 'vasari' in i.name:
            race = 'Vasari'
        elif 'trader' in i.name:
            race = 'TEC'
        elif 'advent' in i.name:
            race = 'Advent'
        else:
            print(f"Error: {i.name} has no recognized race")
            continue

        if race:
            name = race + ' ' + name
            subject['race'] = race

        subject['domain'] = LOCALIZED_TEXT.get(f"{race.lower()}_research_domain_partial_name_{subject['domain']}", subject['domain'].capitalize())
        subject['tier'] = f"{subject['domain'].capitalize()} {getTierNumerals(subject['tier'])}" # We're going to change this back like immediately -_-


        try:
            subject['description'] = LOCALIZED_TEXT.get(subject['description'], None)
        except:
            pass

        # Unpack price for some reason

        subject['credits'], subject['metal'], subject['crystal'] = unpackPrice(subject.pop('price', {} ))

        if subject.get('exotic_price'):
            for j in subject.pop('exotic_price'):
                subject[ LOCALIZED_TEXT.get(f"exotic.{j['exotic_type']}.name").lower() ] = j['count']
        

        # Better process prereqs?
        if prereqsDict['research_subject'].get(name):
            subject['prerequisites'] = prereqsDict['research_subject'].get(name)

        # # Process Prereqs
        # try:
        #     prerequisites = subject['prerequisites']
        # except:
        #     prerequisites = ''

        # if prerequisites != '':
            
        #     subject['prerequisites'] = []

        #     for _, j in enumerate(prerequisites):
        #         tempList = []
        #         if len(j) > 0 and type(j) == list:
        #             for k in j:
        #                 # Prereq name
        #                 prerequisiteName = LOCALIZED_TEXT.get('player_race_name.' + race, race)
        #                 try:
        #                     prerequisiteName += f" {LOCALIZED_TEXT[k + '_research_subject_name']}"
        #                 except:
        #                     prerequisiteName = k

        #                 tempList.append(prerequisiteName)
        #             subject['prerequisites'].append(tempList)

        # Process Modifiers
        modifierClasses = ["unit_modifiers",
                        "weapon_modifiers",
                        "planet_modifiers",
                        "empire_modifiers",
                        "npc_modifiers",
                        "unit_factory_modifiers", ]
                        #"exotic_factory_modifiers"]


        for modType in modifierClasses:
            modifiers = subject.get(modType, False)

            if modifiers:
                for index, modifier in enumerate(modifiers):
                    modifierType = getModifierName(modifier.get('modifier_type'), modType)
                    behavior = modifier.get('value_behavior')
                    value = modifier.get('value')
                    weaponType = modifier.get('weapon_type', False)

                    tags = getTags(modifier)

                    modifiers[index] = f"{tags + ' ' if tags else '' }{f"{weaponType.replace("_", " ").title()} " if weaponType else ""}{modifierType} {"+" if value > 0 else "-"}{f"{formatNumberValue(value*100)}%" if behavior == 'scalar' else formatNumberValue(value)}"

        modifiers = subject.get("exotic_factory_modifiers", False)
        if modifiers:
            for index, modifier in enumerate(modifiers):
                modifierType = getModifierName(modifier.get('modifier_type'), "exotic_factory_modifiers")
                behavior = modifier.get('value_behavior')
                value = modifier.get('value')

                exoticType = modifier.get('exotic_types', '')
                if exoticType != '':
                    temp = ""
                    for etype in exoticType:
                        temp += f"{LOCALIZED_TEXT.get(f"exotic.{etype}.name")}, "
                    exoticType = temp[ : -2] 

                modifiers[index] = f"{"Increases" if value > 0 else "Decreases"} {exoticType} {modifierType} by {f"{formatNumberValue(value*100)}%" if behavior == 'scalar' else formatNumberValue(value)}"

        # Get Unlocks (requires a function in the prereq's section above this to run first)
        if prereqSearch.get( name , False ):
            subject["unlocks"] = prereqSearch.get( name )

        # Process Windfall resources:
        if subject.get('windfall'):
            windfall = subject['windfall']
            temp = []
            for resource, value in windfall.items():
                if type(value) in [int, float, str]:
                    temp.append(f"{LOCALIZED_TEXT.get(f"tooltip.windfall_{resource}_label", resource.capitalize().replace("_", " "))}: {formatNumberValue(value)}"  )
                
                elif resource == "exotics_given":
                    exoticsGivenString = f"{resource.capitalize().replace("_", " ")}: "
                    for index, exotic in enumerate(value):
                        if index == len(value) - 1 and index == 0:
                            exoticsGivenString += f"{exotic['count']} {LOCALIZED_TEXT.get( f"exotic.{exotic["exotic_type"]}.name" )}"
                        elif index < len(value) - 1:
                            exoticsGivenString += f"{exotic['count']} {LOCALIZED_TEXT.get( f"exotic.{exotic["exotic_type"]}.name" )}, "
                        elif index == len(value) - 1 and i == 1:
                            exoticsGivenString = exoticsGivenString[-2] + f" and {exotic['count']} {LOCALIZED_TEXT.get( f"exotic.{exotic["exotic_type"]}.name" )}"
                        else:
                            exoticsGivenString += f"and {exotic['count']} {LOCALIZED_TEXT.get( f"exotic.{exotic["exotic_type"]}.name" )}"

                    temp.append(exoticsGivenString)

                elif resource == "units_given":
                    unitsGivenString = f"{resource.capitalize().replace("_", " ")}: "
                    for index, unit in enumerate(value["required_units"]):
                        count1 = unit['count'][0]
                        count2 = unit['count'][1]

                        if count1 == count2:
                            count = count1
                        else:
                            count = f"{count1}-{count2}"

                        unitName = LOCALIZED_TEXT.get( f"{unit["unit"]}_name" )
                        if "Pirate" not in unitName:
                            unitName = f"{race} {unitName}"

                        unitName = f"[[Sins of a Solar Empire II/{unitName}|{unitName}]]"

                        if index == len(value["required_units"]) - 1 and index == 0:
                            unitsGivenString += f"{count} {unitName}{"s" if count2 > 1 else ""}"
                        elif index < len(value["required_units"]) - 1:
                            unitsGivenString += f"{count} {unitName}{"s" if count2 > 1 else ""}, "
                        elif index == len(value["required_units"]) - 1 and i == 1:
                            unitsGivenString = exoticsGivenString[-2] + f" and {count} {unitName}{"s" if count2 > 1 else ""}"
                        else:
                            unitsGivenString += f"and {count} {unitName}{"s" if count2 > 1 else ""}"
                    temp.append(unitsGivenString)
            
            subject['windfall'] = temp

        try:
            image = f"{race} {LOCALIZED_TEXT.get(f"{subject.get("tooltip_picture")[:-16]}_name", subject.get("tooltip_picture"))}"
            image = image.replace("_unlock", "").replace("_subject", "").replace("_research", "")
            subject['image'] = image
        except:
            pass
            
        # Pop shit we don't want
        subject.pop('name_uppercase', '')
        subject.pop('arbitary_research_line', '')
        subject.pop('version', '')
        subject.pop('extra_text_filter_strings', '')

        # # Check for godamn duplicates
        # if subjectDict.get(name):
        #     if "trader_rebel" nameCall

        # Finally, add processed subject to subject
        subjectDict[name] = subject

    with open(WIKIFILES_DICT / 'Wikiresearch.json', 'w') as file:
        json.dump(subjectDict, file, indent=1)

if __name__ == "__main__":
    import wikiPrerequisites
    prereqsDict = wikiPrerequisites.main()
    
    main(prereqsDict)