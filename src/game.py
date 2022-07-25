import random
from dataclasses import dataclass

from src.cpu_player import Player
from src.table import Table


@dataclass
class Game:
    computer_player: Player
    table: Table
    status: str = "initial"

    def init_game(self):
        pass
        will_start_human = bool(random.getrandbits(1))

        while not self.is_finished_game():
            self.next_turn(will_start_human)

    def next_turn(self, will_start_human):
        if will_start_human:
            ui.print_table()
            card, position = ui.get_movement()
            self.table.put_card(card, position)
        self.computer_player.make_movement()
