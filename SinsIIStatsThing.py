

import json, glob

def recursiveprint(collection, output, localText = {}, level = 0):
    printTypes = [str, int, float]

    indents = "\t" * level

    if type(collection) is list:
        for entry in collection:
            if type(entry) not in printTypes:
                recursiveprint(entry, output, localText, level + 1)
                
            else:
                try: entry = localText[entry]
                except: pass
                
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
                except: pass

                print(f"{indents}{name} : {entry}")
                output.write(f"{indents}{name} : {entry}\n")

def getSinsData(race, type, output = False, file = "F:\\SteamLibrary\\steamapps\\common\\Sins2\\entities" ):
    unitfilelist = glob.glob(f"{file}\\{race}**{type}")

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
        except: 
            try:
                weaponStats["dps"] = weaponStats["bombing_damage"] / weaponStats["cooldown_duration"]
            except:
                pass

        WeaponsDict[indexName] = weaponStats

    return WeaponsDict
        
def FormatUnitEntries(UnitList, weaponDict, filter = "health", consolePrint = True, outputFile = False):
    with open("F:\\SteamLibrary\\steamapps\\common\\Sins2\\localized_text\\en.localized_text") as t:
        inGameText = json.load(t)
    
    for i in UnitList:

        unitName = i[0].split("\\")[-1]
        unitDict = i[1]
        if filter in unitDict:

            try: outputName = inGameText[unitName + "_name"]
            except: outputName = unitName

            #Ship Cost Block

            #print("\tResource Cost")

            try: unitBuildTime = unitDict["build"]["build_time"]
            except: unitBuildTime = ""

            try: unitCreditCost = unitDict["build"]["price"]["credits"]
            except: unitCreditCost = ""

            try: unitMetalCost = unitDict["build"]["price"]["metal"]
            except: unitMetalCost = ""

            try: unitCrystalCost = unitDict["build"]["price"]["crystal"]
            except: unitCrystalCost = ""

            try: unitSupply = unitDict["build"]["supply_cost"]
            except: unitSupply = ""

            #Ship Durability Block
            try: unitMoveSpeed = unitDict["physics"]["max_linear_speed"]
            except: unitMoveSpeed = ""

            try: unitAcceleration = unitMoveSpeed / unitDict["physics"]["time_to_max_linear_speed"]
            except: unitAcceleration = ""

            try: unitDurability = unitDict["health"]["durability"]
            except: unitDurability = ""
 
            try: unitArmorStrength = unitDict["health"]["levels"][0]["armor_strength"]   
            except: unitArmorStrength = ""

            try:
                startingHP = int( unitDict["health"]["levels"][0]["max_hull_points"])
                endingHP = int( unitDict["health"]["levels"][9]["max_hull_points"])
                unitHP = f"{startingHP} - {endingHP}"
            except:
                try: unitHP = int( unitDict["health"]["levels"][0]["max_hull_points"])
                except: unitHP = ""   

            try:
                startingAP = int( unitDict["health"]["levels"][0]["max_armor_points"])
                endingAP = int( unitDict["health"]["levels"][9]["max_armor_points"])
                unitAP = f"{startingAP} - {endingAP}"
            except:    
                try: unitAP = int(unitDict["health"]["levels"][0]["max_armor_points"])
                except: unitAP = ""

            try:
                startingSP = int(unitDict["health"]["levels"][0]["max_shield_points"] )
                endingSP = int(unitDict["health"]["levels"][9]["max_shield_points"] )
                unitSP = f"{startingSP} - {endingSP}"
            except:
                try: unitSP = int(unitDict["health"]["levels"][0]["max_shield_points"])
                except: unitSP = ""

            try: unitShieldBurstCD = unitDict["health"]["levels"][0]["shield_burst_restore"]["cooldown_duration"]
            except: unitShieldBurstCD = "nan"

            #Ship Weapons Block

            try: unitAntimatterAmt = unitDict["antimatter"]["max_antimatter"]
            except: unitAntimatterAmt = ""
            
            try: unitWeaponsBlock = unitDict["weapons"]["weapons"]  
            except: unitWeaponsBlock = False #or maybe make it false and add a conditional     
            
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
                except: pass
            except: carrier = False

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
                print(f"\t\tweapon name\tdps\tcount\ttdps\tpen\trange")

                for weapon, count in weaponCollection.items():
                    weaponName : str = weaponDict[weapon]["name"].split(".")[-1]
                    weaponName = weaponName.replace("_", " ")

                    weaponDPS : float = weaponDict[weapon]['dps']
                    weaponDPS = round(weaponDPS, 1)
                    
                    try: weaponPenetration = weaponDict[weapon]["penetration"]
                    except: weaponPenetration = 0

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
                        except: weaponPenetration = 0

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

    weaponList = getSinsData("",".weapon")
    weaponDict = createWeaponDict(weaponList)

    FormatUnitEntries(tecUnitList, weaponDict, consolePrint= False, outputFile="TEC Units")
    FormatUnitEntries(adventUnitList, weaponDict, consolePrint= False, outputFile="Advent Units")
    FormatUnitEntries(vasariUnitList, weaponDict, consolePrint= False, outputFile="Vasari Units")
    
if __name__ == "__main__":
    main()