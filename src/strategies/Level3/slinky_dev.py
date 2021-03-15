class BerserkerStrategy:

    def __init__(self, player_number):
        self.player_number = player_number

    def decide_ship_movement(self, unit_num, hidden_game_state):
        units = hidden_game_state['players'][self.player_number]['units']
        for unit in units:
            if unit['num'] == unit_num:
                if tuple(unit['coords']) != (3,6):
                    return (0,1)

    def decide_which_unit_to_attack(self, combat_state, coords, attacker_num):
        # attack the first opposing ship that's not a Homeworld or Colony

        for unit in combat_state[coords]:
            if unit['player'] != self.player_number:
                if unit['type'] not in ['Homeworld', 'Colony']:
                    return combat_state[coords].index(unit)

        for unit in combat_state[coords]:
            if unit['player'] != self.player_number:
                return combat_state[coords].index(unit)

class StationaryStrategy:

    def __init__(self, player_number):
        self.player_number = player_number

    def decide_ship_movement(self, unit_num, hidden_game_state):
        return (0,0)

    def decide_which_unit_to_attack(self, combat_state, coords, attacker_num):
        # attack the first opposing ship that's not a Homeworld or Colony

        for unit in combat_state[coords]:
            if unit['player'] != self.player_number:
                if unit['type'] not in ['Homeworld', 'Colony']:
                    return combat_state[coords].index(unit)

        for unit in combat_state[coords]:
            if unit['player'] != self.player_number:
                return combat_state[coords].index(unit)