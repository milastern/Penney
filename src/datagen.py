import numpy as np
import os 
import json

HALF_DECK_SIZE = 26
DECK_SIZE = HALF_DECK_SIZE*2
N_DECKS = 250000

class decking: 
    
    def __init__(self, seed: int):
        self.seed = seed
        self.rounds = 0 
        self.storage_dir = os.path.join(os.getcwd(), "files")  # Store files in "files/"
        # Ensure the "files" folder exists
        os.makedirs(self.storage_dir, exist_ok=True)
    """
    Manages deck generation and storage, tracking the last used seed and file paths.

    Attributes:
        self.seed (int): The last random seed used.
        self.rounds (int): Number of times decks have been generated.
        self.storage_dir (str): Path where files are saved.
    """
        
    def gen_decks(self, 
                n_decks: int, 
                half_deck_size: int = HALF_DECK_SIZE 
                ) : #-> tuple[np.ndarray, np.ndarray, int]
        """
    Generates and stores decks of cards along with their seeds.

    Args:
        num_decks (int): Number of decks to generate.
        HALF_DECK_SIZE (int): Number of cards in each deck, defaulted to the size specified at the top of the file .
        
    Returns:
        tuple: (list of decks, list of seeds, next seed to use).
    """
        init_deck = [0]*half_deck_size + [1]*half_deck_size
        decks = np.tile(init_deck, (n_decks, 1))
        rng = np.random.default_rng(self.seed)
        rng.permuted(decks, axis=1, out=decks)
        seeds = np.array(range(self.seed, self.seed+n_decks+1))
        self.seed = self.seed+n_decks+1
        # Check if stuff.npy exists, and append data if so
        deck_storage_path = os.path.join(self.storage_dir, "deck_storage.npy")
        state_file_path = os.path.join(self.storage_dir, "state.json")
         # Ensure fresh storage when the class is first instantiated
        if self.rounds == 0 and os.path.exists(deck_storage_path):
            os.remove(deck_storage_path)  #  # Start fresh when first generating deck
    
        if os.path.exists(deck_storage_path):
            existing_decks = np.load(deck_storage_path)
            decks = np.vstack((existing_decks, decks))  # Append new decks
        
        np.save(deck_storage_path, decks)  # Save updated decks
        
        state = rng.bit_generator.state
        with open(state_file_path, 'w') as f:
            json.dump(state, f)
        the_next = self.seed
        self.rounds += 1
        return decks, seeds, the_next
    

#gen_cards = decking(9903)
#gen_cards.gen_decks(N_DECKS)