import pandas as pd
import numpy as np
import os 
import json
from src.helpers import debugger_factory

from src.datagen import DECK_SIZE
class processing:
    def __init__(self):
        self.decks_prosessed = 0 
        self.results_by_cards =  np.zeros((8, 8, 2), dtype=int)
        self.results_by_tricks =  np.zeros((8, 8, 2), dtype=int)

    def play_penney(self,
                    pick1: np.ndarray,
                    pick2: np.ndarray,
                    deck: np.ndarray,
                    standings: list,
                    ) -> np.ndarray:
        """
        Simulates a round of Penney’s Game with the given deck and scoring method.

        Args:
            player1_choice (np.ndarray): Player 1's sequence of choices.
            player2_choice (np.ndarray): Player 2's sequence of choices.
            deck (np.ndarray): The deck used for the game.
            standings (list): The current standings (wins, losses, draws).
            score_by_tricks (bool): Whether to score by tricks (default: True) or by cards.

        Returns:
            list: Updated standings [wins, losses, draws].
        """
        last_win, tricks1, tricks2, cards1, cards2, curr = 0, 0, 0, 0, 0, 0  
        while curr <= (DECK_SIZE-3): 
            top_of_deck = deck[curr: curr+3] 
            if np.all(top_of_deck == pick1): 
                tricks1 += 1
                cards1 += (curr - last_win + 3)
                last_win = curr + 3 
                curr += 3
            elif np.all(top_of_deck == pick2):
                tricks2 += 1
                cards2 += curr - last_win + 3
                last_win = curr +3 
                curr += 3
            else: 
                curr += 1
                
        if tricks1 < tricks2: 
            standings[0] += 1 
        elif tricks1 == tricks2: 
            standings[1] += 1   
        if cards1 < cards2: 
            standings[2] += 1
        elif cards1 == cards2: 
            standings[3] += 1 
        return standings  

    @debugger_factory(show_args=False)
    def simulations(self) -> dict:
        """
        Runs simulations for all unique player choice combinations across stored decks.

        Args:
            score_by_tricks (bool): Scoring method (default: tricks).

        Returns:
            dict: Dictionary mapping player choices to their game outcome percentages.
        """
        
        file_path = os.path.join("files", "deck_storage.npy")
        ready_decks = np.load(file_path)  
        if len(ready_decks) > self.decks_prosessed:
            new_decks = len(ready_decks)- self.decks_prosessed 
            ready_decks = ready_decks[-new_decks:]
        choices = np.array([[0,0,0], [0,0,1], [0,1,0], [0,1,1], [1,0,0], [1,0,1], [1,1,0], [1,1,1]])
        for i in range(8):
            pick1 = choices[i]
            for k in range(8):
                pick2 = choices[k]
                if i == k: 
                    continue 
                standings = [0,0,0,0] 
                for deck in ready_decks:
                    standings = self.play_penney(pick1, pick2, deck, standings)
                self.results_by_tricks[i,k,0] += standings[0]
                self.results_by_tricks[i,k,1] += standings[1]
                self.results_by_cards[i,k, 0] += standings[2]
                self.results_by_cards[i,k, 1] += standings[3] 
        self.decks_prosessed += len(ready_decks)
        return  

    def get_percents(self, tricks: bool = True):
        percentages = np.zeros((8, 8, 2), dtype=float)
        if tricks == True: 
            for i in range(8):
                for k in range(8):
                    if i == k: 
                        continue 
                    percentages[i,k,0] =(self.results_by_tricks[i,k,0]/self.decks_prosessed)*100
                    percentages[i,k,1] = (self.results_by_tricks[i,k,1]/self.decks_prosessed)*100
        elif tricks == False: 
            for i in range(8):
                for k in range(8):
                    if i == k: 
                        continue 
                    percentages[i,k,0] =(self.results_by_cards[i,k,0]/self.decks_prosessed)*100
                    percentages[i,k,1] = (self.results_by_cards[i,k,1]/self.decks_prosessed)*100
        return percentages
    
    def get_decks(self):
        decks = self.decks_prosessed
        return decks 
    
    def load_past_data(self):
        cards = np.load("files/results_cards.npy")
        tricks = np.load("files/results_tricks.npy")
        n_decks = np.load("files/n_decks_processed.npy")
        self.decks_prosessed = n_decks 
        self.results_by_cards = cards
        self.results_by_tricks = tricks
        return
    
    def save_simulations(self):
        folder_path = 'files'
        tricks_file = os.path.join(folder_path, "results_tricks.npy")
        cards_file = os.path.join(folder_path, "results_cards.npy")
        n_decks_file = os.path.join(folder_path, "n_decks_processed.npy")
        np.save(tricks_file, self.results_by_tricks)
        np.save(cards_file, self.results_by_cards)
        np.save(n_decks_file, self.decks_prosessed)
        return

