from unittest import TestCase

from src.card import Card, CardNumber
from src.cpu_player import Player
from src.table import Table


class TestCPUPlayer(TestCase):
    def setUp(self) -> None:
        self.table = Table()
        self.deck = [Card(1, 1, 1, 1)] * 4 + [Card(7, 5, "A", 5)]
        self.cpu_player = Player(self.deck)

    def test_best_initial_card(self):
        self.cpu_player.play(self.table)
        self.assertEqual(self.table.is_empty(), False)

    def test_get_stronger_card(self):
        response = self.cpu_player.get_stronger_card(CardNumber(4), "bottom")
        self.assertEqual(4, response)
