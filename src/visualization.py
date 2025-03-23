import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd 
import numpy as np
from src.processing import processing
import os



def make_graph_tricks(result_dict: dict,
                      num_decks: int):
    """
    Generates a heatmap visualizing Player 2’s win percentage using tricks as the scoring method.

    Returns:
        heatmap figure
    """
    color_p1 = ["BBB", "BBR", "BRB", "BRR", "RBB", "RBR", "RRB", "RRR"]
    color_p2 = ["BBB", "BBR", "BRB", "BRR", "RBB", "RBR", "RRB", "RRR"]
    num_decks = num_decks
    df = pd.DataFrame([{'i': key[0], 'k': key[1], 'value': value} for key, value in result_dict.items()])
    df['value'] = df['value'].apply(lambda x: x if isinstance(x, list) else [0, 0, 0]) 
    df_pivot = df.pivot(index='k', columns='i', values='value')
    win_matrix = df_pivot.applymap(lambda x: x[0] if isinstance(x, list) else 0).to_numpy().T
    draw_matrix = df_pivot.applymap(lambda x: x[1] if isinstance(x, list) else 0).to_numpy().T
    labels = np.array([[f"{round(win)}\n({round(draw)})" for win, draw in zip(win_row, draw_row)] 
                    for win_row, draw_row in zip(win_matrix, draw_matrix)])
    plt.figure(figsize=(8, 6))
    ax = sns.heatmap(win_matrix, annot=labels, fmt="", cmap="Blues", cbar=False, linewidths=0.5, linecolor="black",
                 xticklabels=color_p1, yticklabels=color_p2)
    plt.xlabel("My Choice", fontsize=12)
    plt.ylabel("Opponent Choice", fontsize=12)
    plt.title(f"Heat Map of Win Percentage; Scoring = Tricks\n(Decks Processed: {num_decks})", fontsize=14, fontweight="bold")
    plt.xticks(rotation=45, ha='right')
    plt.yticks(rotation=0)
    folder_path = 'files'
    file_path = os.path.join(folder_path, 'scoring_by_tricks.png')
    plt.savefig(file_path, format='png')
    plt.show()
    figure = plt.gcf()
    return figure 


def make_graph_cards(result_dict: dict,
                     num_decks: int):
    """
    Generates a heatmap visualizing Player 2’s win percentage using cards as the scoring method.

    Returns:
        heatmap figure
    """
    color_p1 = ["BBB", "BBR", "BRB", "BRR", "RBB", "RBR", "RRB", "RRR"]
    color_p2 = ["BBB", "BBR", "BRB", "BRR", "RBB", "RBR", "RRB", "RRR"]
    num_decks = num_decks
    df = pd.DataFrame([{'i': key[0], 'k': key[1], 'value': value} for key, value in result_dict.items()])
    df['value'] = df['value'].apply(lambda x: x if isinstance(x, list) else [0, 0, 0]) 
    df_pivot = df.pivot(index='k', columns='i', values='value')
    win_matrix = df_pivot.applymap(lambda x: x[0] if isinstance(x, list) else 0).to_numpy().T
    draw_matrix = df_pivot.applymap(lambda x: x[1] if isinstance(x, list) else 0).to_numpy().T
    labels = np.array([[f"{round(win)}\n({round(draw)})" for win, draw in zip(win_row, draw_row)] 
                    for win_row, draw_row in zip(win_matrix, draw_matrix)])
    plt.figure(figsize=(8, 6))
    ax = sns.heatmap(win_matrix, annot=labels, fmt="", cmap="Blues", cbar=False, linewidths=0.5, linecolor="black",
                 xticklabels=color_p1, yticklabels=color_p2)
    plt.xlabel("My Choice", fontsize=12)
    plt.ylabel("Opponent Choice", fontsize=12)
    plt.title(f"Heat Map of Win Percentage; Scoring = Cards\n(Decks Processed: {num_decks})", fontsize=14, fontweight="bold")
    plt.xticks(rotation=45, ha='right')
    plt.yticks(rotation=0)
    folder_path = 'files'
    file_path = os.path.join(folder_path, 'scoring_by_cards.png')
    plt.savefig(file_path, format='png')
    plt.show()
    figure = plt.gcf()
    return figure 

