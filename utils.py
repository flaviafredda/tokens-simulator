import random
import string
import numpy as np
import sys


class OwnedItems:
    def __init__(self, name, nameOwner, value=0):
        self._name = name
        self._value = value
        self._state = "owned"  # owned or borrowed or pending
        self._owner = nameOwner
        self._borrower = ""
        self._days = 0
        self._remaining_days = 0

    # Getter for 'name'
    @property
    def name(self):
        return self._name

    # Getter and setter for 'value'
    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        if isinstance(value, (int, float)) and value >= 0:  # Ensure the value is non-negative
            self._value = value
        else:
            raise ValueError("Value must be a non-negative number")

    @property
    def days(self):
        return self._days
    
    @days.setter
    def days(self,days):
        self._days = days

    @property
    def remaining_days(self):
        return self._remaining_days
    
    @remaining_days.setter
    def remaining_days(self,remaining_days):
        self._remaining_days = remaining_days

    # Getter and setter for 'state'
    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, state_str):
        valid_transitions = {
        "owned": ["pending"],  # From 'owned', it can only change to 'pending'
        "pending": ["owned", "borrowed"],  # From 'pending', it can change to 'owned' or 'borrowed'
        "borrowed": ["owned"]  # From 'borrowed', it can only change to 'owned'
        }

        if self._state not in valid_transitions:
            raise ValueError(f"Current state '{self._state}' is not a valid state.")

        if state_str not in ["owned", "borrowed", "pending"]:
            raise ValueError("State must be either 'owned', 'borrowed', or 'pending'.")

        if state_str not in valid_transitions[self._state]:
            raise ValueError(f"Invalid state transition from '{self._state}' to '{state_str}'.")

        self._state = state_str

    # Getter and setter for 'borrower'
    @property
    def borrower(self):
        return self._borrower

    @borrower.setter
    def borrower(self, borrower_name):
        if isinstance(borrower_name, str):
            self._borrower = borrower_name
        else:
            raise ValueError("Borrower name must be a string")

    # Getter for 'owner'
    @property
    def owner(self):
        return self._owner


#Random string generator
def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
        return ''.join(random.choice(chars) for _ in range(size))


#======================  PLAYERS ==================================
class Person:
    def __init__(self, name, behavior_lending, behavior_borrowing, tokens):
        self._name = name 
        self._behavior_lending = behavior_lending
        self._behavior_borrowing = behavior_borrowing
        self._state = ""
        self._tokens = tokens
        self._tokens_as_borrower = 0
        self._tokens_as_lender = 0
        self._lockedTokens = 0
        self._objects = []
        self._objects_borrowing = []
    
    @property
    def name(self):
        return self._name

    @property
    def objects(self):
        return self._objects
    
    @property
    def behavior_lending(self):
        return self._behavior_lending
    
    @property
    def behavior_borrowing(self):
        return self._behavior_borrowing
    
    @property
    def state(self):
        return self._state
    
    @state.setter
    def state(self,state):
        self._state = state

    @property
    def tokens(self):
        return self._tokens

    @tokens.setter
    def tokens(self,tokens):
        self._tokens = tokens
    
    @property
    def tokens_as_borrower(self):
        return self._tokens_as_borrower

    @tokens_as_borrower.setter
    def tokens_as_borrower(self,tokens_as_borrower):
        self._tokens_as_borrower = tokens_as_borrower

    @property
    def tokens_as_lender(self):
        return self._tokens_as_lender

    @tokens_as_lender.setter
    def tokens_as_lender(self,tokens_as_lender):
        self._tokens_as_lender = tokens_as_lender
    
    @property
    def lockedTokens(self):
        return self._lockedTokens
    
    @lockedTokens.setter
    def lockedTokens(self,lockedTokens):
        self._lockedTokens = lockedTokens

    @property
    def objects_borrowing(self):
        return self._objects_borrowing

    @objects_borrowing.setter
    def objects_borrowing(self,objects_borrowed):
        self._objects_borrowing.append(objects_borrowed)

    @property
    def person(self):
        return f"Person {self._name}\t has behavoir lending {self._behavior_lending},\t behavior borrowing {self._behavior_borrowing}\t and have currently {self._tokens} tokens."

    def createRandomObjects(self,num_objects):
        for i in range(num_objects):
            name_obj = id_generator()
            self._objects.append(OwnedItems(name_obj, self._name, value=1))
    
    def is_borrowing(self):
        return self._objects_borrowing != [] and len(self._objects_borrowing) != 0


