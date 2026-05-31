from wikiUnit import getSinsData, createWeaponDict, FormatUnitEntries, WIKIFILES_DIR

# Override main from wikiUnit
def main():

    unitList = getSinsData("", ".unit")

    weaponList = getSinsData("",".weapon")
    weaponDict = createWeaponDict(weaponList)

    FormatUnitEntries(unitList, weaponDict, filter=["structure", "starbase"], outputFile= WIKIFILES_DIR / "Wikistructure")

if __name__ == "__main__":
    main()