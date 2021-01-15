from basic_strategy import BasicStrategy
import sys
sys.path.append('src')
from units.scout import Scout


class DumbStrategy(BasicStrategy):
    def __init__(self, player_index):  # wutever else we need):
        self.player_index = player_index

    def decide_purchases(self, game_state):
        return self.decide_ship_purchases(game_state)

    def decide_ship_purchases(self, game_state):
        return Scout(None, (0, 0), 0, 0, True)

    def decide_ship_movement(self, ship, game_state, movement_round):
        x, y = 0,0
        if ship['x'] < game_state['players'][self.player_index]['grid_size']:
            x += ship['movement_tech'][movement_round]
        return x, y
