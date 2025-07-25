import json, pprint, glob

def main():


    with open('.env', 'r') as env:
        SINS_DIRECTORY = json.load(env)['sins2File']

    with open(SINS_DIRECTORY + r'\localized_text\en.localized_text', 'r') as file:
        LOCALIZED_TEXT = json.load(file)

    ENTITIES_DIRECTORY = SINS_DIRECTORY + "\\entities"

    subjectGlob = glob.glob(ENTITIES_DIRECTORY + r'\**.research_subject')
    entitiesGlob = glob.glob(ENTITIES_DIRECTORY + r'\**')

    prereqsDict = {}

    for i in entitiesGlob:
        entityType = i.split('.')[-1]

        if entityType not in prereqsDict.keys():
            prereqsDict[entityType] = {}

    for i in entitiesGlob:
        with open(i, 'r') as file:
            entity = json.load(file)

        entityType = i.split('.')[-1]
        entityString = i.split("\\")[-1].split('.')[0]


        if "dlc" not in i:
            race = i.split("\\")[-1].split("_")[0]
        else:
            race = i.split("\\")[-1].split("_")[1]

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

        if prerequisites != '':
            prereqsDict[entityType][name] = []

            for _, j in enumerate(prerequisites):
                tempList = []
                if len(j) > 0 and type(j[0]) == list:
                    for k in j[0]:
                        # Prereq name
                        prerequisiteName = LOCALIZED_TEXT.get('player_race_name.' + race, race)
                        try:
                            prerequisiteName += f" {LOCALIZED_TEXT[k + '_research_subject_name']}"
                        except:
                            prerequisiteName = k
                        tempList.append( prerequisiteName )
                else:
                    prerequisiteName = LOCALIZED_TEXT.get('player_race_name.' + race, race)
                    try:
                        prerequisiteName += f" {LOCALIZED_TEXT[j[0] + '_research_subject_name']}"
                    except:
                        prerequisiteName = j

                    if len(prerequisiteName) > 1:
                        tempList.append( prerequisiteName )


                prereqsDict[entityType][name].append( tempList )

    with open('WikiFiles\\Wikiprerequsites.json', 'w') as file:
        json.dump(prereqsDict, file, indent=1)


if __name__ == "__main__":
    main()