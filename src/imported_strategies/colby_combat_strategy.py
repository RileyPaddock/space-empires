from basic_strategy import BasicStrategy
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
import sys
import random
sys.path.append('src')


class CombatStrategy(BasicStrategy):
    def __init__(self, player_index):  # wutever else we need):
        self.player_index = player_index
        self.__name__ = 'CombatStrategy'
        self.previous_buy = 'Scout'

    def decide_purchases(self, game_state):
        purchases = {'units': [], 'technology': []}
        total_cost = 0
        while game_state['players'][self.player_index]['creds'] > total_cost:
            if game_state['turn'] == 1 and game_state['players'][self.player_index]['ship_size_tech'] == 0 and 'building size' not in purchases['technology']:
                if game_state['players'][self.player_index]['creds'] > total_cost + self.upgrade_costs('building size', game_state):
                    purchases['technology'].append('building size')
                    total_cost += self.upgrade_costs('building size', game_state)
                else: break
            else:
                ship = self.decide_ship_purchases(game_state)
                if game_state['players'][self.player_index]['creds'] > total_cost + self.ship_cost(ship):
                    purchases['units'].append(ship)
                    total_cost += self.ship_cost(ship)
                else: break
        return purchases

    def ship_cost(self, ship):
        if ship == 'Scout':
            return 6
        elif ship == 'Destroyer':
            return 9
        elif ship == 'Cruiser':
            return 12
        elif ship == 'BattleCruiser':
            return 15
        elif ship == 'Battleship':
            return 20
        elif ship == 'Dreadnaught':
            return 24
        elif ship == 'Carrier':
            return 12
        elif ship == 'Miner':
            return 5
        elif ship == 'Colony_Ship':
            return 8
        else:
            return 6

    def decide_ship_purchases(self, game_state):
        if self.check_previous_buy() == 'Destroyer':
            self.previous_buy = 'Scout'
            return 'Scout'
        if self.check_previous_buy() == 'Scout':
            self.previous_buy = 'Destroyer'
            return 'Destroyer'

    def check_previous_buy(self):
        if self.previous_buy == 'Scout':
            return 'Scout'
        elif self.previous_buy == 'Destroyer':
            return 'Destroyer'

    def decide_ship_movement(self, ship_index, game_state):
        center_point_x, center_point_y = game_state['board_size'][0] // 2, game_state['board_size'][0] // 2
        ship = game_state['players'][self.player_index]['units'][ship_index]
        ship_x, ship_y = ship['coords']
        x, y = 0, 0
        if ship_x != center_point_x:
            if ship_x < center_point_x:
                x += ship['movement_tech'][game_state['movement_round']]
            elif ship_x > center_point_x:
                x -= ship['movement_tech'][game_state['movement_round']]
            return x, y
        if ship_y != center_point_y:
            if ship_y < center_point_y:
                y += ship['movement_tech'][game_state['movement_round']]
            elif ship_y > center_point_y:
                y -= ship['movement_tech'][game_state['movement_round']]
            return x, y
        return x, y
