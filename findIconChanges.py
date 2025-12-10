import glob
import filecmp
import shutil
import os

SINS_DIRECTORY = "f:\\SteamLibrary\\steamapps\\common\\Sins2"
TEXTURES_LOCATION = SINS_DIRECTORY + "\\textures"
SINS_FILES_LOCATION = "f:\\SinsFiles\\textures"

newPatchNumber = input("New Patch Number [format 1.28.16]:  ")
while True:
    userInput = input(f"Is '{newPatchNumber}' the correct number for the current patch? [yes/no]")

    if userInput.strip().lower() in ['yes', 'y','yea', 'yeah']:
        print("Acknowledged")
        break
    elif userInput.strip().lower() in ['no', 'n', 'nahp', 'nope', 'nay']:
        newPatchNumber = input("Current Patch Number [format 1.28.16]:  ")
    else:
        print("Input not recognized, try again.")

# Try to get pastpatch number from .env, otherwise from user.
# try: 
#     pastPatchNumber = env["pastPatch"]
# except KeyError:
print("No previous patch number found, please input one.")
pastPatchNumber = input("Previous Patch Number [format 1.28.16]:  ")

while True:
    userInput = input(f"Is '{pastPatchNumber}' the correct number for the previous patch? [yes/no]")

    if userInput.strip().lower() in ['yes', 'y','yea', 'yeah']:
        print("Acknowledged")
        break
    elif userInput.strip().lower() in ['no', 'n', 'nahp', 'nope', 'nay']:
        pastPatchNumber = input("Previous Patch Number [format 1.28.16]:  ")
    else:
        print("Input not recognized, try again.")

# Copy over new set of files
print("Copying new texture files")

new_data_folder = f"{SINS_FILES_LOCATION}\\Patch {newPatchNumber[2:]} Textures"
past_data_folder = f"{SINS_FILES_LOCATION}\\Patch {pastPatchNumber[2:]} Textures"

try:
    shutil.copytree(TEXTURES_LOCATION,  new_data_folder)
except FileExistsError:
    shutil.rmtree(new_data_folder)
    shutil.copytree(TEXTURES_LOCATION, new_data_folder)

# Change number formatting (for reasons)
newPatchNumber = newPatchNumber.replace(".","-")
pastPatchNumber = pastPatchNumber.replace(".","-")


## Get files
oldImages = glob.glob(f"{past_data_folder}\\**tooltip_picture200.png")
newImages = glob.glob("f:\\SteamLibrary\\steamapps\\common\\Sins2\\textures\\**tooltip_picture200.png")

shutil.rmtree(f"{SINS_FILES_LOCATION}\\New Textures")
os.mkdir(f"{SINS_FILES_LOCATION}\\New Textures")

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

    shutil.copy2(newImage, f"{SINS_FILES_LOCATION}\\New Textures")
