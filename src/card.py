from collections import defaultdict
from dataclasses import dataclass
from typing import List, Optional


@dataclass
class Position:
    x: int
    y: int

    def __repr__(self) -> str:
        return f"{self.x},{self.y}"


@dataclass
class Card:
    upper_number: int
    bottom_number: int
    left_number: int
    right_number: int
    played_by: str

    def __str__(self) -> str:
        return "cool card"


@dataclass
class Player:
    deck: List[Card]

    def play(self):
        pass


@dataclass
class Cell:
    position: Position
    card: Optional[Card] = None
    owner_by_player: Optional[str] = None

    def is_empty(self):
        return self.card is None


@dataclass
class Table:
    cells = defaultdict(default_factory=None)
    x_max: int = 3
    y_max: int = 3

    def put_card(self, card: Card, position: Position):
        if self.cells.get(str(position), None) is None:
            self.cells[str(position)] = Cell(position, card, card.played_by)
            self.calculate_status(position)

    def __str__(self) -> str:
        return f"{str(self.cells)}"

    def _check_card_left(self, cell):
        if cell.position.x - 1 >= 0:
            cell_on_left = self.cells[
                str(Position(cell.position.x - 1, cell.position.y))
            ]
            if cell_on_left:
                if cell.card.left_number > cell_on_left.card.right_number:
                    cell_on_left.owner_by_player = cell.card.played_by
                elif cell.card.left_number < cell_on_left.card.right_number:
                    cell.owner_by_player = cell_on_left.owner_by_player

    def _check_card_right(self, cell):
        if cell.position.x + 1 <= self.x_max:
            cell_on_right = self.cells.get(
                str(Position(cell.position.x + 1, cell.position.y))
            )
            if cell_on_right:
                if cell.card.right_number > cell_on_right.card.left_number:
                    cell_on_right.owner_by_player = cell.card.played_by
                elif cell.card.right_number < cell_on_right.card.left_number:
                    cell.owner_by_player = cell_on_right.owner_by_player

    def _check_card_down(self, cell):
        if cell.position.y - 1 >= 0:
            cell_down = self.cells.get(
                str(Position(cell.position.x, cell.position.y - 1))
            )
            if cell_down:
                if cell.card.bottom_number > cell_down.card.upper_number:
                    cell_down.owner_by_player = cell.card.played_by
                elif cell.card.bottom_number < cell_down.card.upper_number:
                    cell.owner_by_player = cell_down.owner_by_player

    def _check_card_up(self, cell):
        if cell.position.y + 1 <= self.y_max:
            cell_up = self.cells.get(
                str(Position(cell.position.x, cell.position.y + 1))
            )
            if cell_up:
                if cell.card.upper_number > cell_up.card.bottom_number:
                    cell_up.owner_by_player = cell.card.played_by
                elif cell.card.upper_number < cell_up.card.bottom_number:
                    cell.owner_by_player = cell_up.owner_by_player

    def calculate_status(self, position: Position):
        cell: Card = self.cells.get(str(position))
        self._check_card_left(cell)
        self._check_card_right(cell)
        self._check_card_down(cell)
        self._check_card_up(cell)


@dataclass
class Game:
    computer_player: Player
    table: Table
    status: str = "initial"

    def init_game(self):
        pass
        # first_player = self.turn.random_number()

        # while self.table.calculate_status != "finish":
        #     pass
        # pass
