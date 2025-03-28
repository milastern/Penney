import pandas as pd
import numpy as np
import os 
import json
from src.helpers import debugger_factory
from src.datagen import DECK_SIZE


class processing:
    """
    Class for simulating and processing Monte Carlo experiments for Penney's Game.

    Attributes:
        decks_prosessed (int): The total number of decks that have been processed.
        results_by_cards (np.ndarray): A 3D array (shape: 8x8x2) storing cumulative outcomes using
            the cards-based scoring method. For each pair of player choices, the two values represent
            Player 2's wins and ties.
        results_by_tricks (np.ndarray): A 3D array (shape: 8x8x2) storing cumulative outcomes using
            the tricks-based scoring method. For each pair of player choices, the two values represent
            Player 2's wins and ties.

    Methods:
        play_penney(pick1, pick2, deck, standings):
            Simulates a single round of Penney's Game with a given deck and updates the standings.
        simulations():
            Runs simulations across all unique combinations of player choices using the stored decks.
        get_percents(tricks=True):
            Calculates and returns the win and tie percentages for the specified scoring method.
        get_decks():
            Returns the total number of decks that have been processed.
        load_past_data():
            Loads previously saved simulation data from storage, updating internal state accordingly.
        save_simulations():
            Saves the current simulation data (results and number of processed decks) to storage files.
    """
    def __init__(self):
        self.decks_prosessed = 0 #number of decks processed
        self.results_by_cards =  np.zeros((8, 8, 2), dtype=int) #results of each set of choices (scored by cards)
        self.results_by_tricks =  np.zeros((8, 8, 2), dtype=int) #results of each set of choices (scored by tricks)

    def play_penney(self,
                    pick1: np.ndarray,
                    pick2: np.ndarray,
                    deck: np.ndarray,
                    standings: list,
                    ) -> list:
        """
        Simulates a round of Penney’s Game with the given deck and scoring method.

        Args:
            player1_choice (np.ndarray): Player 1's sequence of choices.
            player2_choice (np.ndarray): Player 2's sequence of choices.
            deck (np.ndarray): The deck used for the game.
            standings (list): The current standings (wins, losses, draws).

        Returns:
            list: Updated standings [wins (tricks), ties (tricks), wins (cards), ties (cards)].
        """
        last_win, tricks1, tricks2, cards1, cards2, curr = 0, 0, 0, 0, 0, 0  #initilizing variables for the game 
        while curr <= (DECK_SIZE-3): #keep looping through the deck until you run out of cards 
            top_of_deck = deck[curr: curr+3] #top three cards 
            if np.all(top_of_deck == pick1): #check if player 1's pick is at the top of the deck 
                tricks1 += 1
                cards1 += (curr - last_win + 3)
                last_win = curr + 3 
                curr += 3
            elif np.all(top_of_deck == pick2):  #check if player 2's pick is at the top of the deck 
                tricks2 += 1
                cards2 += curr - last_win + 3
                last_win = curr +3 
                curr += 3
            else:  #if niether is at top of deck, deal the next card and try again
                curr += 1
        
        #update game standings         
        if tricks1 < tricks2: #P2 wins by tricks 
            standings[0] += 1 
        elif tricks1 == tricks2: #ties by tricks 
            standings[1] += 1   
        if cards1 < cards2: #P2 wins by cards 
            standings[2] += 1
        elif cards1 == cards2: #ties by cards 
            standings[3] += 1 
        return standings  #return the updated standings 

    #@debugger_factory(show_args=False) #debugger decorator to time how long the simulation runs for
    def simulations(self) -> None:
        """
        Runs simulations for all unique player choice combinations across stored decks and saves the standings to the class

        Returns:
            None
        """
        
        file_path = os.path.join("files", "deck_storage.npy")
        ready_decks = np.load(file_path)  #load decks into the program 
        if len(ready_decks) > self.decks_prosessed: #check to see if there are unprocessed decks  
            new_decks = len(ready_decks)- self.decks_prosessed 
            ready_decks = ready_decks[-new_decks:] #set array of decks to just the unprocessed ones 
        choices = np.array([[0,0,0], [0,0,1], [0,1,0], [0,1,1], [1,0,0], [1,0,1], [1,1,0], [1,1,1]]) #strategy choices 
        for i in range(8): #for each of the 8 choices 
            pick1 = choices[i] #give playert 1 choice i 
            for k in range(8): #for each of the 8 choices 
                pick2 = choices[k] #give playert 2 choice k
                if i == k: 
                    continue #if p1 and p2 have the same choice, skip to the next combo of choices 
                standings = [0,0,0,0] #initialize standings for each choice 
                for deck in ready_decks: #for each deck 
                    standings = self.play_penney(pick1, pick2, deck, standings) #play the game for that deck and combo of player's choices 
                self.results_by_tricks[i,k,0] += standings[0] #update the standings to the class so it can be accessed later 
                self.results_by_tricks[i,k,1] += standings[1]
                self.results_by_cards[i,k, 0] += standings[2]
                self.results_by_cards[i,k, 1] += standings[3] 
        self.decks_prosessed += len(ready_decks) #update the number of decks we have processed
        return None 

    def get_percents(self, tricks: bool = True) -> np.ndarray:
        """
    Calculate the win and tie percentages for each matchup based on the scoring method.

    Args:
        tricks (bool, optional): If True, compute percentages using tricks-based scoring data; if False, use
                                 cards-based scoring data. Defaults to True.

    Returns:
        np.ndarray: A 3D NumPy array of shape (8, 8, 2) where the first two dimensions represent the player
                    choice combinations and the third dimension contains the win and tie percentages.
        """
        percentages = np.zeros((8, 8, 2), dtype=float) #create a new array for datastorage 
        if tricks == True: #check if we are scoring by tricks 
            for i in range(8): 
                for k in range(8): #for each combination of choices 
                    if i == k: 
                        continue #except not when p1 and p2 have the same choice 
                    percentages[i,k,0] =(self.results_by_tricks[i,k,0]/self.decks_prosessed)*100 #get win results and convert to percent 
                    percentages[i,k,1] = (self.results_by_tricks[i,k,1]/self.decks_prosessed)*100 #get tie results and convert to percent 
        elif tricks == False: 
            for i in range(8):
                for k in range(8): #for each combination of choices 
                    if i == k: 
                        continue #except not when p1 and p2 have the same choice 
                    percentages[i,k,0] =(self.results_by_cards[i,k,0]/self.decks_prosessed)*100 #get win results and convert to percent
                    percentages[i,k,1] = (self.results_by_cards[i,k,1]/self.decks_prosessed)*100 #get tie results and convert to percent 
        return percentages #return array of percentage reasults 
    
    def get_decks(self) -> int:
        """
    Retrieve the total number of decks processed.

    Returns:
        int: The cumulative count of decks that have been processed during the simulations.
        """
        decks = self.decks_prosessed #get number of decks that have been processed 
        return decks #return it 
    
    def load_past_data(self) -> None:
        """
    Load previously saved simulation data from storage files.

    This function updates the internal state of the object by reading the cumulative results for both
    cards-based and tricks-based scoring methods, as well as the total number of decks processed. It
    loads data from pre-defined .npy files stored in the "files" directory so that the simulation can
    resume from where it left off.

    Returns:
        None
        """
        cards = np.load("files/results_cards.npy") #load standings by cards
        tricks = np.load("files/results_tricks.npy") #load standings by tricks 
        n_decks = np.load("files/n_decks_processed.npy") #load number of decks processed 
        self.decks_prosessed = n_decks #assign the data to the class so it can be acessed again 
        self.results_by_cards = cards
        self.results_by_tricks = tricks
        return None
    
    def save_simulations(self)-> None:
        """
    Save the current simulation data to storage files.

    This function writes the cumulative simulation results for both tricks-based and cards-based scoring methods,
    as well as the total number of decks processed, to corresponding .npy files in the 'files' directory.

    Returns:
        None
        """
        folder_path = 'files'
        tricks_file = os.path.join(folder_path, "results_tricks.npy") 
        cards_file = os.path.join(folder_path, "results_cards.npy") 
        n_decks_file = os.path.join(folder_path, "n_decks_processed.npy") 
        np.save(tricks_file, self.results_by_tricks) #save tricks results 
        np.save(cards_file, self.results_by_cards) #save cards results 
        np.save(n_decks_file, self.decks_prosessed) #save number of decks processed 
        return None 

