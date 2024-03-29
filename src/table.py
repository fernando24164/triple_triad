from collections import defaultdict
from dataclasses import dataclass, field
from typing import List, Optional

from src.card import Card, Position


@dataclass
class Cell:
    position: Position
    card: Optional[Card] = None
    owner_by_player: Optional[str] = None

    def is_empty(self):
        return self.card is None


@dataclass
class Table:
    cells: defaultdict = field(default_factory=lambda: defaultdict(None))
    x_max: int = 3
    y_max: int = 3

    def put_card(self, card: Card, position: Position):
        if self.cells.get(str(position), None) is None:
            self.cells[str(position)] = Cell(position, card, card.played_by)
            self.calculate_status(position)

    def calculate_points(self):
        score = {"player1": 0, "player2": 0}
        if not self.cells:
            return {"player1": 5, "player2": 5}
        for cell in self.cells.values():
            if cell.owner_by_player == "player1":
                score["player1"] += 1
            else:
                score["player2"] += 1
        return score

    def __str__(self) -> str:
        return f"{str(self.cells)}"

    def _check_card_left(self, cell):
        if cell.position.x - 1 >= 0:
            cell_on_left = self.cells.get(
                str(Position(cell.position.x - 1, cell.position.y))
            )
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

    def is_empty(self):
        return len(self.cells) <= 0

    def get_occupied_position(self) -> List[str]:
        return self.cells.keys()

    def get_empty_cells_surround(self, cell: Cell) -> List[Cell]:
        empty_positions: List[Cell] = []
        cell_position = cell.position
        # check left
        position_left = cell_position.x - 1
        if 0 <= position_left <= self.x_max:
            cell = self.cells.get(str(Position(position_left, cell_position.y)))
            if not cell:
                empty_positions.append(Position(position_left, cell_position.y))
        # check right
        position_right = cell_position.x + 1
        if 0 <= position_right <= self.x_max:
            cell = self.cells.get(str(Position(position_right, cell_position.y)))
            if not cell:
                empty_positions.append(Position(position_right, cell_position.y))
        # check up
        position_up = cell_position.y + 1
        if 0 <= position_up <= self.y_max:
            cell = self.cells.get(str(Position(cell_position.x, position_up)))
            if not cell:
                empty_positions.append(Position(cell_position.x, position_up))
        # check down
        position_down = cell_position.y - 1
        if 0 <= position_down <= self.y_max:
            cell = self.cells.get(str(Position(cell_position.x, position_down)))
            if not cell:
                empty_positions.append(Position(cell_position.x, position_down))

        return empty_positions
