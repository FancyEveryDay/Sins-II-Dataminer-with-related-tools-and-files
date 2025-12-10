

import json, glob

# try:
with open(".env", 'r') as file:
    env = json.load(file)
    SINS_DIRECTORY = env['sins2File']
    LAST_PATCH_NUM = env["pastPatch"]
# except FileNotFoundError:
#     print(".env file not found")

try:
    with open(SINS_DIRECTORY + "\\localized_text\\en.localized_text") as t:
        LOCALIZED_TEXT = json.load(t)
except FileNotFoundError:
    print("Localized text file not found")


def recursiveprint(collection, output = False, localText = {}, level = 0):
    printTypes = [str, int, float]

    indents = "\t" * level

    if output is not False:

        if type(collection) is list:
            for entry in collection:
                if type(entry) not in printTypes:
                    recursiveprint(entry, output, localText, level + 1)
                    
                else:
                    try: entry = localText[entry]
                    except KeyError: pass
                    
                    print(f"{indents}{entry}")
                    output.write(f"{indents}{entry}\n")


        elif type(collection) is dict:
            for name, entry in collection.items():

                if type(entry) not in printTypes:
                    print(f"{indents}{name}\n")
                    output.write(f"\n{indents}{name}\n")
                    recursiveprint(entry, output, localText, level + 1)
                else:
                    try: entry = localText[entry]
                    except KeyError: pass

                    print(f"{indents}{name} : {entry}")
                    output.write(f"{indents}{name} : {entry}\n")

    else:
        if type(collection) is list:
            for entry in collection:
                if type(entry) not in printTypes:
                    recursiveprint(entry, output, localText, level + 1)
                    
                else:
                    try: entry = localText[entry]
                    except KeyError: pass
                    
                    print(f"{indents}{entry}")


        elif type(collection) is dict:
            for name, entry in collection.items():

                if type(entry) not in printTypes:
                    print(f"{indents}{name}\n")
                    recursiveprint(entry, output, localText, level + 1)
                else:
                    try: entry = localText[entry]
                    except KeyError: pass

                    print(f"{indents}{name} : {entry}")

def getSinsData(race, type, output = False, file = SINS_DIRECTORY + "\\entities" ):
    unitfilelist = glob.glob(f"{file}\\**{race}**{type}")

    listODatas = []

    if output == True:

        with open(f"{race}{type}Text.txt", "w") as output:
            output.write("Sins of a Solar Empire 2 Unit Characteristics\n")

            for unitfile in unitfilelist:
                with open(unitfile) as unitJSON:
                    d = json.load(unitJSON)
                
                print(unitfile.split("\\")[-1])
                output.write(unitfile.split("\\")[-1] + "\n")
                recursiveprint(d, output, 1)

    else:
        for unitfile in unitfilelist:
                with open(unitfile) as unitJSON:
                    d = json.load(unitJSON)

                listODatas.append([unitfile.split("\\")[-1].split(".")[0], d])

    return listODatas

# def printAllData(data, output = None):

def createWeaponDict(WeaponList):
    WeaponsDict = {}

    for weapon in WeaponList:
        indexName = weapon[0].split("\\")[-1]
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
        
