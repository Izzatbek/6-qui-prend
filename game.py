#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
TODO list:

Test the game for robustness
Score counting and statistics

"""

def construct_card_vals():
    card_vals = [1 for i in range(105)] # Each card has a certain number of points (cattle heads)
    card_vals[0] = 0 # there is no 0-card
    for i in range(11, 105, 11): # 8 cards with 5 cattle heads—the multiples of 11, i.e. 11, 22, 33, and so on through 99
        card_vals[i] = 5
    for i in range(10, 105, 10): # 10 cards with 3 cattle heads—the multiples of ten, i.e. 10, 20, 30, and so through 100
        card_vals[i] = 3
    for i in range(5, 105, 10): # 9 cards with 2 cattle heads—the multiples of five which are not multiples of ten, i.e. 5, 15, 25, and so on through 95
        card_vals[i] = 2
    card_vals[55] = 7 # 1 card with 7 cattle heads—number 55
    return card_vals

def countHeads(card_stack):
    return sum(Game.card_vals[v] for v in card_stack)

def index_difference(list_of_interest, max_card, card):
    return list_of_interest.index(card) - list_of_interest.index(max_card)

class Card:
    # Costs for choose function
    PLAY_NOW = 1
    PLAY_LATER = 2
    CHOOSE_COLUMN = 3
    POTENTIAL_TAKE = 4
    # Costs for try_not_to_take function
    MAX_DIFF = 1
    MIN_COWS = 2

class Game(object):

    card_vals = construct_card_vals()

    def __init__(self, n_players=2, junk=None):
        if not junk:
            junk = set()
        self.junk = junk
        self.n_players = n_players
        self.all_cards = set(range(1, n_players * 10 + 5))

    @property
    def table(self):
        return self._table

    def sort_table(self):
        self._table = sorted(self._table, key=lambda t: max(t))
        self.max_cols = [max(col) for col in self._table]

    @table.setter
    def table(self, table):
        # N of columns must be == 4 and N of cards < 6
        assert(len(table) == 4 and all(len(col) < 6 for col in table))
        self._table = table
        self.sort_table()

    @property
    def hand(self):
        return self._hand

    @hand.setter
    def hand(self, hand):
        assert(len(hand) < 11)
        self._hand = sorted(hand)

    def print_table(self):
        print "The current table is:"
        for i, column in enumerate(self.table):
            print "Column", i + 1, sorted(column)
        print

    def remove_column(self, ind, card):
        assert(ind in range(0, 4))
        self.junk |= self.table[ind]
        self.table[ind] = set([card])

    def find_col_index(self, card):
        cur_col_i = 0
        while cur_col_i < 3 and card > self.max_cols[cur_col_i + 1]:
            cur_col_i += 1
        # the card is smaller than all of last cards
        # -> so, we return None because we cannot
        # place this card without taking a column
        if cur_col_i == 0 and card < self.max_cols[0]:
            return None
        return cur_col_i

    def play(self, played, remove_func):
        # card: chosen card
        # played: all other cards
        self.sort_table()
        played.sort()
        for card in played:
            if card in self.hand:
                self.hand.remove(card)
        for card in played:
            # This calls setter
            cur_col_i = self.find_col_index(card)
            if cur_col_i != None:
                if len(self.table[cur_col_i]) == 5:
                    self.junk |= self.table[cur_col_i]
                    self.table[cur_col_i] = set([card])
                else:
                    self.table[cur_col_i].add(card)
            else:
                self.remove_column(remove_func(self), card)
            self.sort_table()

    def try_not_to_take(self):
        # Another score_dict cost function
        score_dict = {}
        s_interest = self.build_set_of_interest() - set(self.hand)
        col_costs = [countHeads(col) for col in self.table]
        for card in self.hand:
            index = self.find_col_index(card)
            l_interest = sorted(s_interest | set([card]))
            dif = index_difference(l_interest, self.max_cols[index], card)
            # Try to find a card which is higher than the card of an opponent
            if dif > 1: # 1 can be changed
                score_dict[card] = [Card.MAX_DIFF, -dif, card]
            # If not, try to take a column with the minimum number of cows
            else:
                score_dict[card] = [Card.MIN_COWS, col_costs[index], card]
        return min(score_dict, key=score_dict.get)

    def check_first_card(self, threshold):
        opp = sorted(self.all_cards - self.junk - set.union(*self.table) - set(self.hand))
        if opp[0] < self.hand[0] or min(self.max_cols) < self.hand[0]:
            return False
        # You can change this threshold
        return any([countHeads(col) < threshold for col in self.table])

    def build_set_of_interest(self):
        return self.all_cards - set.union(*self.table) - self.junk | set(self.max_cols)

    def can_postpone(self, index, l_interest, card):
        interest_wo_hand = sorted(set(l_interest) - set(self.hand) | set([card]))
        if card != interest_wo_hand[-1]:
            return False
        col_costs = [countHeads(col) for col in self.table]
        return any([cost < col_costs[index] for cost in col_costs])

    def choose(self):
        score_dict = {}
        if self.check_first_card(2):
            return self.hand[0]
        l_interest = sorted(self.build_set_of_interest())
        col_costs = [countHeads(col) for col in self.table]
        for card in self.hand:
            cur_col_i = self.find_col_index(card)
            if cur_col_i != None:
                ind_dif = index_difference(l_interest, self.max_cols[cur_col_i], card)
                # Ranking, the difference with last card of the column, the number of cards in the column
                # cow cost and the card value are added in the cost function.
                score_dict[card] = [Card.PLAY_NOW, ind_dif, -len(self.table[cur_col_i]), -col_costs[cur_col_i], card]

                # Assign higher score to the maximum card which we can play later.
                # Now better to play low value cards, because anyway nobody will take
                # this column and our card will be played to the same place
                if self.can_postpone(cur_col_i, l_interest, card):
                    score_dict[card][0] = Card.PLAY_LATER

                # If the current card put in this column could possibly
                # lead to taking all the cards in the column
                if min(score_dict[card][1], self.n_players) - score_dict[card][2] > 5:
                    score_dict[card][0] = Card.POTENTIAL_TAKE # Change the score to higher
            else:
                # Maybe add another strategy to compute costs like
                # taking into account cow scores?
                interest_wo_hand = sorted(set(l_interest) - set(self.hand) | set([card]))
                dif = index_difference(interest_wo_hand, interest_wo_hand[0], card)
                # Try to find a card which is higher than the card of an opponent
                score_dict[card] = [Card.CHOOSE_COLUMN, -dif, card]

        if all([val[0] == Card.POTENTIAL_TAKE for k, val in score_dict.iteritems()]):
        	return self.try_not_to_take()

        return min(score_dict, key=score_dict.get)
