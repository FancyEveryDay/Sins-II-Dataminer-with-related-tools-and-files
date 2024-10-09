from SinsIIStatsThing import getSinsData, createWeaponDict, FormatUnitEntries
import json, glob


def recursiveprint(collection, output, level = 0):
    printTypes = [str, int, float]

    indents = "\t" * level

    if type(collection) is list:
        
        for entry in collection:
            if type(entry) not in printTypes:
                recursiveprint(entry, output, level + 1)
                
            else:
                print(f"{indents}{entry}")

                if level == 0:
                    output.write(f"\n")

                output.write(f"{indents}{entry}\n")


    elif type(collection) is dict:
        for name, entry in collection.items():
            if (entry == False): # or (name in weaponDict.keys()):
                pass
            elif type(entry) not in printTypes:
                print(f"{indents}{name}\n")
                if level == 0:
                    output.write(f"\n")
                output.write(f"{indents}{name}\n")
                recursiveprint(entry, output, level + 1)
            else:
                if level == 0:
                    output.write(f"\n")

                print(f"{indents}{name} : {entry}")
                output.write(f"{indents}{name} : {entry}\n")

def compareShipDicts(newDict : dict, oldDict : dict):
    
    changesDict = {}

    for i, j in newDict.items():
        print(i)
        changesDict[i] = recursiveCompare(j, oldDict[i])
        print()

    return changesDict

def recursiveCompare(obj1, obj2, level = 1):
    printTypes = [str, int, float]

    changes = {}

    indents = "\t" * level

    if (type(obj1) in printTypes) and type(obj2) in printTypes:
        if obj1 != obj2:
            # print(f"{indents}{obj2} -> {obj1}")
            return f"{obj2} -> {obj1}"
        else: return False

    if (type(obj1) is list) and (type(obj2) is list): # and (obj1 != obj2):
        for i, j in enumerate(obj1):

            try:
                # print(f"{indents}{i+1}")
                change = recursiveCompare(j, obj2[i], level = level + 1)

                if change != False:
                    changes[i] = change
                else: change = False
            except:
                change = False

    if (type(obj1) is dict) and type(obj2) is dict: #and (obj1 != obj2):
        for i, j in obj1.items():
            
            try:
                if i == "weapon":
                    # print(f"{indents}{j}")
                    try:
                        i = weaponDict[j]["name"].split('.')[-1]
                        change = recursiveCompare(weaponDict[j], oldWeaponDict[j], level = level + 1)
                    except:
                        change = recursiveCompare(weaponDict[j], oldWeaponDict[j], level = level + 1)

                else:  #j != obj2[i]:
                    # print(f"{indents}{i}")   
                    change = recursiveCompare(j, obj2[i], level = level + 1)

                if change != False:
                    changes[i] = change
                else: change = False
            except:
                change = "[NEW]"

    if changes == {}:
        return False
    else:
        return changes
    
def getSinsDataDict(race, type, file = "F:\\SteamLibrary\\steamapps\\common\\Sins2\\entities"):
    dataList = getSinsData(race, type, file = file)
    dataDict = createWeaponDict(dataList)
    return dataDict

if __name__ == "__main__":

    filelist = glob.glob(f"F:\\SteamLibrary\\steamapps\\common\\Sins2\\entities\\*")
    objectTypes = []
    for f in filelist:
        objectType = f.split(".")[-1]
        if objectType not in objectTypes and objectType != "weapon":
            objectTypes.append(objectType)

    print(objectTypes)


    with open("F:\SteamLibrary\steamapps\common\Sins2\localized_text\en.localized_text") as t:
        inGameText = json.load(t)

    with open("28-16changes.txt", 'w') as file:
        pass

    raceList = ["advent", "trader", "vasari"]

    weaponDict = getSinsDataDict("",".weapon")
    oldWeaponDict = getSinsDataDict("",".weapon", file = "Patch 28.10 Entities")
    

    for race in raceList:
        with open("28-16changes.txt", 'a') as file:
            if race == "trader":
                file.write(f"\n\n# {"TEC"} Changes\n")
            else: file.write(f"\n\n# {race.capitalize()} Changes\n")

        ChangesList = []
        for obtype in objectTypes:

            shipDict = getSinsDataDict(race,f"{obtype}")
            oldShipDict = getSinsDataDict(race,f"{obtype}", file = "Patch 28.10 Entities")


            unitChanges = compareShipDicts(shipDict, oldShipDict)

            unitChanges2 = {}

            for name, content in unitChanges.items():
                namefound = False
                for fileSuffix in ["_name", "_ability_name", "_unit_item_name"]:
                    try:
                        unitChanges2[inGameText[name+fileSuffix]] = content
                        namefound = True
                    except:
                        continue

                if namefound == False:
                    unitChanges2[name] = content

            ChangesList.append(unitChanges2)
            
        with open("28-16changes.txt", 'a') as file:

            for i, changes in enumerate(ChangesList):
                listList = []
                for p, q in changes.items():
                    listList.append((p,q))

                listList.sort(key = lambda x: x[0])

                hasChanges = False

                for j in listList:
                    if j[1] == False or j[1] == {} or j[1] == []:
                        continue
                    else:
                        hasChanges = True
                        break

                if hasChanges == True:
                    file.write("\n## " + objectTypes[i].capitalize() + " Changes\n")
                    for j in listList:
                        if j[1] != False:
                            file.write(f"\n**{j[0]}**\n")
                            recursiveprint(j[1], file, 1)
