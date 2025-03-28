import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.processing import processing
from src.visualization import make_graph_tricks, make_graph_cards
from src.datagen import decking, HALF_DECK_SIZE

def main(): 
    """
    The main function that runs the Penney's Game simulation.

    This function handles the overall flow of the simulation, including loading
    saved data, generating new decks, running simulations, and displaying the results.
    The user is prompted for input at several stages to customize the simulation's behavior,
    including deck generation, scoring methods (cards or tricks), and final graph generation.
    The function allows the user to save the simulation results before exiting.

    Steps:
        1. Greets the user and asks whether they would like to load past data.
        2. Prompts for how many new decks to generate.
        3. Runs simulations based on user-selected scoring methods (cards, tricks, or both).
        4. Optionally generates and displays graphs based on the selected scoring method.
        5. Allows the user to save the simulation results before exiting.
        6. Exits when the user chooses to stop deck generation or processing.

    Prompts:
        - Load saved data (yes/no)
        - Generate a specified number of decks
        - Select scoring method (cards/tricks/both)
        - Continue processing or exit
        - Generate final graphs or skip
        - Save results or exit without saving

    Returns:
        None
    """
    running = True
    do_it = processing() #initialize processing 
    gen_cards = decking(9903) #intialize deck generation 
    print("Welcome to Mila's Penney Simulation!")
    new = input("Would you like to load saved data? yes(1) or no(2)?  ") #user imputs a value 
    if int(new) == 1: #if user says yes load in saved data and generate the coresponding number of decks
        do_it.load_past_data()
        past = do_it.get_decks()
        gen_cards.gen_decks(past)
    while running == True: 
        n_decks = do_it.get_decks()
        print(f"You currently have {n_decks} processed decks.") #tells user how many decks they currently have processed 
        new_decks = input("How many decks would you like to generate?  ") #user imputs the number of decks they want generated 
        decks_int = int(new_decks)
        if decks_int == 0: #if they want 0 decks stop this phase of the program 
            running = False
            continue 
        else: #otherwise contine 
            gen_cards.gen_decks(decks_int) #generate specified number of decks 
            scoring = input("Would you like to score by cards (1), tricks (2), or both (3)?  ") #score by chosen method(s)
            scoring = int(scoring)
            do_it.simulations()
            if scoring == 1: 
                cards = do_it.get_percents(tricks = False) #do the data generation and processing
                decks = do_it.get_decks()
                graph = make_graph_cards(cards, decks) #make the graph
            elif scoring == 2:
                tricks = do_it.get_percents() #do the data generation and processing
                decks = do_it.get_decks()
                graph = make_graph_tricks(tricks, decks) #make the graph
            elif scoring == 3:
                tricks = do_it.get_percents() #do the data generation and processing for tricks 
                cards = do_it.get_percents(tricks = False) #do the data generation and processing for cards 
                decks = do_it.get_decks()
                graph1= make_graph_cards(cards, decks) #make the graph for cards 
                graph2= make_graph_tricks(tricks, decks) #make the graph for cards 
            else: 
                choice = input("Press 0 to exit deck generation & processing ")   #user indicates if they would like to make and process more decks or not 
                if int(choice) == 0: 
                    running = False
                    continue
            choice =  input("Would you like to continue deck generation & processing (1) or exit (0)?  ") #user indicates if they would like to make and process more decks or not 
            if int(choice) == 0: 
                running = False
                continue
    more = input("Would you like to generate final graphs (1) or skip (0)?  ") #user indicates if they would like to generate final graphs 
    if int(more) == 1: 
        tricks = do_it.get_percents()
        cards = do_it.get_percents(tricks = False)
        decks = do_it.get_decks()
        graph1= make_graph_cards(cards, decks)
        graph2= make_graph_tricks(tricks, decks)

    save = input("Would you like to save your data (1) or exit without saving (0)?  ") #user indicates if they would like to save their data or not
    if int(save) == 1:
        do_it.save_simulations()
        print("Data Saved")
    print("Goodbye.")
    return None 
            
if __name__ == "__main__":
    main()  # Call the main function to run the program
