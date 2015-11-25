#!/usr/bin/env python
# -*- coding: utf-8 -*-

import operator
from pprint import pprint

card_vals = []
junk = set()

"""
TODO list:
1. Test the game for robustness
2. Resolve all problems for the test cases
3. Write enum for scoring
4. Implement better scoring for small cards
5. Separate UI and logic
6. Maybe rewrite in OOP fashion (not sure if it's worth it)
"""

def print_table(table):
    print "The current table is:"
    for i, column in enumerate(table):
        print "Column", i + 1, sorted(column)
    print

def sort_table(table):
    table = sorted(table, key=lambda t: max(t))
    max_cols = [max(col) for col in table]
    return table, max_cols

def remove_column(table, card):
    """ FIXME Check the index before the call move it to another function
    """
    global junk
    print_table(table)
    while True:
        ind = int(raw_input("Please choose a column to take: ")) - 1
        if ind in range(0, 4):
            break
    junk |= table[ind]
    table[ind] = set([card])
    return table

def find_best_index(table, max_cols, card):
    cur_col_i = 0
    #import IPython;IPython.embed()
    while cur_col_i < 3 and card > max_cols[cur_col_i + 1]:
        cur_col_i += 1
    # the card is smaller than all of last cards
    # -> so, we return None because we cannot
    # place this card without taking a column
    if cur_col_i == 0 and card < max_cols[0]:
        return None
    return cur_col_i

def play(table, hand, card, played):
    """
    card: chosen card
    played: all other cards
    """
    global junk
    played = sorted(set(played) | set([card]))
    hand.discard(card)
    table, max_cols = sort_table(table)
    for c in played:
        cur_col_i = find_best_index(table, max_cols, c)
        if cur_col_i != None:
            if len(table[cur_col_i]) == 5:
                junk |= table[cur_col_i]
                table[cur_col_i] = set([c])
            else:
                table[cur_col_i].add(c)
        else:
            table = remove_column(table, c)
        table, max_cols = sort_table(table)
        print table
    return table, hand

def construct_card_vals():
    global card_vals
    card_vals = [1 for i in range(105)] # Each card has a certain number of points (cattle heads)
    card_vals[0] = 0 # there is no 0-card
    for i in range(11, 105, 11): # 8 cards with 5 cattle heads—the multiples of 11, i.e. 11, 22, 33, and so on through 99
        card_vals[i] = 5
    for i in range(10, 105, 10): # 10 cards with 3 cattle heads—the multiples of ten, i.e. 10, 20, 30, and so through 100
        card_vals[i] = 3
    for i in range(5, 105, 10): # 9 cards with 2 cattle heads—the multiples of five which are not multiples of ten, i.e. 5, 15, 25, and so on through 95
        card_vals[i] = 2
    card_vals[55] = 7 # 1 card with 7 cattle heads—number 55

construct_card_vals()

def countHeads(card_stack):
    return sum(card_vals[v] for v in card_stack)

def try_not_to_take(table, hand, score_dict):
    print_table(table)
    print(hand)
    print(all_cards)
    opp_set = all_cards - set.union(*table) - set(hand) - junk
    max_dif_card = max(score_dict, key=score_dict.get)
    # Tries to play last
    if any([max_dif_card > i for i in opp_set]):
        return max_dif_card
    # We take anyway, try to choose the column with the minimum number of cows
    else:
        # cost of each column on the table (cow cost)
        col_costs = (countHeads(col) for col in table)
        # minimum column cost
        min_cost = min(col_costs)
        # cost for each card
        card_costs = []
        for card in hand:
            index = find_best_index(card)
            # Append tuple with cost and the card
            if index != None:
                card_costs.append((col_costs[index], card))
            else:
                card_costs.append((min_cost, card))
        return min(costs, key=lambda x: x[0])[1] # Check this

def check_first_card(table, hand, max_cols, threshold):
    opp = sorted(all_cards - junk - set.union(*table) - set(hand))
    if opp[0] < hand[0] or min(max_cols) < hand[0]:
        return False
    # You can change this threshold
    return any([countHeads(col) < threshold for col in table])

def build_set_of_interest(table, max_cols):
    global all_cards, junk
    return all_cards - set.union(*table) - junk | set(max_cols)

