# Welcome to FancyEveryDay's Personal Sins of a Solar Empire II Data Tools

This repository contains my personal tools I use for all my Sins of a Solar Empire II data needs, its messy, kind of sloppy, and not really meant for other people to try to use, but some of you technically inclined people may find them useful or inspirational.

The repository currently contains 3 modules, I've also uploaded the latest collection of unit stats files produced by the SinsIIStatsThing.py

## 1. SinsIIStatsThing.py
   
   The core module, it contains functions for quickly and easily pulling and formatting data from the game.
   The file's Main() function will produce a collection of files full of .txt's formatted roughly like wiki entries for each unit in the game.
   This was made before the WIki really got going, and probably some of the formatting I did here will wind up being incorporated into the wiki when I get around to it.

   In order to use it on your machine you'll need to change the address in the getSinsData() function on line 34 to the address of the entities folder for your game.
   If you want it to print out the correct names, the address in the open() function on line 84 needs to be changed to the location of the en.localized_text file for your game.
   
## 2. SinsIIPatchComparison.py
   
   This module leverages SinsIIStatsThing functions to produce a printout of all the data changes to entities.
   In order to use it you have to copy the entities of a previous patch somewhere you can access them, either while the game is rolled back or before you update.
   This is what I use to produce my Detailed Patch Notes I post to reddit.

   There is one address users will need to change on line 130. On starting the program, users will need to input the patch number to compare to, and the patch number to    output to. It is important that any new data folders added follow the same naming scheme, with the 1 omitted on the front end.

## 3. SinsIIFun.ipynb
   This notebook contains a bunch of experiments and tests as well as a few tools which you can use to potentially run your own tests.

There is also an address which needs to be changed in this file, in the second code cell.

The existing test cells are, in order:
   - Ship eHP per supply lvl 1
   - Ship eHP per supply lvl 10
   - Ship eHP per supply, lvl 10, variable piercing
   - Ship  DPS per supply, variable level and target durability - If you set durability to False it will use a collection of common durabilities and average them
   - Function which produces the table of stats/lvl for each lvling ship I have uploaded on my public google drive
   - Function which produces the table of Strike Craft at each cap ship lvl which I have uploaded on my public google drive 
     
