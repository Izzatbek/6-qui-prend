from game import *
import unittest

class TestGame(unittest.TestCase):

    def setUp(self):
        init_all(set(range(1, 45)), set([]))

    def test_cows(self):
        global card_vals
        print card_vals
        self.assertEqual(card_vals[55], 7)

    def test_dif_1_card(self):
        table = [set([4]), set([3]), set([23]), set([40])]
        hand = set([7, 42, 24, 26, 28])
        self.assertEqual(choose(table, hand), 24)

    def test_choose_column_with_more_cards(self):
        table = [set([4, 5, 6]), set([3]), set([23]), set([40])]
        hand = set([7, 42, 24, 26, 28])
        self.assertEqual(choose(table, hand), 7)

    def test_dif_1_card2(self):
        table = [set([4, 5, 6, 7, 8]), set([3]), set([23, 19, 18, 20, 21]), set([40])]
        hand = set([9, 42, 2, 24, 26, 28])
        self.assertEqual(choose(table, hand), 42)

    def test_not_take_full_column(self):
        table = [set([4, 5, 6, 7, 8]), set([3]), set([23, 19, 18, 20, 21]), set([40])]
        hand = set([9, 2])
        self.assertEqual(choose(table, hand), 2)

    def test_try_not_to_take_if_cannot_put_one(self):
        init_all(set(range(1, 25)), set([]))
        table = [set([1, 2, 3, 4, 5]), set([21, 20, 13, 14, 15]), set([23]), set([24])]
        hand = set([6, 7, 9, 16, 19, 22])
        self.assertEqual(choose(table, hand), 19)

if __name__ == '__main__':
    unittest.main()

"""
junk = set([23])
table = [set([1, 2, 3, 4, 5]), set([8, 9, 10, 11, 7]), set([20, 21]), set([22])]
hand = set([6, 15, 16, 17])
all_cards = set(range(1, 25))
choose(table, hand)
"""
"""
hand = set([5, 6, 10])
#hand = set([9, 11, 7])
table = [set([1, 2, 3, 4, 8]), set([22, 23, 24]), set([12, 13, 14, 16, 17]), set([15, 18, 19, 20, 21])]
junk = set([])
all_cards = set(range(1, 25))
print choose(table, hand)
"""