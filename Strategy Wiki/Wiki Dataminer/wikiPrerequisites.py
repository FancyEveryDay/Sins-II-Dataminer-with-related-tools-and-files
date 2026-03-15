import json, pprint, glob
from pathlib import Path
from wikiUtilities import LOCALIZED_TEXT, ENTITIES, WIKIFILES_DICT



def main(completeItemSet : set = set()):
    if len(completeItemSet) > 0:
        useSet = True
    else:
        useSet = False

    subjectGlob = list(ENTITIES.glob('*.research_subject'))
    entitiesGlob = list(ENTITIES.glob('*'))

    # Get all research subject names (research subjects have inconsistent naming conventions)
    subjectNameSearch = {}
    for i in subjectGlob:
        with open(i, 'r') as file:
            subject = json.load(file)

        # Get Basic Info
        nameCall = subject.pop('name')

        name = LOCALIZED_TEXT.get(nameCall)
        id = i.name.split('.')[0]

        subjectNameSearch[id] = name


    # Begin Prerequisite search
    prereqsDict = {}

    for i in entitiesGlob:
        entityType = i.name.split('.')[-1]

        if entityType not in prereqsDict.keys():
            prereqsDict[entityType] = {}

    for i in entitiesGlob:
        with open(i, 'r') as file:
            entity = json.load(file)

        entityType = i.name.split('.')[-1]
        entityString = i.name.split('.')[0]

        buildable_item_types = set(["unit",
                                   "unit_item",
                                   "research_subject"]
                                   )

        if useSet and (entityType in buildable_item_types) and (entityString not in completeItemSet):
            continue

        if "dlc" not in i.name:
            race = i.name.split("_")[0]
        else:
            race = i.name.split("_")[1]

        # Create item name
        name = LOCALIZED_TEXT.get('player_race_name.' + race, race)
        try:
            if entityType == 'unit':
                name += f" {LOCALIZED_TEXT[entityString + '_name']}"
            elif entityType == 'ability':
                name += f" {LOCALIZED_TEXT[entityString + '_ability_name']}"
            else:
                name += f" {LOCALIZED_TEXT[entity.get('name')]}"
        except:
            name = entityString

        # Get Prereq
        prerequisiteKeys = {
                            "build_prerequisites",
                            "prerequisites",
                            "level_prerequisites",
                            }
        
        prerequisites = (entity.get(k, '') for k in prerequisiteKeys)

        # prerequisites = entity.get('build_prerequisites', '')
        # if prerequisites == '':
        #     prerequisites = entity.get("prerequisites", '')

        for j in prerequisites:
                if j != '':
                    temp = j
                    break
                else:
                    temp = ''
        prerequisites = temp

        if prerequisites == '':
            try:
                prerequisites = entity["build"]['prerequisites']
            except:
                pass

        if prerequisites == '':
            try:
                prerequisites = entity["planet_type_groups"][0]['build_prerequisites']
            except:
                pass

        if prerequisites != '':
            prereqsDict[entityType][name] = []

            for _, j in enumerate(prerequisites):
                tempList = []
                if len(j) > 0 and type(j[0]) == list:
                    for k in j[0]:
                        
                        # Prereq name
                        prerequisiteName = LOCALIZED_TEXT.get('player_race_name.' + race, race)
                        prerequisiteName += f" {subjectNameSearch.get(k, k)}"

                        tempList.append( prerequisiteName )
                else:
                    prerequisiteName = LOCALIZED_TEXT.get('player_race_name.' + race, race)
                    try:
                        prerequisiteName += f" {subjectNameSearch.get(j[0])}"
                    except:
                        prerequisiteName = j

                    if len(prerequisiteName) > 1:
                        tempList.append( prerequisiteName )


                prereqsDict[entityType][name].append( tempList )

    with open(WIKIFILES_DICT / "Wikiprerequsites.json", 'w') as file:
        json.dump(prereqsDict, file, indent=1)

    return(prereqsDict)


if __name__ == "__main__":
    main()