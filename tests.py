import unittest
from practice import *


class TestOverallBehavior(unittest.TestCase):
    def setUp(self):
        self.card = Card(9, 'D')
        self.card.x = 120
        self.card.xmax = self.card.x + self.card.image.get_size()[0]
        self.card.y = 50
        self.card.ymax = self.card.y + self.card.image.get_size()[1]

        self.deck = Deck()

    def tearDown(self):
        del self.card

    def test_within_true(self):
        actual = within(self.card, 130, 69)
        self.assertTrue(actual)

    def test_within_false(self):
        actual = within(self.card, 110, 79)
        self.assertFalse(actual)

    def test_sum(self):
        expected = 32
        actual = sum(14, 18)
        self.assertEqual(expected, actual)

    def test_five_cards_first_dial(self):
        for player in PLAYERS:
            player.hand = []
        first_dial(self.deck)
        actual = all(map(lambda p: len(p.hand) == 5, PLAYERS))
        self.assertTrue(actual)

    def test_eight_cards(self):
        for player in PLAYERS:
            player.hand = []
        first_dial(self.deck)
        second_dial(self.deck)
        actual = all(map(lambda p: len(p.hand) == 8, PLAYERS))
        self.assertTrue(actual)

    def test_cycle_players(self):
        expected = [P0, P1, P00, P11, P0]

        player = cycle_players(P0)
        player0 = next(player)
        player1 = next(player)
        player2 = next(player)
        player3 = next(player)
        player4 = next(player)

        actual = [player0, player1, player2, player3, player4]

        self.assertEqual(expected, actual)

    def test_has_color_true(self):
        P0.hand = []
        P0.hand.append(self.card)
        self.assertTrue(has_color(P0, 'D'))

    def test_has_color_false(self):
        P0.hand = []
        P0.hand.append(self.card)
        self.assertFalse(has_color(P0, 'S'))

    def test_teammates_true(self):
        self.assertTrue(teammates(P0, P00))

    def test_teammates_false(self):
        self.assertFalse(teammates(P1, P00))


