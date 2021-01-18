class DumbStrategy:

    def __init__(self, player_num):
        self.player_num = player_num

    def decide_ship_movement(self, ship_index, game_state):
        return (-1,0) 

    def decide_purchases(self, game_state):
        purchases = {}
        cp =game_state['players'][self.player_num]['cp']
        units = []
        scout = game_state['unit_data']['Scout']
        if cp > scout['cp_cost']:
            while True:
                if cp >= scout['cp_cost']:
                    units.append('Scout')
                    cp -= scout['cp_cost']
                else:
                    break
        if len(units) >= 1:
            purchases['units'] = units
        purchases['tech'] = []
        return purchases

    def decide_removal(self, game_state):
        return -1
        
    def decide_which_unit_to_attack(self, combat_state, location, attacker_index):
        for unit in combat_state[tuple(location)]:
            if unit['player'] != combat_state[tuple(location)][attacker_index]['player']:
                return combat_state[tuple(location)].index(unit)


    def will_colonize_planet(self, coords, game_state):
        return False

    def decide_which_units_to_screen(self, combat_state):
        return []