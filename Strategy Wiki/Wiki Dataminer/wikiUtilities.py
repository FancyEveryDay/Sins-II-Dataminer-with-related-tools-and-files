from pathlib import Path
import json

## This file holds common functions and variables used accross many of the scripts.
## This is to avoid having many varients of the same code in multiple files.

TOP_DIR = Path(__file__).parent.parent.parent.resolve()

with open('.env', 'r', encoding='utf-8') as env:
    SINS_DIRECTORY = Path(json.load(env)['sins2File'])

with open(SINS_DIRECTORY / 'uniforms' / 'planet.uniforms', 'r', encoding='utf-8') as file:
    PLANET_UNIFORMS = json.load(file)

with open(SINS_DIRECTORY / 'localized_text' / 'en.localized_text', 'r', encoding='utf-8') as file:
    LOCALIZED_TEXT = json.load(file)

ENTITIES = SINS_DIRECTORY / 'entities'
UNIFORMS = SINS_DIRECTORY / 'uniforms'

WIKIFILES_DIR = TOP_DIR / 'Strategy Wiki' / 'WikiFiles'

SOURCES = {"DLC" : "Paths to Power", "DLC2" : "Reinforcements"}

with open(UNIFORMS / "gui.uniforms", 'r', encoding='utf-8') as file:
    UNIT_MODIFIERS = json.load(file)

_modifier_lookup = {}
for _, group in UNIT_MODIFIERS['modifier'].items():
    _modifier_lookup = _modifier_lookup | group

_other_keys = {}
for key, value in _modifier_lookup.items():
    if isinstance(value, dict):
        for subkey, subvalue in value.items():
            _other_keys[subkey] = LOCALIZED_TEXT.get(subvalue, subvalue)
    else:
        _modifier_lookup[key] = LOCALIZED_TEXT.get(value, value)

MODIFIER_LOOKUP = _modifier_lookup | _other_keys

with open(SINS_DIRECTORY / 'gui' / 'modifier_tooltip.gui', 'r', encoding='utf-8') as file:
    MODIFIER_TOOLTIPS = json.load(file)

def getRace(entityName):
    NPC_RACE_NAME_LOOKUP = {
        "alutar" : "alutar_sect",
        "aluxian" : "aluxian_resurgence",
        "eivonns" : "eivonns_frigates",
        "jiskun" : "jiskun_force",
        "nilari" : "nilari_cult",
        "pranast" : "pranast_united",
        "viturak" : "viturak_cabal"
    }

    if "dlc" in entityName:
        raceID = NPC_RACE_NAME_LOOKUP.get(entityName.split("_")[1], entityName.split("_")[1])

    else:
        raceID = NPC_RACE_NAME_LOOKUP.get(entityName.split("_")[0], entityName.split("_")[0])

    race = LOCALIZED_TEXT.get(f"player_race_name.{raceID}", 
                            LOCALIZED_TEXT.get(f"npc_player.{raceID}.play",
                            raceID.replace("_", " ").title()))

    return race

def unpackPrice(price : dict):
    price = (price.get('credits', 0), price.get('metal', 0), price.get('crystal', 0))
    
    return price

def formatExoticPrice(outputDict : dict, exoticDict : dict):
    lookup = {item["exotic_type"] : item["count"] for item in exoticDict}
    for exotic in ['economic', 'offense', 'defense', 'utility', 'ultimate']:
        ingameText = LOCALIZED_TEXT.get(f"exotic.{exotic}.name", exotic).lower()
        outputDict[ingameText] = lookup.get(exotic, None)
    
class ModifierEnum:
    EMPIRE_MODIFIER = "empire_modifier_names"
    PLANET_MODIFIER = "planet_modifier_names"
    UNIT_MODIFIER = "unit_modifier_names"
    WEAPON_MODIFIER = "weapon_modifier_names"
    UNIT_FACTORY_MODIFIER = "unit_factory_modifier_names"
    EXOTIC_FACTORY_MODIFIER = "exotic_factory_modifier_names"
    STRIKECRAFT_MODIFIER = "strikecraft_modifier_names"
    NPC_MODIFIER = "npc_modifier_names"

def formatModifier(modifier, modifierType : ModifierEnum):
    if modifier is None:
        return None
    
    modifiers = []
    
    for m in modifier:
        match modifierType:
            case ModifierEnum.EMPIRE_MODIFIER:
                formated_modifier = LOCALIZED_TEXT[UNIT_MODIFIERS["modifier"][modifierType][m["modifier_type"]]]
            case ModifierEnum.PLANET_MODIFIER:
                formated_modifier = LOCALIZED_TEXT[UNIT_MODIFIERS["modifier"][modifierType][m["modifier_type"]]]
            case ModifierEnum.UNIT_MODIFIER:
                formated_modifier = LOCALIZED_TEXT[UNIT_MODIFIERS["modifier"][modifierType][m["modifier_type"]]]
            case ModifierEnum.WEAPON_MODIFIER:
                formated_modifier = LOCALIZED_TEXT[UNIT_MODIFIERS["modifier"][modifierType]['normal'][m["modifier_type"]]]
            case ModifierEnum.UNIT_FACTORY_MODIFIER:
                formated_modifier = LOCALIZED_TEXT[UNIT_MODIFIERS["modifier"][modifierType][m["modifier_type"]]]
            case ModifierEnum.EXOTIC_FACTORY_MODIFIER:
                formated_modifier = LOCALIZED_TEXT[UNIT_MODIFIERS["modifier"][modifierType][m["modifier_type"]]]
            case ModifierEnum.STRIKECRAFT_MODIFIER:
                formated_modifier = LOCALIZED_TEXT[UNIT_MODIFIERS["modifier"][modifierType][m["modifier_type"]]]
            case ModifierEnum.NPC_MODIFIER:
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