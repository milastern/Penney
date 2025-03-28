# Project Penney 

This project contains a program that runs monte-carlo simulations on every strategy in Penney's Game in order to identify the optimal strategies for players. 

## Penney's Game: Overview 

**Penney’s Game** is a probability-based card game where players choose a sequence of three card colors (e.g., red-black-red), representing red and black suits. A shuffled deck is revealed one card at a time, forming a moving sequence of three. The first player whose chosen sequence appears wins the round. Scoring can follow two main methods: **tricks-based** or **cards-based**. In the tricks-based method, the game is played over multiple rounds, and each round’s winner earns a trick, with victory going to the player who wins the most tricks. In the cards-based method, each time a sequence appears, its owner earns points based on the number of cards drawn since the last match, rewarding longer gaps between matches. Despite appearing fair, the game has a strategic twist- there is a second-mover advantage, where the player who picks second can always choose a sequence that gives them a very high probability of winning based on the opponent’s choice, making turn order a crucial part of strategy. 


## Project Overview 
This project simulates all possible strategies in **Penney’s Game** using Monte Carlo methods to identify optimal strategies for both players. By running large-scale simulations, the program quantifies the probability of success for different strategy choices under both **tricks-based** and **cards-based** scoring methods.  

### Key Components  

- **Generating and storing randomized decks** to ensure a fair and reproducible testing environment.  
- **Simulating every possible strategy combination** by iterating through predefined sequences chosen by the players.  
- **Tracking win probabilities** for Player 2 across all possible Player 1 choices to highlight the **second-mover advantage**, where Player 2 can always select a near-optimal counterstrategy.  
- **Visualizing the results** through heatmaps that display Player 2’s win rates across strategy matchups, helping to illustrate patterns in the game’s inherent probability dynamics.  

### Insights  

This analysis provides insight into how **Penney’s Game**, despite appearing fair, offers significant advantages to an informed second player. The project also serves as a demonstration of Monte Carlo simulations in game theory and probabilistic decision-making.

# Files Included

## `src/`

### `datagen.py`

This file generates decks of cards and stores them. It defines the size of each deck and the number of decks at the top of the file for ease of users to change them as desired.

It consists of a data class called `Decking`, which manages deck generation parameters, such as the random number generator's state. The `Decking` class contains one function and maintains important state information, such as the rng state, the number of times decks have been generated, and the file path where decks are saved within the program's `files` folder. To activate the class, you must specify an initial random seed.

The main function in this program, `gen_decks()`, takes only one argument: the number of decks to generate. It creates the specified number of decks and stores them in the `files` folder.

---

### `processing.py`

This file imports stored decks from `datagen.py` and contains functions to play and store the results of **Penney's Game**.

It includes six functions: `play_penney()`, `simulations()`, `get_percents()`, `get_decks()`, `load_past_data()`, and `save_simulations()` in a class called `processing`. This class doesn't take any arguements for initlization. 

#### `play_penney()`

This function takes five arguments:

- **Player 1's choice** (an array)
- **Player 2's choice** (an array)
- **The deck to use** for the game (an array)
- **The standings of these choices** (an array)

The function loops through each card in the deck, checking for each player's pattern until the game is completed. It then scores the game based on the chosen method and returns an array containing updated standings for that choice’s game:

- **Index 0**: Player 2's number of wins scored by tricks 
- **Index 1**: Number of games tied scored by tricks 
- **Index 2**: Player 2's number of wins scored by cards 
- **Index 3**: Number of games tied scored by cards 

#### `simulations()`

This function takes no arguments. First it loads all the saved decks and identifies the unprocessed decks. It then runs nested loops to generate all possible player choice combinations (ensuring they are not the same). For each combination, it plays Penney’s Game using every stored deck and updates the standings. The final results are stored in a 3D array, where the row is the index of  Player 1's choice, the column is the index of Player 2’s choice and the third dimension stores P2's wins and ties (by scoring type). These results are saved to the class so they can be updated everytime the simulations function is run

#### `get_percents()`

This function converts the stored simulation data into percentages rather than raw numbers. It only takes one argument: a booleen indicating if you are looking for the data scoring by tricks (True) or cards (False). The fucntion creates a new 3D array that divides the number of wins & ties by the number of simulations that have been completed. This allows ease of updating the current percents. This function returns the new array with the percents of wins & ties by the specified scoring type. 

#### `get_decks()`

This fucntion takes no arguments returns the number of rounds of simulations that have been run in that instance of the class. 

#### `get_past_data()`

This function loads any saved simulation data into the function, updating the arrays storing win & tie data by scoring method and the number of siluations run. This allows the user to pick up where they left off. This funtion takes no arguments and returns nothing. 

#### `save_simulations()` 

This function saves the arrays containing the sumulition data for tricks and cards as well as the number of simulations run to .npy files in the `files` folder. This function takes no arguments and returns nothing. 

---

### `visualization.py`

This file contains two functions to create a heatmap visualizing the percentage of times Player 2 wins for each choice combination.

It imports `processing.py` and contains two functions, one for generating a heatmap using **tricks** as the scoring method and another using **cards** as the scoring method. Both functions:

- Take two arguements: the array containing the simulation data for the scoring type & the number of decks that have been processed 
- Extract win and draw percentages from specified method and create a heatmap showing how often Player 2 wins each combination of strategies 
- Save heatmap to the `files` folder
- Return the heatmap

---

### `main.py`

This file contians the main program and allows the user to run it as they wish. 

First it asks the user if they wish to load any saved data into the program. This allows users to pick up where they left off and continie deck generation and processing. 

Then it prompts the user specify how many decks they wish to generate and by which method they wish to see the heat map of(cards, tricks, or both). If the user does not wish to generate any more decks they can enter 0 to move on 

Next it asks the user if they would like to generate final heatmaps and if they would like to save the data. 


---

### `Play_penney_game.ipynb`

This Jupyter Notebook imports `visualization.py` and calls both visualization functions to generate heatmaps.

Designed for ease of use, all the user needs to do is run the functions to visualize the results of **Penney's Game**.

---

### `helpers.py`

Contains a decorator function called `debugger_factory()`. This function prints the time it took a function to run, it is used for debbuging and optimization. 