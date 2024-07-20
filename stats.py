def _update_statistics(statistics, key, value):

    if key in statistics:
        statistics[key].append(value)
    else:
        statistics[key] = [value]

def calculate_behavior_statistics(players):
    statistics_behaviors = {}
    for p in players.values():
        beh = f"L = {p.behavior_lending}, B = {p.behavior_borrowing}"
        _update_statistics(statistics_behaviors, beh, p.tokens)
    return statistics_behaviors

def calculate_lender_statistics(players):
    statistic_lenders = {}
    for p in players.values():
        beh = f"L = {p.behavior_lending}"
        _update_statistics(statistic_lenders, beh, p.tokens_as_lender)
    return statistic_lenders

def calculate_borrower_statistics(players):
    statistic_borrowers = {}
    for p in players.values():
        beh = f"B = {p.behavior_borrowing}"
        _update_statistics(statistic_borrowers, beh, p.tokens_as_borrower)
    return statistic_borrowers
