from typing import List
from unittest import TestCase
from src.card import Position, Table, Card

class TestTable(TestCase):
    def setUp(self):
        self.table = Table()
        self.deck : List[Card] = [Card(5,5,5,5,'player_1'),Card(1,1,1,1, 'player_2')]

    def test_put_card(self):
        self.table.put_card(self.deck.pop(), Position(0,0))
        self.assertIsNotNone(len(self.table.cells))
