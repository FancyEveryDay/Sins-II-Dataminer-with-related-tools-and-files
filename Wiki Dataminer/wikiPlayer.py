import glob, json, pprint

with open('.env', 'r') as env:
    SINS_DIRECTORY = json.load(env)['sins2File']

ENTITIES = SINS_DIRECTORY + r'\entities'

with open(SINS_DIRECTORY + r'\localized_text\en.localized_text', 'r') as file:
    LOCALIZED_TEXT = json.load(file)

def getUniqueLists(subject : str, wiki_player : dict, playerDict : dict, itemDict : dict):
    global LOCALIZED_TEXT

    for faction, itemList in playerDict.items():
        race = itemList['race']
        uniquePlanetItemList = itemList['unique_' + subject] = []
        print(faction)

        for item in itemList.get( subject ):
            item_is_copy = False

            for f, i in playerDict.items():
                if (f == faction) or (itemList.get('name').find("dlc_") < 0 and i.get('name').find("dlc_") > -1):
                    continue

                for j in i.get( subject ):
                    if item == j:
                        item_is_copy = True
                        break

                if item_is_copy == True:
                    try: 
                        string = f'{race} {LOCALIZED_TEXT[itemDict[item]]}'
                    except:
                        
                        print(f"Oopsie with {item} string on finding item is copy")

                    if string not in wiki_player[race][ subject ]:
                        wiki_player[race][ subject ].append(string)

                    break

            if item_is_copy == False:

                try: 
                    string = f'{race} {LOCALIZED_TEXT[itemDict[item]]}'
                    uniquePlanetItemList.append(string)
                    # print("\t" + string)
                except: 
                    string = item
                    uniquePlanetItemList.append(string)
                    #print("\t" + string)

    for faction, itemList in playerDict.items():
        itemList.pop('planet_components')
        itemList.get('unique_planet_items').sort()

    for race, itemList in wiki_player.items():
        itemList.get('planet_components').sort()

def itemDict(fileType):

    global ENTITIES

    subjectGlob = glob.glob(f'{ENTITIES}\\**{fileType}')

    itemDict = {}

    for i in subjectGlob:
        with open(i, 'r') as file:
            subject = json.load(file)

        name = i.split("\\")[-1].replace(fileType, "")
        itemDict[name] = subject.get('name')

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

        playerDict[raceFaction] = {'research' : faction["research"]["research_subjects"],
                                'planet_components' : faction["planet_components"],
                            'name' : name,
                            'race' : race}

    for faction, factionDict in playerDict.items():
        if wiki_player.get(factionDict.get('race')) == None:
            wiki_player[factionDict.get('race')] = {'research_subjects' : [], 
                                                    'planet_components' : []}
            # print(factionDict.get('race'))

        wiki_player[factionDict.get('race')][faction] = factionDict
        # print('\t' + faction)

    nameDict = {'research_subjects' : '.reasearch_subject',
                'planet_components' : '.unit_item'
                }


    for key, itemGroup in nameDict.items():
        key : str
        itemGroup : str
        
        getUniqueLists(subject= key, wiki_player= wiki_player, playerDict= playerDict, itemDict= itemDict(itemGroup))

    # with open("WikiFiles\\Wikiplayer.json", "w") as file:
    #     json.dump(wiki_player, file, indent = 1)


if __name__ == "__main__":
    main()