class TestCalculation(unittest.TestCase):
    def setUp(self):
        self.card1 = Card(11, 'S')  # вале пика
        self.card2 = Card(12, 'D')  # дама каро
        self.card3 = Card(11, 'C')  # вале спатия
        self.card4 = Card(9, 'H')   # 9 купа

        self.cards = [self.card1, self.card2, self.card3, self.card4]

    def tearDown(self):
        for card in [self.card1, self.card2, self.card3, self.card4]:
            del card

    def test_calculate_clubs(self):
        expected = 25
        actual = calculate(self.cards, 1)
        self.assertEqual(expected, actual)

    def test_calculate_diamonds(self):
        expected = 7
        actual = calculate(self.cards, 2)
        self.assertEqual(expected, actual)

    def test_calculate_hearts(self):
        expected = 21
        actual = calculate(self.cards, 3)
        self.assertEqual(expected, actual)

    def test_calculate_spades(self):
        expected = 25
        actual = calculate(self.cards, 4)
        self.assertEqual(expected, actual)

    def test_calculate_no_trumps(self):
        expected = 14
        actual = calculate(self.cards, 5)
        self.assertEqual(expected, actual)

    def test_calculate_all_trumps(self):
        expected = 57
        actual = calculate(self.cards, 6)
        self.assertEqual(expected, actual)

    def test_calculated_points_all_trumps(self):
        P0.taken = [self.cards[0]]
        P1.taken = self.cards[1:3]
        P00.taken = []
        P11.taken = [self.cards[3]]

        expected = {0: 30, 1: 37}
        actual = calculate_points(6, P0)
        self.assertEqual(expected, actual)

    def test_calculated_points_no_trumps(self):
        P0.taken = [self.cards[0]]
        P1.taken = self.cards[1:3]
        P00.taken = []
        P11.taken = [self.cards[3]]

        expected = {0: 24, 1: 10}
        actual = calculate_points(5, P0)
        self.assertEqual(expected, actual)

    def test_shape_result(self):
        small_result = {0: 94, 1: 68}
        bonuses = {P0: {3: 1, 4: 0, 5: 0, '4ofakind': 0, 'belote': 1},
                   P1: {3: 0, 4: 0, 5: 0, '4ofakind': 0, 'belote': 0},
                   P00: {3: 0, 4: 0, 5: 0, '4ofakind': 0, 'belote': 0},
                   P11: {3: 0, 4: 0, 5: 0, '4ofakind': 0, 'belote': 0}}
        expected = {0: 13, 1: 7}
        actual = shape_result(small_result, P0, bonuses)
        self.assertEqual(expected, actual)

    def test_shape_result_underdogs_win(self):
        small_result = {0: 123, 1: 135}
        bonuses = {P0: {3: 0, 4: 1, 5: 0, '4ofakind': 0, 'belote': 0},
                   P1: {3: 0, 4: 0, 5: 0, '4ofakind': 0, 'belote': 1},
                   P00: {3: 0, 4: 0, 5: 0, '4ofakind': 0, 'belote': 0},
                   P11: {3: 0, 4: 0, 5: 0, '4ofakind': 0, 'belote': 0}}
        expected = {0: 33, 1: 0}
        actual = shape_result(small_result, P1, bonuses)
        self.assertEqual(expected, actual)

    def test_shape_result_kapo(self):
        small_result = {0: 0, 1: 162}
        bonuses = {P0: {3: 0, 4: 1, 5: 0, '4ofakind': 0, 'belote': 0},
                   P1: {3: 0, 4: 0, 5: 0, '4ofakind': 0, 'belote': 1},
                   P00: {3: 0, 4: 0, 5: 0, '4ofakind': 0, 'belote': 0},
                   P11: {3: 0, 4: 0, 5: 0, '4ofakind': 0, 'belote': 0}}
        expected = {0: 5, 1: 27}
        actual = shape_result(small_result, P1, bonuses)
        self.assertEqual(expected, actual)


class TestWinnerInHand(unittest.TestCase):
    def setUp(self):
        self.card1 = Card(10, 'S')  # десетка пика
        self.card1.played_by = P0
        self.card2 = Card(13, 'H')  # поп купа
        self.card2.played_by = P1
        self.card3 = Card(9, 'S')   # 9 пика
        self.card3.played_by = P00
        self.card4 = Card(11, 'S')  # вале пика
        self.card4.played_by = P11

        self.on_table = [self.card1, self.card2, self.card3, self.card4]

    def tearDown(self):
        for card in [self.card1, self.card2, self.card3, self.card4]:
            del card

    def test_trump(self):
        expected = P1
        actual = winner_in_hand(self.on_table, 3)  # игра на купа
        self.assertEqual(expected, actual)

    def test_wanted_trump(self):
        expected = P11
        actual = winner_in_hand(self.on_table, 4)  # игра на купа
        self.assertEqual(expected, actual)

    def test_no_trumps(self):
        expected = P0
        actual = winner_in_hand(self.on_table, 5)  # игра на купа
        self.assertEqual(expected, actual)

    def test_all_trumps(self):
        expected = P11
        actual = winner_in_hand(self.on_table, 6)  # игра на купа
        self.assertEqual(expected, actual)

    def test_decision_making_no_trumps_first_call(self):
        c1 = Card(14, 'S')
        c2 = Card(14, 'D')
        c3 = Card(11, 'S')
        c4 = Card(13, 'H')
        c5 = Card(7, 'C')

        P0.hand = [c1, c2, c3, c4, c5]
        availables = list(range(7))
        self.assertEqual(5, decide_announce(P0, availables))

    def test_decision_making_no_trumps_second_call(self):
        c1 = Card(14, 'S')
        c2 = Card(14, 'D')
        c3 = Card(11, 'S')
        c4 = Card(13, 'H')
        c5 = Card(7, 'C')

        P0.hand = [c1, c2, c3, c4, c5]
        availables = list(range(4, 7))
        self.assertEqual(5, decide_announce(P0, availables, P11))

    def test_decision_making_no_trumps_no_call(self):
        c1 = Card(14, 'S')
        c2 = Card(14, 'D')
        c3 = Card(11, 'S')
        c4 = Card(13, 'H')
        c5 = Card(7, 'C')

        P0.hand = [c1, c2, c3, c4, c5]
        availables = list(range(4, 7))
        self.assertEqual(0, decide_announce(P0, availables, P00))

    def test_decision_making_all_trumps_partner_called(self):
        c1 = Card(9, 'S')
        c2 = Card(9, 'D')
        c3 = Card(11, 'S')
        c4 = Card(13, 'H')
        c5 = Card(7, 'C')

        P0.hand = [c1, c2, c3, c4, c5]
        availables = list(range(4, 7))
        self.assertEqual(6, decide_announce(P0, availables, P00, 3))


