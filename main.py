#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pprint import pprint
from game import Game

def verify_table(game, table):
    if len(table) != 4:
        print "The number of columns must be equal to 4"
        return False
    table_set = set.union(*table)
    if len(table_set) != 4:
        print "All cards must be unique"
        return False
    for e in table_set:
        if not e in game.all_cards:
            print "All cards must be between 1 and", len(game.all_cards)
            return False
    return True

def verify_hand(game, hand):
    table_set = set.union(*game.table)
    for card in hand:
        if not card in game.all_cards:
            print game.all_cards
            print "All cards must be between 1 and", len(game.all_cards)
            return False
    if len(table_set & hand) > 0:
        print "All cards must be unique"
        return False
    return True

def start():
    print("------ 6 qui prend ------")
    n_players = int(raw_input("Please define the number of players: "))
    game = Game(n_players)
    while True:
        in_cards = raw_input("Please define the cards on the table separating by space: ")
        table = [set([int(i)]) for i in in_cards.split()]
        if verify_table(game, table):
            break
    game.table = table
    hand = set()
    while True:
        in_cards = raw_input("Define cards in your hand: ")
        hand |= set(int(i) for i in in_cards.split())
        if verify_hand(game, hand):
            break
    game.hand = hand
    return game

def choose_card(game):
    game.print_table()
    while True:
        ind = int(raw_input("Please choose a column to take: ")) - 1
        if ind in range(0, 4):
            break
    return ind

def main():
    game = start()

    while (len(game.hand) > 0):
        best = game.choose()
        print "The best card to choose is", best
        print
        played_input = raw_input("Please define the played cards separating by space: ")
        played = [int(i) for i in played_input.split()]
        game.play(played, choose_card)
        print "Current hand and table: ", game.hand
        pprint(game.table)

if __name__ == '__main__':
    main()