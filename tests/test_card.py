from unittest import TestCase

from src.card import CardNumber, Card, Position


class TestCardNumber(TestCase):
    def test_card_number_gt(self):
        a = CardNumber(7)
        b = CardNumber("A")
        self.assertFalse(a > b)

    def test_card_number_lt(self):
        a = CardNumber(1)
        b = CardNumber(9)
        self.assertTrue(a < b)

    def test_card_number_eq_wrong(self):
        a = CardNumber("A")
        b = CardNumber(9)
        self.assertFalse(a == b)

    def test_card_number_eq_check(self):
        a = CardNumber(9)
        b = CardNumber(9)
        self.assertTrue(a == b)

    def test_card_sum(self):
        a = CardNumber("A")
        b = CardNumber(9)
        self.assertEqual(19, a + b)


class TestCard(TestCase):
    def test_card_creation(self):
        a = Card(1, 2, 3, 4)
        self.assertIsNotNone(a)

    def test_card_score(self):
        a = Card(1, 2, 3, 4)
        score = a.get_sum()
        self.assertEqual(10, score)

    def test_card_score_left(self):
        a = Card("A", 2, "A", 4)
        score = a.get_sum_upper_left()
        self.assertEqual(20, score)

    def test_card_stronger_section(self):
        a = Card("A", 2, 9, 4)
        score = a.get_stronger_section_position()
        self.assertEqual(19, score[0])

    def test_card_weaker_number(self):
        a = Card("A", 2, 9, 4)
        weaker_side = a.get_weaker_side(Position(0,0))
        self.assertEqual((CardNumber(value=2), Position(0,1)), weaker_side)

    def test_card_weaker_number_impossible_position(self):
        a = Card(1, 2, 9, 4)
        weaker_side = a.get_weaker_side(Position(0,0))
        self.assertEqual((CardNumber(value=1), None), weaker_side)
