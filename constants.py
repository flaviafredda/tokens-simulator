import numpy as np
from datetime import datetime
from parameters import *
from utils import *

date_time = datetime.now().strftime("%Y-%m-%d--%H.%M.%S.%f")

#TOKENS PRESTITO 
payoffs_borrowing = { #"tokens noleggio"
    "lender": np.array([1, 0, 0]) , 
    "borrower": np.array([-1, 0, 0]) 
}

#TOKENS TOTALI
payoffs_days = {
    "lender": payoffs_reward["lender"]+ payoffs_borrowing["lender"] , 
    "borrower": payoffs_reward["borrower"]+ payoffs_borrowing["borrower"]
}

utility = {
    "lender" : {
        "honest": [3, 2, 1],
        "random": random.sample([1,2,3], 3),
        "malicious": [1, 2, 3],
        "opportunistic": generate_opportunistic_utility(payoffs_days["lender"])
    },
    "borrower" : {
        "honest": [3, 2, 1],
        "random": random.sample([1,2,3], 3),
        "malicious": [1, 3, 2],
        "opportunistic": generate_opportunistic_utility(payoffs_days["borrower"])
    }
}




