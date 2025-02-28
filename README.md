
Files Included
src/
datagen.py
This file generates decks of cards and stores them along with their corresponding random seeds. It defines the size of each deck and the number of decks at the top of the file for ease of users to change them as desired. 
It consists of a data class called Decking, which manages deck generation parameters, such as the latest seed used. The Decking class contains one function and maintains important state information, such as the last seed used, the number of times decks have been generated, and the file path where decks are saved within the program's files folder. To activate the class, you must specify an initial random seed.
The main function in this program, gen_store_decks_seeds(), takes only one argument: the number of decks to generate. It creates the specified number of decks, stores them in the files folder, and returns them as an array, along with an array of the seeds used and the integer value of the next seed to use.
At the bottom of the file, we instantiate the Decking class with seed 9903 (inspired by my birthday, if you were curious) and then call gen_store_decks_seeds() to generate and store the specified number and size of decks.

processing.py
This file imports stored decks from datagen.py and contains functions to play and store the results of Penney's Game.
It includes two functions: play_penney() and simulations(). It also imports the deck size from datagen.py to ensure consistency throughout the program. Importing datagen.py ensures that deck generation and storage occur before processing begins.
play_penney()
This function takes five arguments:
Player 1's choice (an array)
Player 2's choice (an array)
The deck to use for the game (an array)
The standings of these choices (an array)
A boolean specifying the scoring method (default: True for tricks, False for cards)
The function loops through each card in the deck, checking for each player's pattern until the game is completed. It then scores the game based on the chosen method and returns an array containing updated standings for that choice’s game:
Index 0: Number of wins
Index 1: Number of losses
Index 2: Number of draws
simulations()
This function takes one argument: the preferred scoring method (default: tricks). It runs nested loops to generate all possible player choice combinations (ensuring they are not the same). For each combination, it plays Penney’s Game using every stored deck and updates the standings. The final results are stored as percentages in a dictionary, where the key is a tuple representing Player 1’s and Player 2’s choices.
The function then returns this dictionary containing the standings for every unique combination of choices.

visualization.py
This file processes game results and creates a heatmap visualizing the percentage of times Player 2 wins for each choice combination.
It imports processing.py and contains two functions, one for generating a heatmap using tricks as the scoring method and another using cards as the scoring method. Both functions:
Take no arguments
Call simulations() to run the simulation using the corresponding scoring method
Convert the results dictionary into a pandas DataFrame
Extract win and draw percentages from each result and create a heatmap showing how often Player 2 wins each combination

Play_penney_game.ipynb
This Jupyter Notebook imports visualization.py and calls both visualization functions to generate heatmaps.
Designed for ease of use, all the user needs to do is run the functions to visualize the results of Penney's Game. 

