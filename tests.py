#!/usr/bin/env python
# -*- coding: utf-8 -*-

from game import Game
import unittest

class TestGame(unittest.TestCase):

    def test_cows(self):
        self.assertEqual(Game.card_vals[55], 7)

    def test_dif_1_card(self):
        game = Game(4)
        game.table = [set([4]), set([3]), set([23]), set([40])]
        game.hand = set([7, 42, 24, 26, 28])
        self.assertEqual(game.choose(), 24)
        game.table = [set([4, 5, 6, 7, 8]), set([3]), set([23, 19, 18, 20, 21]), set([40])]
        game.hand = set([9, 42, 2, 24, 26, 28])
        self.assertEqual(game.choose(), 42)

    def test_choose_column_with_more_cards(self):
        game = Game(4)
        game.table = [set([4, 5, 6]), set([3]), set([23]), set([40])]
        game.hand = set([7, 42, 24, 26, 28])
        self.assertEqual(game.choose(), 7)

    def test_not_take_full_column(self):
        game = Game(4)
        game.table = [set([4, 5, 6, 7, 8]), set([3]), set([23, 19, 18, 20, 21]), set([40])]
        game.hand = set([9, 2])
        self.assertEqual(game.choose(), 2)

    def test_try_not_to_take_if_cannot_put_one(self):
        game = Game(2)
        game.table = [set([1, 2, 3, 4, 5]), set([21, 20, 13, 14, 15]), set([23]), set([24])]
        game.hand = set([6, 7, 9, 16, 19, 22])
        self.assertEqual(game.choose(), 19)

    def test_diffence_considering_junk_table(self):
        game = Game(4)
        game.junk = set([8, 9, 10, 11])
        game.all_cards = set([12, 21, 13, 23, 24, 1, 20, 6, 7]) | game.junk
        game.table = [set([6, 7]), set([20]), set([24]), set([1])]
        game.hand = set([12, 21])
        self.assertEqual(game.choose(), 12)

    def test_take_into_account_num_players(self):
        game = Game(3)
        game.table = [set([8, 12]),set([21]),set([22, 23, 27, 29]), set([24, 25, 33, 34])]
        game.hand = [16, 19, 20]
        self.assertEqual(game.choose(), 16)

    def test_do_not_play_highest(self):
        game = Game(3)
        game.hand = set([34, 4, 7, 12, 19, 20, 23, 27, 31])
        game.table = [set([1]), set([18, 21]), set([28]), set([30, 33])]
        self.assertNotEqual(game.choose(), 34)
        
        game = Game(2, set([24, 22]))
        game.hand = set([23, 21, 5])
        game.table = [set([4]), set([6]), set([19, 20]), set([15])]
        self.assertEqual(game.choose(), 5)

    def test_consecutive_taking_cards(self):
        game = Game(2, junk=set([23]))
        game.table = [set([1, 2, 3, 4, 5]), set([8, 9, 10, 11, 7]), set([20, 21]), set([22])]
        game.hand = set([6, 15, 16, 17])
        self.assertEqual(game.choose(), 15)

        game.junk = set([23, 12, 13, 14])
        game.table = [set([1, 2, 3, 4, 5]), set([8, 9, 10, 11, 7]), set([20, 21]), set([22])]
        game.hand = set([6, 15, 16, 17])
        self.assertEqual(game.choose(), 6)
    
    def test_consecutive_small_cards(self):
        game = Game(3, junk=set([1, 2, 3, 4, 5, 32]))
        game.table = [set([17, 24]), set([18, 21, 22, 23, 25]), set([28, 29, 31]), set([30, 33, 34])]
        game.hand = set([7, 12, 19, 20, 27])
        self.assertNotEqual(game.choose(), 20)

    def test_good_tie_cards(self):
        game = Game(6)
        game.table = [set([3, 6, 10]), set([36, 60]), set([12, 13]), set([5, 23])]
        game.hand = set([26, 16])
        self.assertEqual(game.choose(), 26)

        game.table = [set([3, 6, 10]), set([36, 60]), set([12, 13]), set([6, 23])]
        game.hand = set([26, 16])
        self.assertEqual(game.choose(), 16)

    """
    def test_hope_for_opponents_mistake(self):
        game = Game(2, junk=set([4]))
        game.table = [set([5, 6, 7, 8, 9]), set([23]), set([1, 2, 3]), set([11, 12, 13, 14])]
        game.hand = [10, 16, 17, 21, 22]
        self.assertEqual(game.choose(), 16)
    """

if __name__ == '__main__':
    unittest.main()