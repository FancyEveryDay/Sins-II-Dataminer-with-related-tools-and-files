import wikiPlanet 
import wikiPlayer
import wikiPrerequisites
import wikiUtilities

def main():
    
    wikiPlanet.main()
    completeItemSet = wikiPlayer.main()
    wikiPrerequisites.main(completeItemSet = completeItemSet)


if __name__ == "__main__":
    main()