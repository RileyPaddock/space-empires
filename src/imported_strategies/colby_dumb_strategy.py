from basic_strategy import BasicStrategy
import sys
import random
sys.path.append('src')
from units.decoy import Decoy
from units.base import Base
from units.ship_yard import ShipYard
from units.colony import Colony
from units.colony_ship import ColonyShip
from units.dreadnaught import Dreadnaught
from units.battleship import Battleship
from units.battlecruiser import Battlecruiser
from units.cruiser import Cruiser
from units.destroyer import Destroyer
from units.scout import Scout
from units.unit import Unit



class DumbStrategy(BasicStrategy):
    def __init__(self, player_index):  # wutever else we need):
        self.player_index = player_index
        self.__name__ = 'DumbStrategy'

    def decide_purchases(self, game_state):
        return self.decide_ship_purchases(game_state)

    def decide_ship_purchases(self, game_state):
        return Scout(None, (0, 0), 0, 0, True)

    def decide_ship_movement(self, ship, game_state, movement_round):
        x, y = 0, 0
        if ship['x'] < game_state['players'][self.player_index]['board_size']:
            x += ship['movement_tech'][movement_round]
        return x, y
