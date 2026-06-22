import glob, json
from pathlib import Path
from wikiUtilities import *

def getSinsData(race, type, output = False, file = SINS_DIRECTORY / "entities" ):
    file = Path(file) # just in case
    unitfilelist = file.rglob(f"{race}*{type}")

    listODatas = []

    for unitfile in unitfilelist:
            with open(unitfile) as unitJSON:
                d = json.load(unitJSON)

            listODatas.append([unitfile.name.split(".")[0], d])

    return listODatas

def createWeaponDict(WeaponList):
    WeaponsDict = {}

    for weapon in WeaponList:
        indexName = weapon[0]
        weaponStats = weapon[1]
        try:
            weaponStats["dps"] = weaponStats["damage"] / weaponStats["cooldown_duration"]
        except KeyError:
            try:
                weaponStats["dps"] = weaponStats["bombing_damage"] / weaponStats["cooldown_duration"]
            except KeyError:
                pass

        WeaponsDict[indexName] = weaponStats

    return WeaponsDict

def getUnitName(unitName):
    try: outputName = LOCALIZED_TEXT[unitName + "_name"]
    except KeyError: outputName = "_".join(unitName.split("_")[1:]).replace("_", " ").title()

    return outputName

def createWeaponBlock(weaponCollection, weaponDict, weaponPrereqs):

    if len(weaponCollection) == 0:
        return None

    unitWeapons = []

    for weapon, count in weaponCollection.items():

        weaponName : str = weaponDict[weapon]["name"].split(".")[-1]
        weaponName = weaponName.replace("_", " ")
        
        weaponPrereq = LOCALIZED_TEXT.get(f"{weaponPrereqs.get(weapon)}_unit_item_name", None)

        weapon = weaponDict[weapon]

        weaponName = LOCALIZED_TEXT.get(weapon["name"])

        unitWeapon = {}

        unitWeapon["name"] = weaponName
        unitWeapon["required_unit_item"] = weaponPrereq
        unitWeapon["weapon_type"] = weapon.get("weapon_type", None)
        unitWeapon["burst_count"] = len(weapon.get("burst_pattern")) if weapon.get("burst_pattern", False) else None
        unitWeapon["burst_duration"] = weapon.get("burst_pattern")[-1] if weapon.get("burst_pattern", False) else None
        unitWeapon["dps"] = weapon.get('dps', 0)
        unitWeapon["damage"] = int(weapon.get('damage', 0))
        unitWeapon["bombing_damage"] = int(weapon.get('bombing_damage', 0))
        unitWeapon["penetration"] = int(weapon.get("penetration", 0))
        unitWeapon["cooldown_duration"] = weapon.get("cooldown_duration", 0)
        unitWeapon["range"] = int(weapon.get("range", 0))
        unitWeapon["count"] = count
        unitWeapon["firing_type"] = weapon["firing"].get("firing_type", None) if weapon.get("firing", False) else None
        try:
            weaponMissile = weapon["firing"]["torpedo_firing_definition"]
        except KeyError:
            weaponMissile = None
        unitWeapon["spawned_unit"] = (getRace(weaponMissile.get('spawned_unit',"")) + " " + getUnitName( weaponMissile.get('spawned_unit')).replace("_", " ").title()).strip() if weaponMissile else None
        unitWeapon["missile_duration"] = weaponMissile.get("duration", None) if weaponMissile else None
        unitWeapon["bypass_shields_chance"] = weaponMissile.get("bypass_shields_chance", None) if weaponMissile else None

        unitWeapons.append(unitWeapon)

    return unitWeapons

class AlwaysContains:
    def __contains__(self, item):
        return True

        
