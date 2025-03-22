import pandas as pd
import numpy as np
import os 
import json
from src.helpers import debugger_factory

from src.datagen import DECK_SIZE
class processing:
    def __init__(self):
        self.decks_prosessed = 0 
        self.results_by_cards = {}
        self.results_by_tricks = {} 

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
        cards_used = 0 
        tricks1 = 0
        tricks2 = 0
        cards1 = 0
        cards2 = 0 
        curr = 0 
        while curr <= (DECK_SIZE-1): 
            top_of_deck = deck[curr: curr+3] 
            if len(top_of_deck) < 3:
                curr += 1 
                continue
            if np.array_equal(top_of_deck, pick1): 
                tricks1 += 1
                cards1 = cards1 + (curr - cards_used + 3)
                cards_used = curr + 3 
                curr = curr +3 
            elif np.array_equal(top_of_deck, pick2):
                tricks2 += 1
                cards2 = cards2 + (curr - cards_used + 3)
                cards_used = curr +3 
                curr = curr+3 
            else: 
                curr += 1
                
        if tricks1 < tricks2: 
            standings[0] += 1 
        if tricks1 > tricks2: 
            standings[1] += 1 
        if tricks1 == tricks2: 
            standings[2] += 1   
        if cards1 < cards2: 
            standings[3] += 1
        if cards1 > cards2: 
            standings[4] += 1 
        if cards1 == cards2: 
            standings[5] += 1 
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
        
        file_path = os.path.join("files", "deck_storage.npy")  # Update the file path  

        if not os.path.exists(file_path):  
            raise FileNotFoundError(f"File not found: {file_path}")  

        ready_decks = np.load(file_path)  
        #ready_decks = np.load('deck_storage.npy')
        if len(ready_decks) > self.decks_prosessed:
            new_decks = len(ready_decks)- self.decks_prosessed 
            ready_decks = ready_decks[-new_decks:]
        player1 = [[0,0,0], [0,0,1], [0,1,0], [0,1,1], [1,0,0], [1,0,1], [1,1,0], [1,1,1]]
        player2 = [[0,0,0], [0,0,1], [0,1,0], [0,1,1], [1,0,0], [1,0,1], [1,1,0], [1,1,1]]
        for i in range(len(player1)):
            pick1 = player1[i]
            for k in range(len(player2)):
                pick2 = player2[k]
                if pick1 == pick2: 
                    continue 
                standings = [0,0,0,0,0,0] 
                for n in range(len(ready_decks)):
                    standings = self.play_penney(pick1, pick2, ready_decks[n], standings)
                self.results_by_tricks[(i,k)] = [standings[0], standings[1], standings[2]] 
                self.results_by_cards[(i,k)] = [standings[3], standings[4], standings[5]] 
        self.decks_prosessed += len(ready_decks)
        return  

    def get_percents(self, tricks: bool = True):
        percentages = {}
        player1 = [[0,0,0], [0,0,1], [0,1,0], [0,1,1], [1,0,0], [1,0,1], [1,1,0], [1,1,1]]
        player2 = [[0,0,0], [0,0,1], [0,1,0], [0,1,1], [1,0,0], [1,0,1], [1,1,0], [1,1,1]]
        if tricks == True: 
            for i in range(len(player1)):
                pick1 = player1[i]
                for k in range(len(player2)):
                    pick2 = player2[k]
                    if pick1 == pick2: 
                        continue 
                    percentages[(i,k)] =[self.results_by_tricks[(i,k)][0]/self.decks_prosessed,
                                        self.results_by_tricks[(i,k)][1]/self.decks_prosessed,
                                        self.results_by_tricks[(i,k)][2]/self.decks_prosessed]
        elif tricks == False: 
            for i in range(len(player1)):
                pick1 = player1[i]
                for k in range(len(player2)):
                    pick2 = player2[k]
                    if pick1 == pick2: 
                        continue 
                    percentages[(i,k)] =[self.results_by_cards[(i,k)][0]/self.decks_prosessed,
                                        self.results_by_cards[(i,k)][1]/self.decks_prosessed,
                                        self.results_by_cards[(i,k)][2]/self.decks_prosessed]
        return percentages