#==================== SHOWCASE ===================================
def create_showcase(players: dict, associations: dict, payoffs_reward) -> dict:

    items = {}
    for person_id, person in players.items():
        if not isinstance(person, Person):
            raise ValueError(f"The player with ID {person_id} is not an instance of Person")
        for item in person.objects:
            if hasattr(item, 'name'):
                items[item.name] = item
                person.tokens += payoffs_reward["lender"][0]
                person.tokens_as_lender += payoffs_reward["lender"][0]
            else:
                raise AttributeError(f"The item {item} does not have a 'name' attribute")

    for ass_id, ass in associations.items():
        if not isinstance(ass, Person):
            raise ValueError(f"The association with ID {ass_id} is not an instance of Person")
        for item in ass.objects:
            if hasattr(item, 'name'):
                    items[item.name] = item
                    # ass.tokens = int(ass.tokens) - payoffs_reward["lender"][0]
            else:
                raise AttributeError(f"The item {item} does not have a 'name' attribute")
            
    return items

def choose_objects(showcase: dict, borrower: Person, prob): #-> OwnedItems | None: #without "borrower" lenders play alone and earn millions of tokens
    do_borrow = random.random() <= prob
    object_chosen = random.choice(list(showcase.values()))
    is_available = object_chosen.state == "owned" or object_chosen.borrower == ""

    if is_available and do_borrow:
        object_chosen.state = "pending"
        object_chosen.borrower = borrower.name
        return object_chosen
    else:
        return None

def lock_tokens(borrower: Person, ndays):
    if borrower.tokens >= ndays:
        borrower.tokens -= ndays
        borrower.lockedTokens += ndays
    else:
       print(f'Not enough tokens to lock for borrower {borrower.name} which had {borrower.tokens} tokens but wanted {ndays} days')

def borrowing_an_item(current_borrower_choice, utility, players, associations, current_borrower, ndays):
    if current_borrower_choice != None:
            lender_choice_index = negotiation(utility, current_borrower_choice, current_borrower, ndays, players, associations)
            #according to lender's choice, the item can be borrowed or not

            current_borrower_choice_state = current_borrower_choice.state

            if current_borrower_choice_state == "borrowed":
                #the item adds to the already borrowed objects
                current_borrower.objects_borrowing.append(current_borrower_choice)
    return lender_choice_index


def returning_an_item(players, current_borrower, utility, payoffs_reward, object_to_return, associations):
    is_returned = False
    lender_name = object_to_return.owner
    current_lender = find_person_by_name(lender_name, players, associations)
    exchanged_tokens = 0
    borrower_utility = []
    borrower_utility_index = 5

    if current_borrower.is_borrowing():
            
        if current_borrower.behavior_borrowing == "random":
            borrower_utility = random.sample([1,2,3], 3)
            # print(f"Random utility for borrower {current_borrower.name} is: {borrower_utility}")
        else:
            borrower_utility = utility["borrower"][current_borrower.behavior_borrowing]
        
        try:
            borrower_utility_index = borrower_utility.index(3)
        except ValueError:
            print(f"error! borrow utility: {borrower_utility}")

        if borrower_utility_index == 0:
            #the item will be returned
            object_to_return.state = "owned" #returned object
            object_to_return.remaining_days = 0
            object_to_return.days = 0
            object_to_return.borrower = ""

            current_borrower.lockedTokens -= object_to_return.days
            current_borrower.tokens_as_borrower -= object_to_return.days

            current_borrower.tokens += payoffs_reward["borrower"][0]
            current_borrower.tokens_as_borrower += payoffs_reward["borrower"][0]
            
            current_borrower.objects_borrowing.remove(object_to_return) 
            
            current_lender.tokens += payoffs_reward["lender"][0] + object_to_return.days 
            
            current_lender.tokens_as_lender += payoffs_reward["lender"][0] + object_to_return.days 

            exchanged_tokens = object_to_return.days + payoffs_reward["lender"][0]+payoffs_reward["borrower"][0]
            is_returned = True
        else:
            current_lender.tokens += object_to_return.days # we assume that the smart contract unlocks the tokens anyway
            current_lender.tokens_as_lender += object_to_return.days # we assume that the smart contract unlocks the tokens anyway
        
    return current_lender, exchanged_tokens, is_returned

