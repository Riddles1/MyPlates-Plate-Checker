# MyPlates-Plate-Checker
This python script is designed to feed a large volume of words/combinations through the MyPlates website to see if they are still available. 

<div align="center">
  ***SETUP***
</div>

+ Create a csv with the first column named "Word" and the second column named "Availability"
+ Put all the plates that you want to check in the "Word" column
+ Inside myplates.py, input the file location of this csv and the file location of your version of Chrome's web driver (this is necessary for selenium to work)
