import numpy as np
import random
import matplotlib.pyplot as plt
from utils import *
from stats import *
from chart import *
from constants import *
from parameters import *

#==================== SIMULATION ======================================

def main():

    #============ CLI ===================================================================
    # global num_players
    # input_num_players = input(f"Enter value for the number of community participants: ")
    # num_players = int(input_num_players) if input_num_players else num_players

    # associations = {}
    # new_assoc = ask_yes_no_question("Do you want to add an association?")
    # while new_assoc:
    #     input_name_assoc = input(f"What is its name?: ")
    #     input_crowdfunding = input(f"How many crodwfunding tokens? (Put 0 if any): ")
    #     num_services = int(input(f"How many services does it offer? (Put 0 if any): "))
    #     add_association(input_name_assoc, input_crowdfunding, associations, num_services)
    #     new_assoc = ask_yes_no_question("Do you want to add an association?")
    # if new_assoc == False:
    #     print("No other associations have been added")        

    #TODO add rental mechanism
    


    outer_break = False

    wallet_balance_history = []
    exchanged_tokens_history = []
    exchanged_tokens_temp = 0

    current_lender_temp = Person(name='', behavior_lending='',behavior_borrowing='', tokens=0)

    borrower_tokens_history = []
    lender_tokens_history = []
    tokens_associations_history = []
    number_tokens_in_circulation = []
    number_tokens_with_burning = [] 

    num_borrowings = 0
    num_returnings = 0

    borrowable_objects_history = []
    num_remaining_borrowable_objects = 0

    players, behavior_lender_count, behavior_borrower_count = initialize_players(num_players, probabilities, n_token_init)

    showcase = create_showcase(players, associations, payoffs_reward)
    
    associations_tokens = {
        'Library': [],
        'Study help': [],
        'Transportation service': []
    }

    for i in range(max_rounds):
        num_remaining_borrowable_objects = 0

        players_order = random.sample(list(players.values()), k=num_players)

        for j in range(len(players_order)):
    
            current_borrower = players_order[j]
            current_borrower_choice = choose_objects(showcase, current_borrower, prob) #type OwnedItems() || None
            
            if current_borrower_choice != None:
                ndays = random.randint(2,5)
                payoffs_days['lender'] = np.array([ndays,0,0])
                utility["lender"]["opportunistic"] = generate_opportunistic_utility(payoffs_days['lender'])
                lender_choice_index = borrowing_an_item(current_borrower_choice, utility, players, associations, current_borrower, ndays)

                if lender_choice_index == 0 or lender_choice_index == 1:
                    num_borrowings += 1

            if current_borrower.objects_borrowing != []:
                for item in current_borrower.objects_borrowing:   
                    
                    payoffs_days['borrower'] = np.array([-item.days,0,0])
                    utility["borrower"]["opportunistic"] = generate_opportunistic_utility(payoffs_days['borrower'])

                    if item.remaining_days > 1:
                        item.remaining_days -= 1
                    else:
                        object_to_return = item
                        [current_lender, exchanged_tokens, is_returned]= returning_an_item(players, current_borrower, utility, payoffs_reward, object_to_return, associations) 
                        
                        if is_returned:
                            num_returnings += 1
                            borrower_tokens_history.append(-object_to_return.days + payoffs_reward['borrower'][0])
                            lender_tokens_history.append(object_to_return.days + payoffs_reward["lender"][0])

                        else:
                            borrower_tokens_history.append(-object_to_return.days)
                            lender_tokens_history.append(object_to_return.days)
                        
                        exchanged_tokens_temp += exchanged_tokens 
                        current_lender_temp = current_lender         
    
        if any (ass == current_lender_temp for ass in associations.values()):
            tokens_associations_history.append(current_lender_temp.tokens)

        for key, ass in associations.items():
            if ass == current_lender_temp:
                associations_tokens[key].append(current_lender_temp.tokens)
            else:
                associations_tokens[key].append(0)
        
        exchanged_tokens_history.append(exchanged_tokens_temp) 
        for o in showcase.values():
            is_borrowable = o.borrower == ""
            o_owner = o.owner
            if any (p.name == o_owner for p in players.values()):
                lender_utility = utility["lender"][players[o_owner].behavior_lending]
                lender_utility_index = lender_utility.index(3)
            else:
                lender_utility_index = 0 # because associations always lend their objects
                
            if lender_utility_index != 2 and is_borrowable:
                num_remaining_borrowable_objects += 1 # only the values at the last day
        
        borrowable_objects_history.append(num_remaining_borrowable_objects)

        total_tokens_associations = sum(int(ass.tokens) for ass in associations.values())
        total_tokens_players = sum(p.tokens for p in players.values())
        total_tokens = total_tokens_associations + total_tokens_players

        number_tokens_in_circulation.append(total_tokens)
        # number_tokens_with_burning.append(total_tokens)

        # #burning function try
        # if total_tokens > 50*(num_players + len(associations.values())): 
        #     number_tokens_with_burning.append(total_tokens*0.8)

        if outer_break:
            break


    #=========== STATISTICS ================

    statistics_behaviors = calculate_behavior_statistics(players)
    statistic_lenders = calculate_lender_statistics(players)
    statistic_borrowers = calculate_borrower_statistics(players)

    #==================== PLOT=====================

    #------------ First plot: bar chart statistics----------------------

    fig, axs = plt.subplots(2, 4, figsize=(20,10),gridspec_kw={'width_ratios': [3, 3, 1, 2]})

    create_boxplot_statistics(axs[0,0], axs[0,1], statistic_lenders, statistic_borrowers)

    fig3, axs3 = plt.subplots(figsize = (10,10))

    create_tokens_exchanged_graph(axs3, exchanged_tokens_history, borrowable_objects_history)

    # == Description of the simulation in the plot ==
    # Mean of objects owned by players
    total_objects = 0
    for player in players.values():
        total_objects += len(player.objects)  
    mean_objects = total_objects / len(players) if players else 0
    # Constructing the description text
    description_text = ""
    # description_text += f"\nAssociations:{len(COSO.objects)}\n Players' objects mean: {mean_objects}\n Days: {max_rounds}\n Borrowings: {num_borrowings}, \n Returnings: {num_returnings} over total {len(showcase)} objects\n Borrowables at the last day: {num_remaining_borrowable_objects} \n when  borrowing probability is {prob*100}% \n\n   "
    # Pie chart social distribution
    axs[0, 3] = create_pie_chart(axs[0, 3], probabilities)
    description_social = f"Players: {num_players}\n\n"
    description_social += "Lenders:\n"
    for behavior_lender, count in behavior_lender_count.items():
        description_social += f"{behavior_lender}: {count}\n"

    description_social += "\nBorrowers:\n"
    for behavior_borrower, count in behavior_borrower_count.items():
        description_social += f"{behavior_borrower}: {count}\n"

    description_social += f"\n Payoffs reward:\n Borrower: {payoffs_reward['borrower']}\n Lender: {payoffs_reward['lender']}"

    axs[0, 2].text(0.5, 0.5, description_social, ha='center', va='center', fontsize=10, transform=axs[0, 2].transAxes)
    axs[0, 2].axis('off')  # Optionally turn off the axis if it's just text


    # Add the description text to the subplot (for example, the third subplot)
    axs[1, 2].text(0.5, 0.5, description_text, ha='center', va='center', fontsize=10, transform=axs[1, 2].transAxes)
    axs[1, 2].axis('off')  # Optionally turn off the axis if it's just text

    create_circulation_tokens(axs[1,3],number_tokens_in_circulation, number_tokens_with_burning)

    #------------ Second plot: associations--------------------------
    fig2, axs2 = plt.subplots()
    create_associations_tokens(axs2,associations_tokens)

    # Adjust layout
    plt.tight_layout()

    # Save the entire figure
    plt.savefig(f'img/Simulation-{date_time}.jpg')

    # Show the plot
    plt.show()


if __name__ == "__main__":
    main()