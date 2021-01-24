import sys
sys.path.append('src')
from imported_strategies.strategy_util import get_possible_spots, is_in_bounds


class CombatStrategy:
    buy_destroyer = True

    def __init__(self, player_index):
        self.player_index = player_index

    # Don't colonize planets
    def will_colonize_planets(self, coords, game_state):
        return False

    # Move all ships closer to the center
    def decide_ship_movement(self, unit_index, game_state):
        unit = game_state['players'][self.player_index]['units'][unit_index]
        sp = game_state['round']
        tech_amt = game_state['players'][self.player_index]['spaces'][sp]
        possible_spaces = get_possible_spots(
            unit["coords"], tech_amt, game_state["board_size"])
        distances = [dist((2, 2), pos)
                     for pos in possible_spaces]
        next_space = possible_spaces[distances.index(min(distances))]
        return next_space[0] - unit["coords"][0], next_space[1] - unit["coords"][1]

    # Buy all possible size tech and scouts/destroyers
    def decide_purchases(self, game_state):
        unit_data = game_state['unit_data']
        player_state = game_state['players'][self.player_index]
        cp = player_state['cp']
        technology_data = game_state['technology_data']
        ss_level = player_state["tech"]["ss"]
        purchases = {"tech": [], "units": []}
        if cp > technology_data["ss"]["price"][ss_level] and ss_level < 2:
            purchases["tech"].append("ss")
            cp -= technology_data["ss"]["price"][ss_level]
            ss_level = 2
        can_buy_destroyer = cp >= unit_data["Destroyer"][
            "cp_cost"] and ss_level >= unit_data["Destroyer"]["req_size_tech"]
        if self.buy_destroyer:
            if can_buy_destroyer:
                purchases["units"] = ["Destroyer"]
        else:
            purchases["units"] = ["Scout"]
        return purchases

    # Return ship #0
    def decide_removal(self, game_state):
        return 0

    # Choose the first unit to attack
    def decide_which_unit_to_attack(self, combat_state, coords, attacker_index):
        return next((i for i, x in enumerate(combat_state) if self.player_index != x['player'] and x['alive']), None)

    # Don't screen any units
    def decide_which_units_to_screen(self, combat_state):
        return []


def dist(p1, p2):
    return abs(p1[0]-p2[0]) + abs(p1[1]-p2[1])
