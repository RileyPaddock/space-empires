import sys
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

import random



class BasicStrategy:  # no movement or actual strategy, just funcitons like decide_removal or decide_which_unit_to_attack or simple_sort
    def __init__(self, player_index):  # wutever we need):
        self.player_index = player_index

    def decide_removal(self, game_state):
        sorted_list = self.simple_sort(
            game_state['players'][self.player_index]['ships'])
        total_cost = sum([ship['cost'] for ship in sorted_list])
        if total_cost > game_state['players'][self.player_index]['creds']:
            return sorted_list[-1]['id'] - 1

    def decide_which_unit_to_attack(self, combat_state, attacker_index, location):
        return self.strongest_enemy_ship(combat_state[location])

    def decide_which_units_to_screen(self, combat_state):
        return []

    def simple_sort(self, ship_dict):
        fixed_arr, sorted_arr = [], []
        for _, ship_attributes in ship_dict.items():
            if ship_attributes['name'] != 'Decoy' and ship_attributes['name'] != 'Colony Ship' and ship_attributes['name'] != 'Miner' and ship_attributes['name'] != 'Colony':
                fixed_arr.append(ship_attributes)
        while len(fixed_arr) > 0:
            sorted_arr.append(self.max_value(fixed_arr))
            fixed_arr.remove(self.max_value(fixed_arr))
        return sorted_arr

    def max_value(self, arr):
        strongest_ship = arr[0]
        for ship in arr[1:]:
            if self.ship_1_fires_first(ship, strongest_ship):
                strongest_ship = ship
        return strongest_ship

    def ship_1_fires_first(self, ship_1, ship_2):
        if ship_1['fighting_class'] > ship_2['fighting_class']:
            return True
        elif ship_1['fighting_class'] < ship_2['fighting_class']:
            return False
        else:
            if ship_1['attack_tech'] > ship_2['attack_tech']:
                return True
            elif ship_1['attack_tech'] < ship_2['attack_tech']:
                return False
            else:
                if ship_1['attack'] > ship_2['attack']:
                    return True
                elif ship_1['attack'] < ship_2['attack']:
                    return False
                else:
                    return True

    def strongest_enemy_ship(self, combat_state_ship_list):
        for unit_information in combat_state_ship_list:
            if unit_information['player'] != self.player_index + 1:
                return unit_information

    def decide_ship_placement(self, game_state):
        ship_yards = game_state['players'] [self.player_index] ['ship_yards']
        random_ship_yard = random.randint(1, len(ship_yards)) - 1
        return ship_yards[random_ship_yard]['x'], ship_yards[random_ship_yard]['y']

    def will_colonize_planet(self, coordinates, game_state):
        return False

    def upgrade_costs(self, stat_to_upgrade, game_state):
        player = game_state['players'][self.player_index]
        if stat_to_upgrade == 'attack':  # offense
            return 10 * player['attack_tech']
        elif stat_to_upgrade == 'defense':  # defense
            return 10 * player['defense_tech']
        elif stat_to_upgrade == 'fighting' and player['fighting_class_tech'] < 3:  # tactics
            return 5 * player['fighting_class_tech'] + 10
        elif stat_to_upgrade == 'movement' and player['movement_tech_upgrade_number'] < 5:  # speed
            return 10 * player['movement_tech_upgrade_number'] + 10
        elif stat_to_upgrade == 'ship yard' and player['ship_yard_tech'] < 2:  # ship yard
            return 10 * player['ship_yard_tech']
        elif stat_to_upgrade == 'terraform' and player['terraform_tech'] < 2:  # terraform
            return 15 * player['terraform_tech']
        elif stat_to_upgrade == 'building size' and player['ship_size_tech'] < 6:  # biggest ship size that you can build
            return 5 * player['ship_size_tech'] + 10