def index_difference(list_of_interest, max_card, card):
    return list_of_interest.index(card) - list_of_interest.index(max_card)

def can_postpone(table, index, l_interest, hand, card):
    interest_wo_my_cards = sorted(set(l_interest) - set(hand) | set([card]))
    if card != interest_wo_my_cards[-1]:
        return False
    col_costs = [countHeads(col) for col in table]
    return any([cost < col_costs[index] for cost in col_costs])

def choose(table, hand):
    score_dict = {}
    table, max_cols = sort_table(table)
    hand = sorted(hand)
    #import IPython;IPython.embed()
    if check_first_card(table, hand, max_cols, 2):
        return hand[0]
    l_interest = sorted(build_set_of_interest(table, max_cols))
    for card in hand:
        cur_col_i = find_best_index(table, max_cols, card)
        if cur_col_i != None:
            ind_dif = index_difference(l_interest, max_cols[cur_col_i], card)
            # Ranking, the difference with last card of the column, the number of cards in the column
            score_dict[card] = [1, ind_dif, -len(table[cur_col_i])]

            # Assign higher score to the maximum card which we can play later.
            # Now better to play low value cards, because anyway nobody will take
            # this column and our card will be played to the same place
            if can_postpone(table, cur_col_i, l_interest, hand, card):
                score_dict[card][0] = 2

            # If the current card put in this column could possibly
            # lead to taking all the cards in the column
            if min(score_dict[card][1], n_players) - score_dict[card][2] > 5:
                score_dict[card][0] = 5 # Change the score to higher
        else:
            # TODO compute the best policy for small cards
            # Implement two different strategies:
            # 1) Take the minimmum and you are almost sure that you will take a column
            # Take a look at the minimum number of cows in any column
            # 2) Take the maximum card (but minimum in a sequence)
            # Example: 7, 12, 19, 20, take 19
            # Make thrshold for the strategies 
            score_dict[card] = [3, 0, 0]
    pprint(score_dict)
    if all([val[0] == 5 for k, val in score_dict.iteritems()]):
    	return try_not_to_take(table, hand, score_dict)
    return min(score_dict, key=score_dict.get)

def verify_table(table):
    if len(table) != 4:
        print "The number of columns must be equal to 4"
        return False
    table_set = set.union(*table)
    if len(table_set) != 4:
        print "All cards must be unique"
        return False
    for e in table_set:
        if not e in all_cards:
            print "All cards must be between 1 and", len(all_cards)
            return False
    return True

def verify_hand(table, hand):
    table_set = set.union(*table)
    print table_set
    print hand
    for card in hand:
        if not card in all_cards:
            print "All cards must be between 1 and", len(all_cards)
            return False
    if len(table_set & hand) > 0:
        print "All cards must be unique"
        return False
    return True

def start():
    global n_players, all_cards
    print("------ 6 qui prend ------")
    n_players = int(raw_input("Please define the number of players: "))
    all_cards = set(range(1, 10 * n_players + 5)) # pro version
    while True:
        in_cards = raw_input("Please define the initial cards separating by space: ")
        table = [set([int(i)]) for i in in_cards.split()]
        if verify_table(table):
            break
    hand = set()
    while True:
        in_cards = raw_input("Define cards in your hand: ")
        hand |= set(int(i) for i in in_cards.split())
        if verify_hand(table, hand):
            break
    return table, hand

def init_all(junk_i, n_players_i=None, all_cards_i=None):
    global all_cards, junk, n_players
    if not (n_players_i or all_cards_i):
        print "Please define n_players or all_cards"
    if not n_players_i:
        all_cards = all_cards_i
        n_players = len(all_cards) // 10
    if not all_cards_i:
        n_players = n_players_i
        all_cards = set(range(1, n_players * 10 + 5))
    junk = junk_i

def main():
    table, hand = start()

    while (len(hand) > 0):
        best = choose(table, hand)
        print "The best card to choose is", best
        played_input = raw_input("Please define the played cards separating by space: ")
        played = [int(i) for i in played_input.split()]
        table, hand = play(table, hand, best, played)
        print "Current hand: ", hand

if __name__ == '__main__':
    main()