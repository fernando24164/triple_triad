from typing import List
from unittest import TestCase

from src.card import Card, Position
from src.table import Cell, Table


class TestTable(TestCase):
    def setUp(self):
        self.table = Table()
        self.deck: List[Card] = [
            Card(5, 5, 5, 5, "player_1"),
            Card(1, 1, 1, 1, "player_2"),
        ]
        self.table_with_cards = Table()
        self.table_with_cards.put_card(Card(5, 5, 5, 5, "player_1"), Position(0,0))

    def test_put_card(self):
        self.table.put_card(self.deck.pop(), Position(0, 0))
        self.assertIsNotNone(len(self.table.cells))
        self.table.put_card(self.deck.pop(), Position(1, 0))
        self.assertIsNotNone(len(self.table.cells))

    def test_calculate_points_with_initial_table(self):
        scores = self.table.calculate_points()
        self.assertDictContainsSubset(dictionary=scores, subset={"player1": 5})

    def test_get_empty_cells_surround(self):
        cell = Cell(Position(0,0))
        response = self.table_with_cards.get_empty_cells_surround(cell)
        self.assertIsNotNone(response)
