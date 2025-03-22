import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.processing import processing
from src.visualization import make_graph_tricks, make_graph_cards
from src.datagen import decking, HALF_DECK_SIZE

def main(): 
    running = True
    print("Welcome to Mila's Penney Simulation!")
    while running == True: 
        new_decks = input("How many decks would you like to generate?  ")
        decks_int = int(new_decks)
        if decks_int == 0: 
            running = False
            continue 
        else: 
            gen_cards = decking(9903)
            gen_cards.gen_decks(decks_int)
            scoring = input("Would you like to score by cards (1), tricks (2), or both (3)?  ")
            scoring = int(scoring)
            do_it = processing()
            do_it.simulations()
            if scoring == 1: 
                cards = do_it.get_percents(tricks = False)
                graph = make_graph_cards(cards)
            elif scoring == 2:
                tricks = do_it.get_percents()
                graph = make_graph_tricks(tricks)
            elif scoring == 3:
                tricks = do_it.get_percents()
                cards = do_it.get_percents(tricks = False)
                graph1= make_graph_cards(cards)
                graph2= make_graph_tricks(tricks)
            else: 
                choice = input("Press 0 to exit the program  ")   
                if int(choice) == 0: 
                    running = False
                    continue
            choice =  input("Would you like to continue the program (1) or exit (0)?  ")
            if int(choice) == 0: 
                running = False
                continue

            
if __name__ == "__main__":
    main()  # Call the main function to run the program
