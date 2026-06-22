from wikiUtilities import *
from pprint import pprint

# with open(UNIFORMS / "gui.uniforms", 'r') as file:
#     UNIT_MODIFIERS = json.load(file)

# _modifier_lookup = {}
# for _, group in UNIT_MODIFIERS['modifier'].items():
#     _modifier_lookup = _modifier_lookup | group

# _other_keys = {}
# for key, value in _modifier_lookup.items():
#     if type(value) == dict:
#         for subkey, subvalue in value.items():
#             _other_keys[subkey] = LOCALIZED_TEXT.get(subvalue, subvalue)
#     else:
#         _modifier_lookup[key] = LOCALIZED_TEXT.get(value, value)

# MODIFIER_LOOKUP = _modifier_lookup | _other_keys

# with open(SINS_DIRECTORY / 'gui' / 'modifier_tooltip.gui', 'r', encoding='utf-8') as file:
#     MODIFIER_TOOLTIPS = json.load(file)

def getShipItemData():
    itemGlob = ENTITIES.glob('*.unit_item')
    itemDict = {}

    for i in itemGlob:
        with open(i, 'r', encoding='utf-8') as file:
            item = json.load(file)

        if item.get("item_type") == "ship_component":

            name = i.name
            itemDict[name] = item

    return itemDict

def formatShipItemEntries(shipItemDict : dict, outputFile = WIKIFILES_DIR / "Wikishipitem"):

    outputDict = {}

    print(f"Processing {len(shipItemDict)} ship items...") # Print the number of items being processed

    for itemCall, item in shipItemDict.items():

        print(f"Found {itemCall}...")

        itemRace = getRace(itemCall)
        if item.get('is_artifact', False):
            itemRace = "Artifact"

        itemName = LOCALIZED_TEXT.get(item.get('name', None), itemCall)
        outputName = itemRace + ' ' + itemName
           
        outputDict[outputName] = item

        item['name'] = itemName
        item['id'] = itemCall
        item['race'] = itemRace
        item['description'] = LOCALIZED_TEXT.get(item.get('description', None), None)

        item['credits'], item['metal'], item['crystal'] = unpackPrice(item.pop('price', {}))
        formatExoticPrice(item, item.get('exotic_price', []))

        if item.get('ability'):
            unitAbility = item['ability']
            with open(SINS_DIRECTORY / "entities" / (unitAbility + ".ability"), "r", encoding="utf-8") as file:
                ability_file = json.load(file)
            item['ability'] = LOCALIZED_TEXT.get(f"{unitAbility}_ability_name", unitAbility.replace('_', ' ').title()) # LOCALIZED_TEXT.get(nameCall)
        else: item['ability'] = None

        if item.get('build_prerequisites'):
            prereqList = []
            for prereq in item['build_prerequisites']:
                prereqList.append(LOCALIZED_TEXT.get(prereq[0] + "_research_subject_name", prereq[0].replace('_', ' ').title()))
            item['build_prerequisites'] = prereqList

        if item.get('item_level_prerequisites'):
            for i, levels in enumerate(item['item_level_prerequisites']):
                prereqList = []
                for prereq in levels:
                    prereqList.append(LOCALIZED_TEXT.get(prereq[0] + "_research_subject_name", prereq[0].replace('_', ' ').title()))
                item['item_level_prerequisites'][i] = prereqList

        if item.get('weapon_modifiers', False):
            item['weapon_modifiers'] = formatModifier(item['weapon_modifiers'], ModifierEnum.WEAPON_MODIFIER)
        else:
            item['weapon_modifiers'] = None

        if item.get('unit_modifiers', False):
            item['unit_modifiers'] = formatModifier(item['unit_modifiers'], ModifierEnum.UNIT_MODIFIER)
        else:
            item['unit_modifiers'] = None

        sorted_outputDict = dict(sorted(outputDict.items(), key = lambda item: item[0]))

    with open(WIKIFILES_DIR / 'Wikishipitem.json', 'w', encoding='utf-8') as file:
        json.dump(sorted_outputDict, file, indent=1, ensure_ascii=False)

def main():
    shipItemDict = getShipItemData()
    formatShipItemEntries(shipItemDict)

if __name__ == "__main__":
    main()