class TestBonuses(unittest.TestCase):
    def setUp(self):
        self.card1 = Card(10, 'D')
        self.card2 = Card(8, 'D')
        self.card3 = Card(9, 'D')
        self.card4 = Card(11, 'S')
        self.card5 = Card(12, 'D')
        self.card6 = Card(11, 'D')
        self.card7 = Card(13, 'D')
        self.card8 = Card(11, 'H')
        self.card9 = Card(11, 'C')

    def tearDown(self):
        for card in [self.card1, self.card2, self.card3, self.card4,
                     self.card5, self.card6, self.card7, self.card8,
                     self.card9]:
            del card

    def test_no_bonuses(self):
        cards = [self.card1, self.card8, self.card2, self.card4, self.card6]
        expected = {3: 0, 4: 0, 5: 0, '4ofakind': 0, 'belote': 0}
        actual = check_bonuses(6, cards)
        self.assertEqual(expected, actual)

    def test_three_in_a_row(self):
        cards = [self.card1, self.card2, self.card3, self.card4, self.card5]
        expected = {3: 1, 4: 0, 5: 0, '4ofakind': 0, 'belote': 0}
        actual = check_bonuses(6, cards)
        self.assertEqual(expected, actual)

    def test_four_in_a_row(self):
        cards = [self.card1, self.card2, self.card3, self.card4, self.card6]
        expected = {3: 0, 4: 1, 5: 0, '4ofakind': 0, 'belote': 0}
        actual = check_bonuses(6, cards)
        self.assertEqual(expected, actual)

    def test_five_in_a_row(self):
        cards = [self.card1, self.card2, self.card3, self.card5, self.card6]
        expected = {3: 0, 4: 0, 5: 1, '4ofakind': 0, 'belote': 0}
        actual = check_bonuses(6, cards)
        self.assertEqual(expected, actual)

    def test_four_of_a_kind(self):
        cards = [self.card4, self.card6, self.card8, self.card3, self.card9]
        expected = {3: 0, 4: 0, 5: 0, '4ofakind': 1, 'belote': 0}
        actual = check_bonuses(6, cards)
        self.assertEqual(expected, actual)

    def test_check_for_belote_true(self):
        P0.hand = [self.card5, self.card7]
        bonuses = {P0: {3: 1, 4: 0, 5: 0, '4ofakind': 0, 'belote': 0},
                   P1: {3: 0, 4: 0, 5: 0, '4ofakind': 0, 'belote': 0},
                   P00: {3: 0, 4: 0, 5: 0, '4ofakind': 0, 'belote': 0},
                   P11: {3: 0, 4: 0, 5: 0, '4ofakind': 0, 'belote': 0}}

        expected = {P0: {3: 1, 4: 0, 5: 0, '4ofakind': 0, 'belote': 1},
                    P1: {3: 0, 4: 0, 5: 0, '4ofakind': 0, 'belote': 0},
                    P00: {3: 0, 4: 0, 5: 0, '4ofakind': 0, 'belote': 0},
                    P11: {3: 0, 4: 0, 5: 0, '4ofakind': 0, 'belote': 0}}, True

        actual = check_for_belote(self.card5, P0, 2, bonuses)
        self.assertEqual(expected, actual)

    def test_check_for_belote_false(self):
        P0.hand = [self.card5, self.card8]
        bonuses = {P0: {3: 1, 4: 0, 5: 0, '4ofakind': 0, 'belote': 0},
                   P1: {3: 0, 4: 0, 5: 0, '4ofakind': 0, 'belote': 0},
                   P00: {3: 0, 4: 0, 5: 0, '4ofakind': 0, 'belote': 0},
                   P11: {3: 0, 4: 0, 5: 0, '4ofakind': 0, 'belote': 0}}

        expected = {P0: {3: 1, 4: 0, 5: 0, '4ofakind': 0, 'belote': 0},
                    P1: {3: 0, 4: 0, 5: 0, '4ofakind': 0, 'belote': 0},
                    P00: {3: 0, 4: 0, 5: 0, '4ofakind': 0, 'belote': 0},
                    P11: {3: 0, 4: 0, 5: 0, '4ofakind': 0, 'belote': 0}}, False

        actual = check_for_belote(self.card5, P0, 2, bonuses)
        self.assertEqual(expected, actual)


