from game import *
import unittest

class TestGame(unittest.TestCase):
    def setUp(self):
        init_all(set(), 4)

    def test_cows(self):
        self.assertEqual(card_vals[55], 7)

    def test_dif_1_card(self):
        table = [set([4]), set([3]), set([23]), set([40])]
        hand = set([7, 42, 24, 26, 28])
        self.assertEqual(choose(table, hand), 24)
        table = [set([4, 5, 6, 7, 8]), set([3]), set([23, 19, 18, 20, 21]), set([40])]
        hand = set([9, 42, 2, 24, 26, 28])
        self.assertEqual(choose(table, hand), 42)

    def test_choose_column_with_more_cards(self):
        table = [set([4, 5, 6]), set([3]), set([23]), set([40])]
        hand = set([7, 42, 24, 26, 28])
        self.assertEqual(choose(table, hand), 7)

    def test_not_take_full_column(self):
        table = [set([4, 5, 6, 7, 8]), set([3]), set([23, 19, 18, 20, 21]), set([40])]
        hand = set([9, 2])
        self.assertEqual(choose(table, hand), 2)

    def test_try_not_to_take_if_cannot_put_one(self):
        init_all(set(), 2)
        table = [set([1, 2, 3, 4, 5]), set([21, 20, 13, 14, 15]), set([23]), set([24])]
        hand = set([6, 7, 9, 16, 19, 22])
        self.assertEqual(choose(table, hand), 19)

    """
    def test_take_column_with_the_least_cow_score(self):
        init_all(set(range(1, 25)), set([]))
        table = [set([1, 2, 3, 4, 5]), set([21, 20, 13, 14, 15]), set([23]), set([24])]
        hand = set([6, 7, 9, 16, 17, 22])
        self.assertEqual(choose(table, hand), 22)
    """

    def test_diffence_considering_junk_table(self):
        junk = set([8, 9, 10, 11])
        all_cards = set([12, 21, 13, 23, 24, 1, 20, 6, 7]) | junk
        init_all(junk, all_cards_i=all_cards)
        table = [set([6, 7]), set([20]), set([24]), set([1])]
        hand = set([12, 21])
        self.assertEqual(choose(table, hand), 12)

    def test_take_into_account_num_players(self):
        init_all(set(), 3)
        table = [set([8, 12]),set([21]),set([22, 23, 27, 29]), set([24, 25, 33, 34])]
        hand = [16, 19, 20]
        self.assertEqual(choose(table, hand), 16)

    def test_do_not_play_highest(self):
        init_all(set(), 3)
        hand = set([34, 4, 7, 12, 19, 20, 23, 27, 31])
        table = [set([1]), set([18, 21]), set([28]), set([30, 33])]
        self.assertNotEqual(choose(table, hand), 34)
        
        init_all(set([24, 22]), 2)
        hand = set([23, 21, 5])
        table = [set([4]), set([6]), set([19, 20]), set([15])]
        self.assertEqual(choose(table, hand), 5)

    def test_consecutive_taking_cards(self):
        junk = set([23])
        init_all(junk, 2)
        table = [set([1, 2, 3, 4, 5]), set([8, 9, 10, 11, 7]), set([20, 21]), set([22])]
        hand = set([6, 15, 16, 17])
        self.assertEqual(choose(table, hand), 15)

        junk = set([23, 12, 13, 14])
        init_all(junk, 2)
        table = [set([1, 2, 3, 4, 5]), set([8, 9, 10, 11, 7]), set([20, 21]), set([22])]
        hand = set([6, 15, 16, 17])
        self.assertEqual(choose(table, hand), 6)

    def test_consecutive_small_cards(self):
        junk = set([1, 2, 3, 4, 5, 32])
        table = [set([17, 24]), set([18, 21, 22, 23, 25]), set([28, 29, 31]), set([30, 33, 34])]
        hand = set([7, 12, 19, 20, 27])
        init_all(junk, 3)
        self.assertNotEqual(choose(table, hand), 20)


if __name__ == '__main__':
    unittest.main()

"""
hand = set([5, 6, 10])
#hand = set([9, 11, 7])
table = [set([1, 2, 3, 4, 8]), set([22, 23, 24]), set([12, 13, 14, 16, 17]), set([15, 18, 19, 20, 21])]
junk = set([])
all_cards = set(range(1, 25))
print choose(table, hand)
"""