def FormatUnitEntries(UnitList, weaponDict, filter = AlwaysContains, outputFile = False):
    LOCALIZED_TEXT

    outputDict = {}
    
    for stats in UnitList:

        unitName = stats[0]
        unitDict = stats[1]

        outputName = getUnitName(unitName)

        # Check filter
        try: unitType = unitDict.get("target_filter_unit_type")
        except: continue

        if unitType not in filter:
            continue

        print(f"Processing {outputName}...") # Print the name of the unit being processed after filtering

        # Ship Cost Block

        try: unitBuildTime = unitDict["build"]["build_time"]
        except KeyError: 
            try: unitBuildTime = unitDict["strikecraft"]["build_time"]
            except KeyError:
                unitBuildTime = 0

        try: unitCreditCost = int(unitDict["build"]["price"]["credits"])
        except KeyError: unitCreditCost = None

        try: unitMetalCost = int(unitDict["build"]["price"]["metal"])
        except KeyError: unitMetalCost = None

        try: unitCrystalCost = int(unitDict["build"]["price"]["crystal"])
        except KeyError: unitCrystalCost = None

        try: unitSupply = int(unitDict["build"]["supply_cost"])
        except KeyError: unitSupply = None

        try: exoticPrice : list = unitDict["build"]["exotic_price"]
        except KeyError: exoticPrice = []

        #Ship Durability Block
        try: unitMoveSpeed = int(unitDict["physics"]["max_linear_speed"])
        except KeyError: unitMoveSpeed = None

        try: unitTimeToMaxSpeed = unitDict["physics"]["time_to_max_linear_speed"]
        except KeyError: unitTimeToMaxSpeed = None

        try: unitAcceleration = unitMoveSpeed / unitTimeToMaxSpeed
        except TypeError: unitAcceleration = None

        try: unitTurnSpeed = unitDict["physics"]["max_angular_speed"]
        except KeyError: unitTurnSpeed = None

        # Ship Stat Block

        try: unitDurability = int(unitDict["health"]["durability"])
        except KeyError: unitDurability = 0
        
        try:   
            startingArmorStr = unitDict["health"]["levels"][0]["armor_strength"]
            endingArmorStr = unitDict["health"]["levels"][9]["armor_strength"]
            unitArmorStrength = f"{int(startingArmorStr)} - {int(endingArmorStr)} (+{int((endingArmorStr - startingArmorStr) / 9)}/lvl)"
        except:
            try: unitArmorStrength = int(unitDict["health"]["levels"][0]["armor_strength"])
            except KeyError: unitArmorStrength = 0

        try:
            startingXP = int( unitDict["health"]["levels"][0]["experience_given_on_death"])
            endingXP = int( unitDict["health"]["levels"][9]["experience_given_on_death"])
            unitXP = f"{startingXP} - {endingXP} (+{int((endingXP - startingXP) / 9)}/lvl)"
        except : 
            try: unitXP = int(unitDict["health"]["levels"][0]["experience_given_on_death"])
            except KeyError: unitXP = None

        try:
            startingHP = int( unitDict["health"]["levels"][0]["max_hull_points"])
            endingHP = int( unitDict["health"]["levels"][9]["max_hull_points"])
            unitHP = f"{startingHP} - {endingHP} (+{int((endingHP - startingHP) / 9)}/lvl)"
        except :
            try: unitHP = int( unitDict["health"]["levels"][0]["max_hull_points"])
            except : unitHP = None

        try:
            startingHPRegen = ( unitDict["health"]["levels"][0]["hull_point_restore_rate"])
            endingHPRegen = ( unitDict["health"]["levels"][9]["hull_point_restore_rate"])
            unitHPRegen = f"{startingHPRegen} - {endingHPRegen} (+{round((endingHPRegen - startingHPRegen) / 9, 2)}/lvl)"
        except :
            try: unitHPRegen = ( unitDict["health"]["levels"][0]["hull_point_restore_rate"])
            except : unitHPRegen = None

        try:
            startingAP = int( unitDict["health"]["levels"][0]["max_armor_points"])
            endingAP = int( unitDict["health"]["levels"][9]["max_armor_points"])
            unitAP = f"{startingAP} - {endingAP} (+{int((endingAP - startingAP) / 9)}/lvl)"
        except :    
            try: unitAP = int(unitDict["health"]["levels"][0]["max_armor_points"])
            except : unitAP = None

        try:
            startingAPRegen = ( unitDict["health"]["levels"][0]["armor_point_restore_rate"])
            endingAPRegen = ( unitDict["health"]["levels"][9]["armor_point_restore_rate"])
            unitAPRegen = f"{startingAPRegen} - {endingAPRegen} (+{round((endingAPRegen - startingAPRegen) / 9, 2)}/lvl)"
        except :    
            try: unitAPRegen = (unitDict["health"]["levels"][0]["armor_point_restore_rate"])
            except : unitAPRegen = None

        try:
            startingSP = int(unitDict["health"]["levels"][0]["max_shield_points"] )
            endingSP = int(unitDict["health"]["levels"][9]["max_shield_points"] )
            unitSP = f"{startingSP} - {endingSP} (+{int((endingSP - startingSP) / 9)}/lvl)"
        except :
            try: unitSP = int(unitDict["health"]["levels"][0]["max_shield_points"])
            except : unitSP = None

        try:
            startingSPRegen = (unitDict["health"]["levels"][0]["shield_point_restore_rate"] )
            endingSPRegen = (unitDict["health"]["levels"][9]["shield_point_restore_rate"] )
            unitSPRegen = f"{startingSPRegen} - {endingSPRegen} (+{round((endingSPRegen - startingSPRegen) / 9, 2)}/lvl)"
        except :
            try: unitSPRegen = (unitDict["health"]["levels"][0]["shield_point_restore_rate"])
            except : unitSPRegen = None
        
        try:
            startingSBCD = int(unitDict["health"]["levels"][0]["shield_burst_restore"]["cooldown_duration"])
            endingSBCD = int(unitDict["health"]["levels"][9]["shield_burst_restore"]["cooldown_duration"])
            unitShieldBurstCD = f"{startingSBCD} - {endingSBCD} ({round((endingSBCD-startingSBCD)/9,1)}/lvl)"
        except:
            try: unitShieldBurstCD = int(unitDict["health"]["levels"][0]["shield_burst_restore"]["cooldown_duration"])
            except KeyError: unitShieldBurstCD = None

        try:
            startingSBAmt = unitDict["health"]["levels"][0]["shield_burst_restore"]["restore_percentage"]
            endingSBAmt = unitDict["health"]["levels"][9]["shield_burst_restore"]["restore_percentage"]
            unitShieldBurstAmt = f"{int(startingSBAmt * 100)} - {int(endingSBAmt * 100)}% (+{round((endingSBAmt-startingSBAmt)*100/9,0)}%/lvl)"
        except:
            try: unitShieldBurstAmt = f"{int(unitDict["health"]["levels"][0]["shield_burst_restore"]["restore_percentage"]*100)}%"
            except KeyError: unitShieldBurstAmt = None

        unitDescription = LOCALIZED_TEXT.get(unitName + "_description", None)

        # Slot Block for structures
        try:
            slot_type = unitDict["structure"]["slot_type"]
            if slot_type == "military":
                civilian_slots = None
                military_slots = unitDict["structure"].get("slots_required", None)
            elif slot_type == "civilian":
                military_slots = None
                civilian_slots = unitDict["structure"].get("slots_required", None)
            else:
                raise ValueError(f"Unexpected slot type: {slot_type} for unit {unitName}")
        except KeyError:
            military_slots = None
            civilian_slots = None
        
        # Levels block for leveling ships
        if len(unitDict["health"]["levels"]) > 1:
            unitHealthLevels = []
            for i, stats in enumerate(unitDict["health"]["levels"]):
                unitHealthLevels.append({})

                unitHealthLevels[i]["armorstr"] = stats.get("armor_strength", None)
                unitHealthLevels[i]["hull_points"] = stats.get("max_hull_points", None)
                unitHealthLevels[i]["hull_regen"] = stats.get("hull_point_restore_rate", None)
                unitHealthLevels[i]["armor_points"] = stats.get("max_armor_points       ", None)
                unitHealthLevels[i]["armor_regen"] = stats.get("armor_point_restore_rate", None)
                unitHealthLevels[i]["shield_points"] = stats.get("max_shield_points", None)
                unitHealthLevels[i]["shield_regen"] = stats.get("shield_point_restore_rate", None)
                unitHealthLevels[i]["shield_burst_amount"] = stats["shield_burst_restore"].get("restore_percentage", None)
                unitHealthLevels[i]["shield_burst_cd"] = stats["shield_burst_restore"].get("cooldown_duration", None)
                unitHealthLevels[i]["xp"] = stats.get("experience_given_on_death", None)

        else:
            unitHealthLevels = None

        if unitDict.get("levels"):

            for i, stats in enumerate(unitDict["levels"]["levels"]):
                unitHealthLevels[i]["xp_to_next_level"] = stats.get("experience_to_next_level", None)

                unitHealthLevels[i]["antimatter_points"] = stats["unit_modifiers"]["additive_values"].get("max_antimatter", None)
                unitHealthLevels[i]["antimatter_regen"] = stats["unit_modifiers"]["additive_values"].get("antimatter_restore_rate", None)
                unitHealthLevels[i]["carrier_capacity"] = stats["unit_modifiers"]["additive_values"].get("max_squadron_capacity", None)

                try:
                    unitHealthLevels[i]["weapon_damage"] = stats["weapon_modifiers"]["scalar_values"].get("damage", None)
                    unitHealthLevels[i]["weapon_cooldown"] = stats["weapon_modifiers"]["scalar_values"].get("cooldown_duration", None)
                except KeyError:
                    unitHealthLevels[i]["weapon_damage"] = None
                    unitHealthLevels[i]["weapon_cooldown"] = None

        #Ship Weapons Block
        try:
            startingAntimatterAmt = int(unitDict["levels"]["levels"][0]["unit_modifiers"]["additive_values"]["max_antimatter"] )
            endingAntimatterAmt = int(unitDict["levels"]["levels"][9]["unit_modifiers"]["additive_values"]["max_antimatter"] )
            unitAntimatterAmt = f"{startingAntimatterAmt} - {endingAntimatterAmt} (+{int((endingAntimatterAmt - startingAntimatterAmt) / 9)}/lvl)"
        except:
            try: unitAntimatterAmt = unitDict["antimatter"]["max_antimatter"]
            except KeyError: unitAntimatterAmt = None

        try:
            startingAntimatterRegen = int(unitDict["levels"]["levels"][0]["unit_modifiers"]["additive_values"]["antimatter_restore_rate"] )
            endingAntimatterRegen = int(unitDict["levels"]["levels"][9]["unit_modifiers"]["additive_values"]["antimatter_restore_rate"] )
            unitAntimatterRegen = f"{startingAntimatterRegen} - {endingAntimatterRegen} (+{round((endingAntimatterRegen - startingAntimatterRegen) / 9, 2)}/lvl)"
        except:
            try: unitAntimatterRegen = unitDict["antimatter"]["antimatter_restore_rate"]
            except KeyError: unitAntimatterRegen = None
        
        try: unitWeaponsBlock = unitDict["weapons"]["weapons"]  
        except KeyError: unitWeaponsBlock = False #or maybe make it false and add a conditional     
        
        weaponCollection = {}

        if unitWeaponsBlock is not False:
            weaponCollection = {}
            weaponPrereqs = {}
            for weapon in unitWeaponsBlock:           

                weaponName = weapon['weapon']
                if weaponName in weaponCollection:
                    weaponCollection[weaponName] += 1
                else:
                    weaponCollection[weaponName] = 1
                    weaponPrereqs[weaponName] = weapon.get('required_unit_item', None)

        #Ship Carrier Block
        try: 
            carrier = unitDict['carrier']['base_max_squadron_capacity']
            try: 
                carrier = (f"{int(carrier + unitDict['levels']['levels'][0]['unit_modifiers']['additive_values']['max_squadron_capacity'])} - "
                + f"{int(carrier + unitDict['levels']['levels'][9]['unit_modifiers']['additive_values']['max_squadron_capacity'])}")
            except KeyError: pass
        except KeyError: carrier = False

        #Ship Strike-craft Block

        try:
            unitSquadronSize = unitDict["strikecraft"]["squadron_size"]
        except KeyError: unitSquadronSize = None

        try:
            unitStrikeCraftKind = unitDict["strikecraft"]["kind"]
        except KeyError: unitStrikeCraftKind = None

        #Ship Abilities Block

        try:
            unitAbilities_levels = unitDict["abilities"]
            unitAbilities = []

            for stats in unitAbilities_levels:
                unitAbilities += stats["abilities"]
        except KeyError: unitAbilities = None

        if unitAbilities:
            for stats, ability in enumerate(unitAbilities):
                with open(SINS_DIRECTORY / "entities" / (ability + ".ability"), "r", encoding="utf-8") as file:
                    ability_file = json.load(file)

                nameCall = ability_file["gui"]["name"]
                unitAbilities[stats] = LOCALIZED_TEXT.get(nameCall) #LOCALIZED_TEXT.get(f"{ability}_ability_name")

        
        # Final construction of output
        outputFile = Path(outputFile)

        if "dlc" in unitName:
            source = unitName.split("_")[0].upper()
        else:
            source = "Base Game"
            
        race = getRace(unitName)

        source = SOURCES.get(source, "Base Game")

        unit_entry =  (race + " " + outputName).strip()

        outputEntry = outputDict[unit_entry] = {}

        outputEntry["source"] = source
        outputEntry["race"] = race
        outputEntry["name"] = outputName
        outputEntry["type"] = unitType.replace("_", " ").title()

        outputEntry["supply"] = (unitSupply)
        outputEntry["civilianslots"] = civilian_slots
        outputEntry["militaryslots"] = military_slots
        outputEntry["credits"] = (unitCreditCost)
        outputEntry["metal"] = (unitMetalCost)
        outputEntry["crystal"] = (unitCrystalCost)
        outputEntry["buildtime"] = unitBuildTime
        formatExoticPrice(outputEntry, exoticPrice)

        outputEntry["speed"] = (unitMoveSpeed)
        outputEntry["time_to_max_linear_speed"] = unitTimeToMaxSpeed
        outputEntry["acceleration"] = unitAcceleration
        outputEntry["max_angular_speed"] = unitTurnSpeed
        
        outputEntry["durability"] = unitDurability
        outputEntry["armorstr"] = unitArmorStrength

        outputEntry["hull_points"] = unitHP
        outputEntry["hull_regen"] = unitHPRegen
        outputEntry["armor_points"] = unitAP
        outputEntry["armor_regen"] = unitAPRegen
        outputEntry["shield_points"] = unitSP
        outputEntry["shield_regen"] = unitSPRegen
        outputEntry["shield_burst_cooldown"] = unitShieldBurstCD
        outputEntry["shield_burst_amount"] = unitShieldBurstAmt
        outputEntry["xp"] = unitXP

        outputEntry["antimatter_points"] = unitAntimatterAmt
        outputEntry["antimatter_regen"] = unitAntimatterRegen

        outputEntry["description"] = unitDescription

        outputEntry["squadron_size"] = unitSquadronSize
        outputEntry["strike_craft_kind"] = unitStrikeCraftKind

        outputEntry["carrier_capacity"] = carrier if carrier is not False else None

        outputEntry["abilities"] = unitAbilities

        outputEntry["levels"] = unitHealthLevels

        outputEntry["weapons"] = createWeaponBlock(weaponCollection, weaponDict, weaponPrereqs)



    sortedDict =  {k: outputDict[k] for k in sorted(outputDict) }

    with open(f"{outputFile}.json", "w", encoding = "utf-8") as file:
        json.dump(sortedDict, file, indent=1)

def main():

    unitList = getSinsData("", ".unit")

    weaponList = getSinsData("",".weapon")
    weaponDict = createWeaponDict(weaponList)

    FormatUnitEntries(unitList, weaponDict, filter=["corvette", "frigate", "cruiser", "capital_ship", "strikecraft", "super_capital_ship", "titan", "torpedo"], outputFile= WIKIFILES_DIR / "Wikiunit")

if __name__ == "__main__":
    main()