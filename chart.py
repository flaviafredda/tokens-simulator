import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


#TODO: gestire costanti da mettere da qualche parte nel titolo
#TODO: gestire risoluziokne, ad ora tutto appiccicato
def create_bar_chart_statistics(statistic_lenders, statistic_borrowers, filename=None):
    behaviors_L = []
    max_values_L = []
    mean_values_L = []
    min_values_L = []

    for behavior, values in statistic_lenders.items():
        behaviors_L.append(behavior)
        max_values_L.append(max(values))
        mean_values_L.append(np.mean(values))
        min_values_L.append(min(values))

    behaviors_B = []
    max_values_B = []
    mean_values_B = []
    min_values_B = []

    for behavior, values in statistic_borrowers.items():
        behaviors_B.append(behavior)
        max_values_B.append(max(values))
        mean_values_B.append(np.mean(values))
        min_values_B.append(min(values))

    # Setting the positions and width for the bars
    pos = list(range(len(statistic_lenders)))
    width = 0.25

    fig, ax = plt.subplots(2)
    fig.suptitle('Tokens divided by behaviors')

    ax[0].bar([p - width for p in pos], max_values_L, width, alpha=0.5, color='r', label='max')
    ax[0].bar(pos, mean_values_L, width, alpha=0.5, color='y', label='mean')
    ax[0].bar([p + width for p in pos], min_values_L, width, alpha=0.5, color='b', label='min')

    # labels and title
    ax[0].set_title('Lender statistics', fontstyle='italic')
    ax[0].set_xticks([p + 0.5 * width for p in pos], behaviors_L)
    ax[0].legend(['Max', 'Mean', 'Min'], loc='upper left')

    pos_B = list(range(len(statistic_borrowers)))

    ax[1].bar([p - width for p in pos_B], max_values_B, width, alpha=0.5, color='r', label='max')
    ax[1].bar(pos, mean_values_B, width, alpha=0.5, color='y', label='mean')
    ax[1].bar([p + width for p in pos_B], min_values_B, width, alpha=0.5, color='b', label='min')

    # labels and title
    ax[1].set_title('Borrower statistics', fontstyle='italic')
    ax[1].set_xticks([p + 0.5 * width for p in pos_B], behaviors_B)
    ax[1].legend(['Max', 'Mean', 'Min'], loc='upper left')
    if filename:
        plt.savefig(f'img/{filename}', bbox_inches='tight', dpi=300)
    else:
        plt.show()

def create_line_graph_players(players, filename=None):
    players_names = [players[p].name for p in players]
    players_behavior_lending = [players[p].behavior_lending for p in players]
    players_behavior_borrowing = [players[p].behavior_borrowing for p in players]
    tokens_display = [players[p].tokens for p in players]


    # Plotting the line graph
    plt.figure(figsize=(10, 5))  # Set the figure size as desired
    plt.scatter(players_names, tokens_display, marker='o')  # 'o' creates a circle marker at each data point

    # Customizing the x-axis to show multiple labels vertically stacked
    ax = plt.gca()  # Get the current Axes instance
    ax.set_xticks(range(len(players_names)))  # Set the x-ticks to correspond to the number of persons

    # Set the custom labels for each tick
    xtick_labels = [f'B:{b_borrowing[0]}\n L:{b_lending[0]}' for b_borrowing, b_lending in zip(players_behavior_borrowing, players_behavior_lending)]
    ax.set_xticklabels(xtick_labels, rotation=0, ha='center')  # Rotate labels if needed

    # Adding axis labels and a title
    plt.xlabel('Player Details')
    plt.ylabel('Tokens')
    plt.title('Player Tokens and Behaviors')

    # Display the plot
    plt.tight_layout() 
    if filename:
        plt.savefig(f'img/{filename}', bbox_inches='tight', dpi=300)
    else:
        plt.show()

def create_line_graph_wallet(wallet_balance_history):
    plt.figure()
    plt.plot(wallet_balance_history)
    plt.xlabel('Round Number')
    plt.ylabel('Wallet Balance')
    plt.title('Wallet Balance Over Rounds')
    plt.show()

