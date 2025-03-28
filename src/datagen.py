import numpy as np
import os 
import json

HALF_DECK_SIZE = 26
DECK_SIZE = HALF_DECK_SIZE*2
N_DECKS = 250000

class decking: 
    
    """
    Manages deck generation and storage, tracking the last used seed and file paths.

    Attributes:
        self.seed (int): The seed used for the random number generator.
        self.rng (generator): The rng we use to get random unique deck shuffles
        self.rounds (int): Number of times decks have been generated.
        self.storage_dir (str): Path where files are saved.

    Methods: 
        gen_decks: generates and stores decks of cards
    """
        
    def __init__(self, seed: int = 9903):
        self.seed = seed 
        self.rng=np.random.default_rng(self.seed) #Create and store the rng 
        self.rounds = 0 #track and store how many times decks have been created 
        self.storage_dir = os.path.join(os.getcwd(), "files")  # Store files in "files/"
        os.makedirs(self.storage_dir, exist_ok=True) # Ensure the "files" folder exists
    
    def gen_decks(self, 
                n_decks: int, 
                half_deck_size: int = HALF_DECK_SIZE 
                ) -> None: 
        """
        Generates and stores decks of cards.

        Args:
            num_decks (int): Number of decks to generate.
            HALF_DECK_SIZE (int): Number of cards in each deck, defaulted to the size specified at the top of the file .
            
        Returns:
            None
        """
        init_deck = [0]*half_deck_size + [1]*half_deck_size #generate a deck of 26 1s and 26 0s 
        decks = np.tile(init_deck, (n_decks, 1)) #creates a 2D array of n_decks number of decks 
        self.rng.permuted(decks, axis=1, out=decks) #shuffles the decks so each is unique 
        deck_storage_path = os.path.join(self.storage_dir, "deck_storage.npy") 
        state_file_path = os.path.join(self.storage_dir, "state.json")
        if self.rounds == 0 and os.path.exists(deck_storage_path): 
            os.remove(deck_storage_path)  # Ensure fresh storage when the class is first instantiated
    
        if os.path.exists(deck_storage_path): # Check if stuff.npy exists, and append data if so
            existing_decks = np.load(deck_storage_path)
            decks = np.vstack((existing_decks, decks))  # Append new decks to the end of the array 
        
        np.save(deck_storage_path, decks)  # Save updated decks
        state = self.rng.bit_generator.state
        with open(state_file_path, 'w') as f: #save random state for recordkeeping 
            json.dump(state, f)
        self.rounds += 1  #update number of deck generation rounds completed 
        return None
