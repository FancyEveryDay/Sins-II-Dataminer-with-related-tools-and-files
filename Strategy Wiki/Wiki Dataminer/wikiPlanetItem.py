from wikiUtilities import *
from pprint import pprint

def getPlanetItemData():
    itemGlob = ENTITIES.glob('*.unit_item')
    itemDict = {}

    for i in itemGlob:
        with open(i, 'r', encoding='utf-8') as file:
            item = json.load(file)

        if item.get("item_type") == "planet_component":

            name = i.name
            itemDict[name] = item
    
    return itemDict

def formatPlanetItemEntries(planetDict : dict, outputFile = WIKIFILES_DIR / "Wikiplanetitem"):

    outputDict = {}

    for name, item in planetDict.items():

        itemName = LOCALIZED_TEXT.get(item['name'], name.replace('.unit_item', ''))
        itemDescription = LOCALIZED_TEXT.get(item['description'], "")
        itemRace = getRace(name)

        if item.get('is_artifact', False):
            itemRace = "Artifact"

        outputName = f"{itemRace} {itemName}".strip()
        itemFaction = None # At some point I'll do a pass to grab all item factions

        print(f"Processing {outputName}...") # Print the name of the item being processed

        # Cost block
        itemBuildTime = item.get('build_time', None)
        
        itemPrice = item.get('price', None)
        if itemPrice != None:
            itemCreditCost = itemPrice.get('credits', None)
            itemMetalCost = itemPrice.get('metal', None)
            itemCrystalCost = itemPrice.get('crystal', None)

        else:
            itemCreditCost = None
            itemMetalCost = None
            itemCrystalCost = None

        itemExoticCost = item.get('exotic_price', [])

        planetTypeGroups = item.get('planet_type_groups')[0]

        planetTypes = planetTypeGroups.get('planet_types', None)

        itemPlanetTypes = []
        if planetTypes != None:
            for planet in planetTypes:
                itemPlanetTypes.append(LOCALIZED_TEXT.get(planet + "_planet_name", planet).capitalize())

        if item.get('player_modifiers', False):
            itemPlanetEffect = item['player_modifiers'].get('planet_modifiers', None)
            itemEmpireEffect = item['player_modifiers'].get('empire_modifiers', None)
        else: 
            itemPlanetEffect = itemEmpireEffect = None

        if item.get('planet_modifiers', False):
            itemPlanetEffect = item.get('planet_modifiers', None)

        ability = item.get('ability', None)
        if ability != None:
            with open(ENTITIES  / (ability + '.ability'), 'r', encoding='utf-8') as file:
                abilityJson = json.load(file)
            itemAbility = LOCALIZED_TEXT.get(abilityJson.get('name', None), itemName)
        else: itemAbility = None

        prerequisites = planetTypeGroups.get('build_prerequisites', None)

        if prerequisites != None:

            itemPrerequisites = (LOCALIZED_TEXT.get(prerequisites[0][0] + "_research_subject_name", prerequisites[0][0]))

        else: itemPrerequisites = None

        if item.get('item_level_source'):
            levelPrerequisites = []
            for research in item["item_level_prerequisites"]:
                levelPrerequisites.append(
                    LOCALIZED_TEXT[f"{research[0][0]}_research_subject_name"]
                )
        else:
            levelPrerequisites = None

        planetLevelRequirement = item.get("required_planet_level", None)

        # Produce final output

        output = outputDict[outputName] = {}

        output['name'] = itemName
        output['race'] = itemRace
        output['description'] = itemDescription
        output['faction'] = itemFaction 
        output['build_time'] = itemBuildTime
        output['credits'] = itemCreditCost
        output['metal'] = itemMetalCost
        output['crystal'] = itemCrystalCost
        formatExoticPrice(output, itemExoticCost)

        output['planettypes'] = itemPlanetTypes
        output['required_planet_level'] = planetLevelRequirement
        output['empireeffects'] = formatModifier(itemEmpireEffect, ModifierEnum().EMPIRE_MODIFIER)
        output['planeteffects'] = formatModifier(itemPlanetEffect, ModifierEnum().PLANET_MODIFIER)
        output['ability'] = itemAbility
        output['prerequisites'] = itemPrerequisites
        output['level_prerequisites'] = levelPrerequisites

    sorted_outputDict = dict(sorted(outputDict.items(), key = lambda item: item[0]))

    with open(outputFile, 'w', encoding = "utf-8") as file:
        json.dump(sorted_outputDict, file, indent = 1, ensure_ascii=False)


def main():

    planetDict = getPlanetItemData()

    formatPlanetItemEntries(planetDict, outputFile= WIKIFILES_DIR / "Wikiplanetitem.json")

if __name__ == "__main__":
    main()