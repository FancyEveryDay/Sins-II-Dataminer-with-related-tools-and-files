# Welcome to FancyEveryDay's Sins of a Solar Empire II Data Tools

This repository contains the tools I use for all my Sins of a Solar Empire II data needs, its messy, kind of sloppy, and not really meant for other people to try to use, but some of you technically inclined people may find them useful or inspirational.

Contents:
* 5 python modules/notebooks
* Archive of patch changes and patch data
* Collection of formatted data sheets for units
* Current wiki-files

Each has been updated to use a .env file which you will need to create in the parent folder on installation.

{
   'sins2File' : '<Absolute path to sins2 file here>'
   'pastPatch' : '1.42.09'
}

## 1. SinsIIUnitStats.py and Unit Profiles
   
   The original core module, it contains functions for quickly and easily pulling and formatting data from the game.
   The script's Main() function will fill the Unit Profiles directory with a collection of .txt's formatted roughly like wiki entries for each unit in the game.
   This was made before the Strategy Wiki really got going, and a lot of the formatting I used here wound up being a good template for it.

   In order to use it on your machine you'll need to create the .env file mentioned above.

   Functions from this script power or inspired pretty much every other script in this repo.
   
## 2. SinsIIPatchComparison.py and Patch Archive
   
   This module leverages SinsIIStatsThing functions to produce a printout of all the data changes to entities.
   This is what I use to produce my Detailed Patch Notes I post to reddit.

   Creates a record of the current patch files and the patch changes inside the Patch Archive directory.

   In order to use it on your machine you'll need to create the .env file mentioned above. On starting the program, users will need to input the patch number to compare to, and the patch number to output to. It is important that any new data folders added follow the same naming scheme.

## 3. WikiMain.py and Strategy Wiki scripts

   This module contains the code for the dataminer which I am developing to replace the incomplete Java and Javascript miners I inherited when I joined the Sins 2 Wiki project. Also uses a .env but this one must be placed in the Wiki Dataminer folder. The .json format Wiki Files are created in the Wiki Data folder.

   ### Includes:
   - WikiMaine.py : Runs all mining processes in sequence.
   - wikiPlanet.py : exports all planet specific data.
   - wikiPlayer.py : exports data specific to each faction (such as lists of buildable units and research).
   - wikiPrerequisites.py : finds and creates a file which lists all items in the game and their prerequisites.
   - wikiResearch.py : exports research data.

   ### Miner Backlog:
   - wikiShipItem.py - exports ship item data
   - wikiAbility.py - exports ability data for ships, structures, and items.
   
   ### Covered by Daxos' Java dataminer but need replaced eventually
   - wikiUnit.py - exports unit data (including weapon data)
   - wikiStructure.py - (debating combining this with wikiUnit because of similarities) exports unit data
   - wikiPlanetItems.py - exports planet item data

## 4. findIconChanges.py
   This module compares the images in the game to an image folder in a location and produces an output which names all the icons for new or changed art, and then copies these new images into a folder for viewing.

   Still a bit half-baked, doesn't use a .env yet but needs one.

## 5. SinsIIExplorations.ipynb
   This notebook contains a collection of my experiments and tests as well as a few tools which you can use to potentially run your own tests.

   This notebook hasn't been updated to use the .env file so there is also an address which needs to be changed in this file, in the second code cell.

   The existing test cells are, in order:
   - Ship eHP per supply lvl 1
   - Ship eHP per supply lvl 10
   - Ship eHP per supply, lvl 10, variable piercing
   - Ship DPS per supply, variable level and target durability - If you set durability to False it will use a collection of common durabilities and average them
   - Several ship dps per cost comparisons...
   - Function which produces the table of stats/lvl for each lvling ship I have uploaded on my public google drive
   - Function which produces the table of Strike Craft at each cap ship lvl which I have uploaded on my public google drive 
