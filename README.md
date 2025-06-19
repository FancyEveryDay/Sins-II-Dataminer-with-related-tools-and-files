# Welcome to FancyEveryDay's Personal Sins of a Solar Empire II Data Tools

This repository contains my personal tools I use for all my Sins of a Solar Empire II data needs, its messy, kind of sloppy, and not really meant for other people to try to use, but some of you technically inclined people may find them useful or inspirational.

The repository currently contains 3 modules, I've also uploaded the latest collection of unit stats files produced by the SinsIIStatsThing.py

Each has been updated to use a .env file which you will need to create in the parent folder on installation.
{
   'sins2File' : '<Address to sins2 file here>'
   'pastPatch' : '1.42.09'
}

## 1. SinsIIStatsThing.py
   
   The core module, it contains functions for quickly and easily pulling and formatting data from the game.
   The file's Main() function will produce a collection of files full of .txt's formatted roughly like wiki entries for each unit in the game.
   This was made before the WIki really got going, and probably some of the formatting I did here will wind up being incorporated into the wiki when I get around to it.

   In order to use it on your machine you'll need to create the .env file mentioned above.
   
## 2. SinsIIPatchComparison.py
   
   This module leverages SinsIIStatsThing functions to produce a printout of all the data changes to entities.
   In order to use it you have to copy the entities of a previous patch somewhere you can access them, either while the game is rolled back or before you update.
   This is what I use to produce my Detailed Patch Notes I post to reddit.

   In order to use it on your machine you'll need to create the .env file mentioned above. On starting the program, users will need to input the patch number to compare to, and the patch number to    output to. It is important that any new data folders added follow the same naming scheme, with the 1 omitted on the front end.

## 3. SinsIIFun.ipynb
   This notebook contains a bunch of experiments and tests as well as a few tools which you can use to potentially run your own tests.

   This notebook hasn't been updated to use the .env file so there is also an address which needs to be changed in this file, in the second code cell.

   The existing test cells are, in order:
      - Ship eHP per supply lvl 1
      - Ship eHP per supply lvl 10
      - Ship eHP per supply, lvl 10, variable piercing
      - Ship  DPS per supply, variable level and target durability - If you set durability to False it will use a collection of common durabilities and average them
      - Function which produces the table of stats/lvl for each lvling ship I have uploaded on my public google drive
      - Function which produces the table of Strike Craft at each cap ship lvl which I have uploaded on my public google drive 

## 4. jsonReading.ipnb
   This notebook is really not for public consumption and mostly contains experiments and doodles where I am attempting to pull and organize certain pieces of information from game files. May prove useful to someone inclined to learn directly from code.

## 5. WikiMain.py and other wiki scripts

   This module contains the code for the dataminer which I am developing to replace the incomplete Java and Javascript miners I inherited when I joined the Sins 2 Wiki project. Also uses a .env       but this one must be placed in the Wiki Dataminer folder. The .json format Wiki Files are created in the Wiki Data folder.

   ### Includes:
   - wikiPlanet.py : exports all planet specific data

   ### Not Included But in Active Development:
   - wikiPlayer.py - exports data specific to each faction (which mostly comes from .player files)
   - wikiResearch.py - exports research data. Partially covered by Jintekki's Javascript Dataminer.

   ### Miner Backlog:
   - wikiShipItem.py - exports ship item data
   - wikiAbility.py - exports ability data for ships, structures, and items.
   
   #### Covered by Daxos' Java dataminer but need replaced eventually
   - wikiUnit.py - exports unit data (including weapon data)
   - wikiStructure.py - (debating combing this with wikiUnit because of similarities) exports unit data
   - wikiPlanetItems.py - exports planet item data

   
