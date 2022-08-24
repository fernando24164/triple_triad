from dataclasses import dataclass
from typing import List, Optional, Tuple

from src.card import Card, CardNumber, Position
from src.table import Cell, Table


@dataclass
class Player:
    deck: List[Card]
    points: int = 5

    def play(self, table: Table) -> Card:
        deck_card, position_to_play = self.optimized_card(table)
        table.put_card(self.deck.pop(deck_card), position_to_play)

    def best_initial_card(self) -> Tuple[int, Position]:
        stronger: Optional[Tuple[int, Position]] = None
        deck_index = 0
        for index, card in enumerate(self.deck):
            if not stronger:
                stronger = card.get_stronger_section_position()
                deck_index = index
            else:
                stronger_card_section = card.get_stronger_section_position()
                if stronger[0] <= stronger_card_section[0]:
                    stronger = stronger_card_section
                    deck_index = index
        return deck_index, stronger[1]

    def get_best_card_for_positions(self, table: Table) -> Tuple[int, Position]:
        weaker_number_to_compare: int = None
        position_to_play: Position = None
        position_number_to_compare: str = None
        for position in table.get_occupied_position():
            cell: Cell = table.cells.get(position)
            (
                weaker_number,
                suggested_card_position,
                position_weaker_suggested,
            ) = cell.card.get_weaker_side(cell.position)
            if (
                suggested_card_position
                and suggested_card_position in table.get_empty_cells_surround(cell)
            ):
                weaker_number_to_compare = weaker_number
                position_to_play = suggested_card_position
                position_number_to_compare = position_weaker_suggested
        # Playing offensive way
        if position_to_play:
            deck_index = self.get_stronger_card(
                weaker_number_to_compare, position_number_to_compare
            )
        # Playing defensive way
        else:
            less_positions_to_defend = [1] * 4
            for position in table.get_occupied_position():
                cell: Cell = table.cells.get(position)
                random_empty_positions: List[Cell] = table.get_empty_cells_surround(
                    cell
                )
                if random_empty_positions:
                    less_positions_to_defend = min(
                        less_positions_to_defend, random_empty_positions
                    )
            if position_to_defend := less_positions_to_defend.pop() and isinstance(
                position_to_defend, Position
            ):
                deck_index = self.get_stronger_defensive_card(table, position_to_defend)
            return deck_index, random_empty_positions[0]
        return deck_index, position_to_play

    def optimized_card(self, table: Table) -> Tuple[int, Position]:
        if table.is_empty():
            return self.best_initial_card()
        return self.get_best_card_for_positions(table)

    def get_stronger_defensive_card(
        self, table: Table, random_empty_position: Position
    ):
        check_cells_to_defend: List[Cell] = table.get_empty_cells_surround(
            random_empty_position
        )
        positions_to_defend = [cell.position for cell in check_cells_to_defend]
        positions_str = []
        for position in positions_to_defend:
            if position.x + 1 == random_empty_position.x:
                positions_str.append("left")
            if position.x - 1 == random_empty_position.x:
                positions_str.append("right")
            if position.y + 1 == random_empty_position.y:
                positions_str.append("bottom")
            if position.y - 1 == random_empty_position.y:
                positions_str.append("upper")
        stronger = (0, 0)
        for index, card in enumerate(self.deck):
            card_defensive_value = 0
            for position in positions_str:
                if positions_str == "upper":
                    card_defensive_value += card.upper_number
                if positions_str == "bottom":
                    card_defensive_value += card.bottom_number
                if positions_str == "left":
                    card_defensive_value += card.left_number
                if positions_str == "right":
                    card_defensive_value += card.right_number
            if stronger[0] < card_defensive_value:
                stronger = (card_defensive_value, index)
        return stronger[1]

    def get_stronger_card(
        self, weaker_number_to_compare: CardNumber, position_number_to_compare: str
    ):
        stronger = 0
        for index, card in enumerate(self.deck):
            if position_number_to_compare == "bottom":
                if card.bottom_number > weaker_number_to_compare:
                    stronger = index
            if position_number_to_compare == "upper":
                if card.upper_number > weaker_number_to_compare:
                    stronger = index
            if position_number_to_compare == "left":
                if card.left_number > weaker_number_to_compare:
                    stronger = index
            if position_number_to_compare == "right":
                if card.right_number > weaker_number_to_compare:
                    stronger = index
        return stronger