def FormatUnitEntries(UnitList, weaponDict, filter = "health", consolePrint = True, outputFile = False):
    with open(SINS_DIRECTORY + "\\localized_text\\en.localized_text") as t:
        inGameText = json.load(t)
    
    for i in UnitList:

        unitName = i[0].split("\\")[-1]
        unitDict = i[1]
        if filter in unitDict:

            try: outputName = inGameText[unitName + "_name"]
            except KeyError: outputName = unitName

            #Ship Cost Block

            #print("\tResource Cost")

            try: unitBuildTime = unitDict["build"]["build_time"]
            except KeyError: unitBuildTime = ""

            try: unitCreditCost = unitDict["build"]["price"]["credits"]
            except KeyError: unitCreditCost = ""

            try: unitMetalCost = unitDict["build"]["price"]["metal"]
            except KeyError: unitMetalCost = ""

            try: unitCrystalCost = unitDict["build"]["price"]["crystal"]
            except KeyError: unitCrystalCost = ""

            try: unitSupply = unitDict["build"]["supply_cost"]
            except KeyError: unitSupply = ""

            #Ship Durability Block
            try: unitMoveSpeed = unitDict["physics"]["max_linear_speed"]
            except KeyError: unitMoveSpeed = ""

            try: unitAcceleration = unitMoveSpeed / unitDict["physics"]["time_to_max_linear_speed"]
            except KeyError: unitAcceleration = ""

            try: unitDurability = unitDict["health"]["durability"]
            except KeyError: unitDurability = ""
 
            try: unitArmorStrength = unitDict["health"]["levels"][0]["armor_strength"]   
            except KeyError: unitArmorStrength = ""

            try:
                startingHP = int( unitDict["health"]["levels"][0]["max_hull_points"])
                endingHP = int( unitDict["health"]["levels"][9]["max_hull_points"])
                unitHP = f"{startingHP} - {endingHP}"
            except IndexError:
                try: unitHP = int( unitDict["health"]["levels"][0]["max_hull_points"])
                except KeyError: unitHP = ""   

            try:
                startingAP = int( unitDict["health"]["levels"][0]["max_armor_points"])
                endingAP = int( unitDict["health"]["levels"][9]["max_armor_points"])
                unitAP = f"{startingAP} - {endingAP}"
            except IndexError:    
                try: unitAP = int(unitDict["health"]["levels"][0]["max_armor_points"])
                except KeyError: unitAP = ""
            except KeyError: unitAP = ""

            try:
                startingSP = int(unitDict["health"]["levels"][0]["max_shield_points"] )
                endingSP = int(unitDict["health"]["levels"][9]["max_shield_points"] )
                unitSP = f"{startingSP} - {endingSP}"
            except IndexError:
                try: unitSP = int(unitDict["health"]["levels"][0]["max_shield_points"])
                except KeyError: unitSP = ""
            except KeyError: unitSP = ""

            

            try: unitShieldBurstCD = unitDict["health"]["levels"][0]["shield_burst_restore"]["cooldown_duration"]
            except KeyError: unitShieldBurstCD = "nan"

            #Ship Weapons Block

            try: unitAntimatterAmt = unitDict["antimatter"]["max_antimatter"]
            except KeyError: unitAntimatterAmt = "nan"
            
            try: unitWeaponsBlock = unitDict["weapons"]["weapons"]  
            except KeyError: unitWeaponsBlock = False #or maybe make it false and add a conditional     
            
            weaponCollection = {}

            if unitWeaponsBlock is not False:
                weaponCollection = {}
                for weapon in unitWeaponsBlock:
                    weapon = weapon['weapon']
                    if weapon in weaponCollection:
                        weaponCollection[weapon] += 1
                    else:
                        weaponCollection[weapon] = 1

            #Ship Carrier Block
            try: 
                carrier = unitDict['carrier']['base_max_squadron_capacity']
                try: 
                    carrier = (f"{int(carrier + unitDict['levels']['levels'][0]['unit_modifiers']['additive_values']['max_squadron_capacity'])} - "
                    + f"{int(carrier + unitDict['levels']['levels'][9]['unit_modifiers']['additive_values']['max_squadron_capacity'])}")
                except KeyError: pass
            except KeyError: carrier = False

            #Ship Abilities Block

            if consolePrint == True:
                print(outputName)

                print(f"\tSupply: \t{unitSupply}")
                print(f"\tCredits:\t{unitCreditCost}")
                print(f"\tMetal:  \t{unitMetalCost}")
                print(f"\tCrystal:\t{unitCrystalCost}")
                print()

                print(f"\tMovespeed:\t{unitMoveSpeed}")
                print(f"\tAcceleration:\t{unitAcceleration}")
                print()

                print(f"\tDurability:\t{unitDurability}")
                print(f"\tArmor Strength:\t{unitArmorStrength}")
                print()
                print(f"\tHull Points:\t{unitHP}")
                print(f"\tArmor Points:\t{unitAP}")
                print(f"\tShield Points:\t{unitSP}")
                print(f"\t   Shield Burst CD: {unitShieldBurstCD}s")
                print()

                print(f"\tAntimatter:\t{unitAntimatterAmt}")
                print()
                print("\tWeapons:")
                print("\t\tweapon name\tdps\tcount\ttdps\tpen\trange")

                for weapon, count in weaponCollection.items():
                    weaponName : str = weaponDict[weapon]["name"].split(".")[-1]
                    weaponName = weaponName.replace("_", " ")

                    weaponDPS : float = weaponDict[weapon]['dps']
                    weaponDPS = round(weaponDPS, 1)
                    
                    try: weaponPenetration = weaponDict[weapon]["penetration"]
                    except KeyError: weaponPenetration = 0

                    weaponRange = weaponDict[weapon]["range"]
                    
                    print(f"\t\t{weaponName}\t{weaponDPS}\tx{count}\t{weaponDPS * count}\t{weaponPenetration}\t{weaponRange}")

                print()

                if carrier is not False:
                    print(f"\tStrike Craft: {carrier}")
            
            if outputFile != False:
                with open(outputFile + "\\" + outputName + ".txt", "w") as unitFile:
                    unitFile.write(outputName + "\n")

                    unitFile.write(f"\tSupply: \t{unitSupply}\n")
                    unitFile.write(f"\tCredits:\t{unitCreditCost}\n")
                    unitFile.write(f"\tMetal:  \t{unitMetalCost}\n")
                    unitFile.write(f"\tCrystal:\t{unitCrystalCost}\n\n")

                    unitFile.write(f"\tMovespeed:\t{unitMoveSpeed}\n")
                    unitFile.write(f"\tAcceleration:\t{unitAcceleration}\n\n")

                    unitFile.write(f"\tDurability:\t{unitDurability}\n")
                    unitFile.write(f"\tArmor Strength:\t{unitArmorStrength}\n\n")
                    
                    unitFile.write(f"\tHull Points:\t{unitHP}\n")
                    unitFile.write(f"\tArmor Points:\t{unitAP}\n")
                    unitFile.write(f"\tShield Points:\t{unitSP}\n")
                    unitFile.write(f"\t   Shield Burst CD: {unitShieldBurstCD}s\n\n")

                    unitFile.write(f"\tAntimatter:\t{unitAntimatterAmt}\n\n")

                    unitFile.write("\tWeapons:\n")
                    columns = ["weapon name", "dps", "count", "tdps", "pen", "range" ]
                    unitFile.write(f"\t\t{columns[0]: <25}\t{columns[1]:<5}\t{columns[2]:<5}\t{columns[3]:<5}\t{columns[4]:<6}\t{columns[5]:<5}\n")

                    for weapon, count in weaponCollection.items():
                        weaponName : str = weaponDict[weapon]["name"].split(".")[-1]
                        weaponName = weaponName.replace("_", " ")

                        weaponDPS : float = weaponDict[weapon]['dps']
                        weaponDPS = round(weaponDPS, 1)
                        
                        try: weaponPenetration = int(weaponDict[weapon]["penetration"])
                        except KeyError: weaponPenetration = 0

                        weaponRange = int(weaponDict[weapon]["range"])
                        
                        unitFile.write(f"\t\t{weaponName:<25}\t{weaponDPS:<5}\tx{count:<5}\t{round(weaponDPS * count,1):<5}\t{weaponPenetration:<6}\t{weaponRange:<5}\n")

                    if carrier is not False:
                        unitFile.write(f"\n\tStrike Craft: {carrier}\n")
    # necessary weapon entries: "dps", "penitration", "damage", "cooldown duration", "name".split(".")[-1], "range"
    # necessary unit entries: "weapons" (needs a custom function to pull weapon entries), "health" : {"durability, "levels" [{"max_hull_points", "max_armor_points", "armor_strength", "max_shield_points", "shield_burst"}] }


def main():
    vasariUnitList = getSinsData("vasari",".unit")
    tecUnitList = getSinsData("trader",".unit")
    adventUnitList = getSinsData("advent",".unit")
    dlc_UnitList = getSinsData("dlc", ".unit")

    weaponList = getSinsData("",".weapon")
    weaponDict = createWeaponDict(weaponList)

    FormatUnitEntries(tecUnitList, weaponDict, consolePrint= False, outputFile="TEC Units")
    FormatUnitEntries(adventUnitList, weaponDict, consolePrint= False, outputFile="Advent Units")
    FormatUnitEntries(vasariUnitList, weaponDict, consolePrint= False, outputFile="Vasari Units")
    FormatUnitEntries(dlc_UnitList, weaponDict, consolePrint= False, outputFile="DLC Units")
    
if __name__ == "__main__":
    main()