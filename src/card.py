from dataclasses import dataclass
from typing import Union


@dataclass
class Position:
    x: int
    y: int

    def __repr__(self) -> str:
        return f"{self.x},{self.y}"


@dataclass
class CardNumber:
    value: Union[str, int]

    def __eq__(self, other: object) -> bool:
        if (self.value == "A" and isinstance(other.value, int)) or (
            other.value == "A" and isinstance(self.value, int)
        ):
            return False
        return self.value == other.value

    def __gt__(self, other):
        if other.value == "A" and isinstance(self.value, int):
            return False
        if other.value == "A" and self.value == "A":
            return False
        if self.value == "A" and isinstance(other.value, int):
            return True
        return self.value > other.value

    def __lt__(self, other):
        if other.value == "A" and isinstance(self.value, int):
            return True
        if other.value == "A" and self.value == "A":
            return True
        if self.value == "A" and isinstance(other.value, int):
            return False
        return self.value < other.value


@dataclass
class Card:
    upper_number: CardNumber
    bottom_number: CardNumber
    left_number: CardNumber
    right_number: CardNumber
    played_by: str

    def __str__(self) -> str:
        return "cool card"
