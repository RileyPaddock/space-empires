import sys
import random
sys.path.append('src')
from unit.unit import Unit
from unit.scout import Scout
from unit.destroyer import Destroyer
from unit.cruiser import Cruiser
from unit.battle_cruiser import BattleCruiser
from unit.battleship import Battleship
from unit.dreadnaught import Dreadnaught
from unit.colony_ship import Colony_Ship
from unit.colony import Colony
from unit.ship_yard import Ship_Yard
from unit.base import Base
from unit.miner import Miner
from unit.decoy import Decoy
from unit.carrier import Carrier
from strategies.basic_strategy import BasicStrategy

class CombatStrategy(BasicStrategy):
    def __init__(self, player_index):#wutever else we need):
        self.player_index = player_index

    def decide_purchases(self, game_state):
        if game_state['turn'] == 1 and game_state['players'][self.player_index]['ship_size_tech'] == 0: return 7
        else: return self.decide_ship_purchases(game_state)

    def decide_ship_purchases(self, game_state):
        if self.check_previous_buy() == 2: 
            self.previous_buy = Scout(None, (0,0), 0, 0, True)
            return Scout(None, (0,0), 0, 0, True)
        if self.check_previous_buy() == 1: 
            self.previous_buy = Destroyer(None, (0,0), 0, 0, True)
            return Destroyer(None, (0,0), 0, 0, True)

    def check_previous_buy(self):
        if isinstance(self.previous_buy, Scout): return 1
        elif isinstance(self.previous_buy, Destroyer): return 2

    def decide_ship_movement(self, ship_index, game_state):
        center_point_x, center_point_y = game_state['grid_size'] // 2, game_state['grid_size'] // 2
        x, y = 0,0
        if x != center_point_x:
            if x < center_point_x:
                x += game_state['players'][self.player_index]['ships'][ship_index]['movement_tech'][game_state['movement_round']]
            elif x > center_point_x:
                x -= game_state['players'][self.player_index]['ships'][ship_index]['movement_tech'][game_state['movement_round']]  
        if y != center_point_y:
            if y < center_point_y:
                y += game_state['players'][self.player_index]['ships'][ship_index]['movement_tech'][game_state['movement_round']]
            elif y > center_point_y:
                y -= game_state['players'][self.player_index]['ships'][ship_index]['movement_tech'][game_state['movement_round']]
        return x, y