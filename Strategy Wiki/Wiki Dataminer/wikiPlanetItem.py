from wikiUtilities import *
from pprint import pprint

with open(UNIFORMS / "gui.uniforms", 'r') as file:
    UNIT_MODIFIERS = json.load(file)

modifier_lookup = {}
for _, group in UNIT_MODIFIERS['modifier'].items():
    modifier_lookup = modifier_lookup | group

other_keys = {}
for key, value in modifier_lookup.items():
    if type(value) == dict:
        for subkey, subvalue in value.items():
            other_keys[subkey] = LOCALIZED_TEXT.get(subvalue, subvalue)
    else:
        modifier_lookup[key] = LOCALIZED_TEXT.get(value, value)

MODIFIER_LOOKUP = modifier_lookup | other_keys

with open(SINS_DIRECTORY / 'gui' / 'modifier_tooltip.gui', 'r') as file:
    MODIFIER_TOOLTIPS = json.load(file)

def getPlanetItemData():
    itemGlob = ENTITIES.glob('*.unit_item')
    itemDict = {}

    for i in itemGlob:
        with open(i, 'r') as file:
            item = json.load(file)

        if item.get("item_type") == "planet_component":

            name = i.name
            itemDict[name] = item
    
    return itemDict

def formatExoticPrice(outputDict : dict, exoticDict : dict):
    lookup = {item["exotic_type"] : item["count"] for item in exoticDict}
    for exotic in ['economic', 'offense', 'defense', 'utility', 'ultimate']:
        ingameText = LOCALIZED_TEXT.get(f"exotic.{exotic}.name", exotic).lower()
        outputDict[ingameText] = lookup.get(exotic, None)

def getRace(unitName):
    if "dlc" in unitName:
        race = LOCALIZED_TEXT.get(f"player_race_name.{unitName.split("_")[1]}", 
                                    LOCALIZED_TEXT.get(f"npc_race_name.{unitName.split("_")[1]}",
                                                        ""))
    else:
        race = LOCALIZED_TEXT.get(f"player_race_name.{unitName.split("_")[0]}", 
                                    LOCALIZED_TEXT.get(f"npc_player_name.{unitName.split("_")[0]}",
                                                        ""))

    return race

# def formatModifier(modifier_value, modifier_format):
#     match modifier_format:
#         case "no_decimal_place_with_sign":
#             return f"{modifier_value:.0f}"
#         case "percentage_with_sign":
#             return f"{modifier_value:.0f}%"
#         case _:
#             return str(modifier_value)

class ModifierEnum:
    EMPIRE_MODIFIER = "empire_modifier_names"
    PLANET_MODIFIER = "planet_modifier_names"

def formatModifier(modifier, modifierType : ModifierEnum):
    if modifier is None:
        return None
    
    modifiers = []
    
    for m in modifier:
        formated_modifier = LOCALIZED_TEXT[UNIT_MODIFIERS["modifier"][modifierType][m["modifier_type"]]]
        
        values = ""

        if m["value_behavior"] == "additive" and m.get("values",False):
            for i in m['values']:
                values += f"{"+" if i > 0 else ""}{i} → "

            values = values[:-3]

        elif m["value_behavior"] == "additive" and m.get("value",False):
            values = f"{'+' if m['value'] > 0 else ''}{m['value']}"

        elif m["value_behavior"] == "scalar"and m.get("values",False):
            for i in m['values']:
                values += f"{"+" if i > 0 else ""}{i*100}% → "

            values = values[:-3]

        elif m["value_behavior"] == "scalar"and m.get("value",False):
            values = f"{'+' if m['value'] > 0 else ''}{m['value']*100}%"

        modifiers.append(f"{formated_modifier} {values}")


    return modifiers

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
            with open(ENTITIES  / (ability + '.ability'), 'r') as file:
                abilityJson = json.load(file)
            itemAbility = LOCALIZED_TEXT.get(abilityJson.get('name', None), itemName)
        else: itemAbility = None

        prerequisites = planetTypeGroups.get('build_prerequisites', None)

        if prerequisites != None:
            try:
                itemPrerequisites = (LOCALIZED_TEXT[prerequisites[0][0] + "_research_subject_name"])
            except:
                itemPrerequisites = (prerequisites[0][0])
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

    with open(outputFile, 'w', encoding = "utf-8") as file:
        json.dump(outputDict, file, indent = 1, ensure_ascii=False)


def main():

    planetDict = getPlanetItemData()

    formatPlanetItemEntries(planetDict, outputFile= WIKIFILES_DIR / "Wikiplanetitem.json")

if __name__ == "__main__":
    main()