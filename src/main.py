import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.processing import processing
from src.visualization import make_graph_tricks, make_graph_cards
from src.datagen import decking, HALF_DECK_SIZE

def main(): 
    running = True
    do_it = processing()
    gen_cards = decking(9903)
    print("Welcome to Mila's Penney Simulation!")
    new = input("Would you like to load saved data? yes(1) or no(2)?  ")
    if int(new) == 1:
        do_it.load_past_data()
        gen_cards.reload()
    while running == True: 
        n_decks = do_it.get_decks()
        print(f"You currently have {n_decks} processed decks.")
        new_decks = input("How many decks would you like to generate?  ")
        decks_int = int(new_decks)
        if decks_int == 0: 
            running = False
            continue 
        else: 
            gen_cards.gen_decks(decks_int)
            scoring = input("Would you like to score by cards (1), tricks (2), or both (3)?  ")
            scoring = int(scoring)
            do_it.simulations()
            if scoring == 1: 
                cards = do_it.get_percents(tricks = False)
                decks = do_it.get_decks()
                graph = make_graph_cards(cards, decks)
            elif scoring == 2:
                tricks = do_it.get_percents()
                decks = do_it.get_decks()
                graph = make_graph_tricks(tricks, decks)
            elif scoring == 3:
                tricks = do_it.get_percents()
                cards = do_it.get_percents(tricks = False)
                decks = do_it.get_decks()
                graph1= make_graph_cards(cards, decks)
                graph2= make_graph_tricks(tricks, decks)
            else: 
                choice = input("Press 0 to exit deck generation & processing ")   
                if int(choice) == 0: 
                    running = False
                    continue
            choice =  input("Would you like to continue deck generation & processing (1) or exit (0)?  ")
            if int(choice) == 0: 
                running = False
                continue
    more = input("Would you like to generate final graphs (0) or continue (1)?  ")
    if int(more) == 0: 
        tricks = do_it.get_percents()
        cards = do_it.get_percents(tricks = False)
        decks = do_it.get_decks()
        graph1= make_graph_cards(cards, decks)
        graph2= make_graph_tricks(tricks, decks)

    save = input("Would you like to save your data (0) or exit without saving (1)?  ")
    if int(save) == 0:
        do_it.save_simulations()
        print("Data Saved")
    print("Goodbye.")
            
if __name__ == "__main__":
    main()  # Call the main function to run the program
