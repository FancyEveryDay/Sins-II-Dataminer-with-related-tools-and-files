import glob
import filecmp

oldImages = glob.glob("f:\\SinsFiles\\textures\\**tooltip_picture.png")
newImages = glob.glob("f:\\SteamLibrary\\steamapps\\common\\Sins2\\textures\\**tooltip_picture.png")

oldImagesDict = {}

for i in oldImages:
    oldImagesDict[i.split("\\")[-1] ] = i

newImagesDict = {}

for i in newImages:
    newImagesDict[i.split("\\")[-1] ] = i

for i, newImage in newImagesDict.items():
    oldImage = oldImagesDict.get(i, False)
    if oldImage:
        if filecmp.cmp(newImage, oldImage, shallow=False):
            continue
        else:
            print(i)
    else:
        print("[NEW] " + i)