def create_boxplot_statistics(ax_borrowers, ax_lenders, statistic_lenders, statistic_borrowers, filename=None):
    ax_borrowers.set_title('Borrower statistics', fontstyle='italic')
    ax_lenders.set_title('Lender statistics', fontstyle='italic')
    #------ borrowers ----------------
    random_b = statistic_borrowers.get('B = random', 0)
    opportunistic_b = statistic_borrowers.get('B = opportunistic', 0)
    honest_b = statistic_borrowers.get('B = honest', 0)
    malicious_b = statistic_borrowers.get('B = malicious', 0)
    data_b = [malicious_b, honest_b, random_b, opportunistic_b]
    labels_b = ['Malicious', 'Virtuous', 'Random', 'Rational']

    #------ lenders ----------------
    random_l = statistic_lenders.get('L = random', 0)
    opportunistic_l = statistic_lenders.get('L = opportunistic, 0')
    honest_l = statistic_lenders.get('L = honest', 0)
    malicious_l = statistic_lenders.get('L = malicious', 0)
    data_l = [malicious_l, honest_l, random_l, opportunistic_l]
    labels_l = ['Malicious', 'Virtuous', 'Random', 'Rational']

    # Creating the boxplot
    sns.boxplot(data=data_b, palette="PRGn", ax = ax_borrowers)
    ax_borrowers.set_xticks(range(len(labels_b)))
    ax_borrowers.set_xticklabels(labels_b, fontsize = 15)

    # ax_borrowers.set_xticks(range(len(labels_b)), labels = labels_b) #For jupyter does not work
    ax_borrowers.set_ylabel('Tokens\' balance', fontsize = 15)
    # ax_borrowers.set_xlabel('Behaviors')
    ax_borrowers.set_title('BORROWERS', fontsize=20, fontstyle='normal', fontweight='bold')


    sns.boxplot(data=data_l, palette="PRGn", width = 0.8, showfliers=False, ax = ax_lenders)
    ax_lenders.set_xticks(range(len(labels_l)))
    ax_lenders.set_xticklabels(labels_l, fontsize = 15)
    ax_lenders.set_ylabel('Tokens\' balance', fontsize = 15)
    ax_lenders.set_title('LENDERS', fontsize=20, fontstyle='normal', fontweight='bold')


def create_tokens_exchanged_graph(ax, exchanged_tokens, borrowable_objects_history, filename = None):
    
    color1 = 'tab:red'
    ax.set_title('Trend of number of tokens exchanged', fontsize = 20)
    ax.set_xlabel('Days', fontsize=14)
    # ax.set_ylabel('Tokens', color = color1)
    ax.set_ylabel('Tokens', fontsize=14)
    ax.plot(exchanged_tokens, 'o-', color = color1)
    ax.tick_params(axis='y', labelcolor=color1)
    ax.set_box_aspect(9/16) #heigth/width
    
    # color2 = 'tab:blue'
    # ax2 = ax.twinx()
    # ax2.plot(borrowable_objects_history, '*-', color = color2)
    # ax2.set_ylabel('Borrowable objects', color = color2)
    # ax2.tick_params(axis='y', labelcolor=color2)

def create_pie_chart(ax, probabilities):
    labels = 'Virtuous', 'Rational', 'Malicious', 'Random'
    # probabilities = (prob_honest, prob_opportunistic, prob_malicious, prob_random)
    ax.pie(probabilities, labels=labels, autopct='%1.1f%%', colors=sns.color_palette('Set2'))

def create_borrower_tokens(ax, interval, borrower_tokens_history):
    interval_sample = borrower_tokens_history[::interval]
    ax.plot(interval_sample, 'm:o', linewidth=0.5, ms = 2)
    ax.set_title('Interval Sample of Tokens History while borrowing')
    ax.set_xlabel('Sample Days')
    ax.set_ylabel('Number of Tokens earned for borrowing')

def create_lender_tokens(ax, interval, lender_tokens_history):
    interval_sample = lender_tokens_history[::interval]
    ax.plot(interval_sample, 'c:o', linewidth=0.5, ms = 2)
    ax.set_title('Interval Sample of Tokens History if lending')
    ax.set_xlabel('Sample Days')
    ax.set_ylabel('Number of Tokens earned for lending')

def create_associations_tokens(ax,associations_tokens):
    colors = {'Library': 'blue', 'Study help': 'green', 'Transportation service': 'red'}
    for key, values in associations_tokens.items():
        ax.plot(values, '*-', label=key, color = colors[key])
    ax.set_xlabel('Number of borrowings', fontsize = 20)
    ax.set_ylabel('Tokens', fontsize = 20)
    ax.set_title('Tokens Over Time for Different Associations', fontsize = 22)
    ax.legend(loc='lower center', bbox_to_anchor=(1.1, 1.05), fontsize = 20)


def create_circulation_tokens(ax, number_tokens_in_circulation, number_tokens_with_burning):
    color_ass = '#990099'
    ax.plot(number_tokens_in_circulation, '*-', color = color_ass)
    ax.set_box_aspect(9/16) #heigth/width
    ax.set_title('Total number of tokens in circulation')
    ax.set_xlabel('Days')
    ax.set_ylabel('Tokens')

    # color_ass2 = '#F9A704'
    # ax2 = ax.twinx()
    # ax2 = ax.twiny()
    # ax2.plot(number_tokens_with_burning, color = color_ass2, linestyle='solid', marker='*')
    # ax2.set_title('Total number of tokens in circulation')
    # ax2.set_xlabel('Days')
    # ax2.set_ylabel('Tokens')
    # ax2.tick_params(axis='y', labelcolor=color_ass2)

    