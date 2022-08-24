from dataclasses import dataclass
from typing import Any, Dict, Optional, Tuple, Union


@dataclass
class Position:
    x: int
    y: int

    def __repr__(self) -> str:
        return f"{self.x},{self.y}"


@dataclass
class CardNumber:
    value: Union[str, int]

    def __add__(self, other: Any):
        if self.value == "A" and other.value == "A":
            return 10 * 2
        if self.value == "A":
            return 10 + other.value
        if other.value == "A":
            return 10 + self.value
        if isinstance(other, int):
            return self.value + other
        return self.value + other.value

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


class Card:

    position_map = {
        0: "bottom",
        1: "upper",
        2: "left",
        3: "right",
    }

    def __init__(
        self,
        upper_number: int,
        bottom_number: int,
        left_number: int,
        right_number: int,
        played_by: str = "test",
    ) -> None:
        self.upper_number = CardNumber(upper_number)
        self.bottom_number = CardNumber(bottom_number)
        self.left_number = CardNumber(left_number)
        self.right_number = CardNumber(right_number)
        self.played_by = played_by

    def __str__(self) -> str:
        return "cool card"

    def get_sum(self) -> int:
        return (self.upper_number + self.bottom_number) + (
            self.left_number + self.right_number
        )

    def get_sum_upper_left(self) -> int:
        return self.left_number + self.upper_number

    def get_sum_bottom_left(self) -> int:
        return self.left_number + self.bottom_number

    def get_sum_bottom_right(self) -> int:
        return self.right_number + self.bottom_number

    def get_sum_upper_right(self) -> int:
        return self.right_number + self.upper_number

    def get_score_card_for_table(self) -> Dict[str, Tuple[int, Position]]:
        return {
            "upper_left": (self.get_sum_upper_left(), Position(3, 3)),
            "bottom_left": (self.get_sum_bottom_left(), Position(0, 3)),
            "upper_right": (self.get_sum_upper_right(), Position(3, 0)),
            "bottom_right": (self.get_sum_bottom_right(), Position(0, 0)),
        }

    def get_stronger_section_position(self) -> Tuple[int, Position]:
        section_power_map = self.get_score_card_for_table()
        stronger: Optional[Tuple[int, Position]] = None
        for section in section_power_map.values():
            if not stronger:
                stronger = section
            else:
                if stronger[0] < section[0]:
                    stronger = section
        return stronger

    def get_weaker_side(self, position: Position) -> Tuple[CardNumber, Position, str]:
        weaker = None
        position_mapped: str = ""
        calculated_position = None
        for index, card_number in enumerate(
            [self.bottom_number, self.upper_number, self.left_number, self.right_number]
        ):
            if not weaker:
                weaker = card_number
                position_mapped = self.position_map.get(index)
            elif card_number < weaker:
                weaker = card_number
                position_mapped = self.position_map.get(index)
        calculated_position = self._calculate_position(position, position_mapped)
        return (weaker, calculated_position, position_mapped)

    def _calculate_position(self, position, position_mapped) -> Optional[Position]:
        calculated_position = None
        if position_mapped == "bottom" and 0 <= position.y + 1 <= 3:
            calculated_position = Position(position.x, position.y + 1)
        if position_mapped == "upper" and 0 <= position.y - 1 <= 3:
            calculated_position = Position(position.x, position.y - 1)
        if position_mapped == "left" and 0 <= position.x - 1 <= 3:
            calculated_position = Position(position.x - 1, position.y)
        if position_mapped == "right" and 0 <= position.x + 1 <= 3:
            calculated_position = Position(position.x + 1, position.y)
        return calculated_position