def negotiation(utility, chosen_object, borrower: Person, ndays, players, associations: dict):
    assert chosen_object.state == 'pending'
    if any (p.name == chosen_object.owner for p in players.values()):
        owner = players[chosen_object.owner]
    else:
        if any (ass.name == chosen_object.owner for ass in associations.values()):
            owner = associations[chosen_object.owner]

    behavior_as_lender = owner.behavior_lending
    # if behavior_as_lender == 'malicious':
        # print(f"Malicious lender {owner.name} has {owner.tokens} tokens")
    
    if behavior_as_lender == "random":
        behavior = random.sample([1,2,3], 3)
    else:
        behavior = utility["lender"][behavior_as_lender]

    lender_choice_index = behavior.index(3)
    if (lender_choice_index == 0 or lender_choice_index == 1): #perché il secondo elemento è comunque lend
        chosen_object.state ="borrowed" 
        chosen_object.borrower = borrower.name 
        if borrower.tokens > ndays:
            chosen_object.days = ndays
            chosen_object.remaining_days = ndays
            lock_tokens(borrower, ndays)
        else:
            chosen_object.days = borrower.tokens
            chosen_object.remaining_days = borrower.tokens
            lock_tokens(borrower, borrower.tokens)
    else: 
        chosen_object.state ="owned"
        chosen_object.borrower=""
    
    return lender_choice_index


def generate_opportunistic_utility(payoffs):
    U = [0] * len(payoffs)
    sorted_indices = np.argsort(payoffs)  # Indices of elements sorted in ascending order

    if payoffs[0] > 0:
        if payoffs[-2] == payoffs[-1]:
            sorted_indices[-3], sorted_indices[-2] = sorted_indices[-2], sorted_indices[-3]
    elif payoffs[0] < 0:
        if payoffs[-2] == payoffs[-1]:
            sorted_indices[-2], sorted_indices[-1] = sorted_indices[-1], sorted_indices[-2]
    rank = 1
    for index in sorted_indices:
        U[index] = rank
        rank += 1

    return U

behaviors = ["honest", "opportunistic", "malicious", "random"]

def initialize_players(num_players, probabilities, n_token_init):
    # behaviors = ["honest", "opportunsitic", "malicious", "random"]
    behavior_lender_count = {"malicious": 0, "honest": 0, "opportunistic": 0, "random": 0}
    behavior_borrower_count = {"malicious": 0, "honest": 0, "opportunistic": 0, "random": 0}
    
    players = {}
    for i in range(1, num_players + 1):
        # Random choice of behavior
        player_behavior = random.choices(behaviors, weights=probabilities, k=2)
        
        # Counting the behaviors
        behavior_lender_count[player_behavior[0]] += 1
        behavior_borrower_count[player_behavior[1]] += 1

        name = id_generator(10)
        p = Person(name, behavior_lending = player_behavior[0], behavior_borrowing = player_behavior[1], tokens = n_token_init)
        p.createRandomObjects(random.randint(0,3))
        players[p.name] = p

    return players, behavior_lender_count, behavior_borrower_count

def add_association(input_name_assoc, input_crowdfunding, associations, num_objects):
    assoc_new = Person(name=input_name_assoc, behavior_lending='honest',behavior_borrowing='', tokens=input_crowdfunding)
    assoc_new.createRandomObjects(num_objects)
    associations[assoc_new.name] = assoc_new


def find_person_by_name(name, players, associations):
    if any (ass.name == name for ass in associations.values()):
        return associations[name]
    else:
        if any (p.name == name for p in players.values()):
            return players[name]

def ask_yes_no_question(prompt):
    while True:
        answer = input(prompt + " (yes/no): ").strip().lower()
        if answer == 'yes':
            return True
        elif answer == 'no':
            return False
        else:
            print("Please enter 'yes' or 'no'.")

