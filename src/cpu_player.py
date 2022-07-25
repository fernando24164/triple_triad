from dataclasses import dataclass
from typing import List

from src.card import Card


@dataclass
class Player:
    deck: List[Card]
    points: int = 5

    def play(self):
        pass
