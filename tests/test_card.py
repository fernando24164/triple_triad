from unittest import TestCase

from src.card import CardNumber


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
        c = a == b
        self.assertFalse(a == b)

    def test_card_number_eq_check(self):
        a = CardNumber(9)
        b = CardNumber(9)
        self.assertTrue(a == b)
