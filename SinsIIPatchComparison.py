from SinsIIStatsThing import getSinsData, createWeaponDict, FormatUnitEntries
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
                except KeyError: pass
            
                print(f"{indents}{entry}")

                if level == 0:
                    output.write("\n")

                output.write(f"{indents}{entry}\n")


    elif type(collection) is dict:
        for name, entry in collection.items():
            if (entry == False): # or (name in weaponDict.keys()):
                pass
            elif type(entry) not in printTypes:
                print(f"{indents}{name}\n")
                if level == 0:
                    output.write("\n")
                output.write(f"{indents}{name}\n")
                recursiveprint(entry, output, localText, level + 1)
            else:
                try: entry = localText[entry]
                except KeyError: pass
            
                if level == 0:
                    output.write("\n")

                print(f"{indents}{name} : {entry}")
                output.write(f"{indents}{name} : {entry}\n")

def compareShipDicts(newDict : dict, oldDict : dict):
    
    changesDict = {}

    for i, j in newDict.items():
        print(i)
        try:
            changesDict[i] = recursiveCompare(j, oldDict[i])
        except KeyError:
            changesDict["[NEW] " + i] = j
        print()

    for i, j in oldDict.items():
        print(i)
        try:
            recursiveCompare(j, newDict[i])
        except KeyError:
            changesDict["[REMOVED] " + i] = j
        print()

    return changesDict

def recursiveCompare(obj1, obj2, level = 1):
    printTypes = [str, int, float]

    changeDict = {}

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
                    changeDict[i] = change
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
                    except KeyError:
                        change = recursiveCompare(weaponDict[j], oldWeaponDict[j], level = level + 1)

                else:  #j != obj2[i]:
                    # print(f"{indents}{i}")   
                    change = recursiveCompare(j, obj2[i], level = level + 1)

                if change != False:
                    changeDict[i] = change
                else: change = False
            except KeyError:
                change = "[NEW]"

    if changeDict == {}:
        return False
    else:
        return changeDict
    
def getSinsDataDict(race, entityType, file = "F:\\SteamLibrary\\steamapps\\common\\Sins2\\entities"):
    dataList = getSinsData(race, entityType, file = file)
    dataDict = createWeaponDict(dataList)
    return dataDict

if __name__ == "__main__":
    # Change this to match your machine.
    gameLocation = "F:\\SteamLibrary\\steamapps\\common\\Sins2"

    gameEntitiesLocation = gameLocation + "\\entities"
    gameLocalizedText = gameLocation + "\\localized_text\\en.localized_text"

    newPatchNumber = input("New Patch Number [format 1.28.16]:  ")
    pastPatchNumber = input("Previous Patch Number [format 1.28.16]:  ")

    newPatchNumber = newPatchNumber.replace(".","-")
    pastPatchNumber = pastPatchNumber.replace(".","-")

    filelist = glob.glob(gameEntitiesLocation + "\\*")
    objectTypes = []
    for f in filelist:
        objectType = f.split(".")[-1]
        if objectType not in objectTypes and objectType != "weapon":
            objectTypes.append(objectType)

    print(objectTypes)


    with open(gameLocalizedText, 'r') as t:
        inGameText = json.load(t)

    with open(newPatchNumber + "_changes.txt", 'w') as file:
        pass

    raceList = ["advent", "trader", "vasari"] # Add Minor races and general changes

    weaponDict = getSinsDataDict("",".weapon", file = gameEntitiesLocation)
    oldWeaponDict = getSinsDataDict("",".weapon", file = "Patch " + pastPatchNumber[2:].replace("-",".") + " Entities")
    

    for race in raceList:
        with open(newPatchNumber + "_changes.txt", 'a') as file:
            if race == "trader":
                file.write(f"\n\n# {'TEC'} Changes\n")
            else: file.write(f"\n\n# {race.capitalize()} Changes\n")

        ChangesList = []
        for obtype in objectTypes:

            shipDict = getSinsDataDict(race,f"{obtype}", file= gameEntitiesLocation)
            oldShipDict = getSinsDataDict(race,f"{obtype}", file = "Patch " + pastPatchNumber[2:].replace("-",".") + " Entities")


            unitChanges = compareShipDicts(shipDict, oldShipDict)

            unitChanges2 = {}

            for name, content in unitChanges.items():
                namefound = False
                new = False
                if "[NEW] " in name:
                    name = name.strip("[NEW] ")
                    new = True

                for fileSuffix in ["_name", "_ability_name", "_unit_item_name"]:
                    try:
                        name = inGameText[name+fileSuffix]
                        namefound = True
                    except:
                        continue

                if new == True:
                    name = "[NEW] " + name
                
                unitChanges2[name] = content

            ChangesList.append(unitChanges2)
            
        with open(newPatchNumber + "_changes.txt", 'a') as file:

            for i, changeDict in enumerate(ChangesList):
                listList = []
                for p, q in changeDict.items():
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
                            recursiveprint(j[1], file, inGameText, 1)