class TestCardAvailability(unittest.TestCase):
    def setUp(self):
        self.card1 = Card(10, 'D')
        self.card2 = Card(8, 'D')
        self.card3 = Card(9, 'D')
        self.card4 = Card(11, 'S')
        self.card5 = Card(12, 'C')
        self.card6 = Card(11, 'D')
        self.card7 = Card(13, 'C')
        self.card8 = Card(11, 'H')

        P0.hand = [self.card1, self.card4]
        P1.hand = [self.card3, self.card2]
        P00.hand = [self.card5, self.card6]
        P11.hand = [self.card7, self.card8]

    def tearDown(self):
        for card in [self.card1, self.card2, self.card3, self.card4,
                     self.card5, self.card6, self.card7, self.card8]:
            del card

    def test_wrong_color(self):
        on_table = [self.card1]
        self.assertFalse(is_available(self.card4, on_table, P0, 'D', 4))

    def test_trump_wanted_true(self):
        on_table = [self.card1, self.card8, self.card2]
        self.assertTrue(is_available(self.card3, on_table, P1, 'D', 2))

    def test_trump_wanted_false(self):
        on_table = [self.card1, self.card8, self.card2]
        self.assertFalse(is_available(self.card2, on_table, P1, 'D', 2))

    def test_player_has_to_play_trump_true(self):
        on_table = [self.card4]
        self.card4.played_by = P0
        self.assertTrue(is_available(self.card7, on_table, P11, 'S', 1))

    def test_player_has_to_play_trump_false(self):
        on_table = [self.card4]
        self.card4.played_by = P0
        self.assertFalse(is_available(self.card8, on_table, P11, 'S', 1))

    def test_player_free_because_partner_wins(self):
        self.card1.played_by = P0
        self.card5.played_by = P1
        self.card3.played_by = P00

        on_table = [self.card1, self.card5, self.card3]
        self.assertTrue(is_available(self.card8, on_table, P11, 'S', 1))

    def test_expected_rise_all_trumps_true(self):
        on_table = [self.card1]
        P0.hand = [self.card2, self.card3]
        self.assertTrue(is_available(self.card3, on_table, P0, 'D', 6))

    def test_expected_rise_all_trumps_false(self):
        on_table = [self.card1]
        P0.hand = [self.card2, self.card3]
        self.assertFalse(is_available(self.card2, on_table, P0, 'D', 6))


def main():
    unittest.main()

if __name__ == '__main__':
    main()
