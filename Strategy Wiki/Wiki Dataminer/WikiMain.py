import wikiPlanet 
import wikiPlayer
import wikiPrerequisites
import wikiResearch
import wikiUtilities

def main():
    
    wikiPlanet.main()
    completeItemSet = wikiPlayer.main()
    prereqsDict = wikiPrerequisites.main(completeItemSet = completeItemSet)
    wikiResearch.main(prereqsDict)



if __name__ == "__main__":
    main()