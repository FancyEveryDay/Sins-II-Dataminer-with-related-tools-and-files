import wikiPlanet 
import wikiPlayer
import wikiPrerequisites
import wikiResearch
import wikiUtilities
import wikiUnit
import wikiStructure
import wikiPlanetItem
import wikiShipItem

def main():
    
    wikiPlanet.main()
    completeItemSet = wikiPlayer.main()
    prereqsDict = wikiPrerequisites.main(completeItemSet = completeItemSet)
    wikiResearch.main(prereqsDict)
    wikiUnit.main()
    wikiStructure.main()
    wikiPlanetItem.main()
    wikiShipItem.main()

if __name__ == "__main__":
    main()