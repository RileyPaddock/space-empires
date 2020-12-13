class DumbStrategy:
    def __init__(self,player_num):
        self.player_num = player_num

    def will_colinize_planet(self,colony_ship_loc,game_state):
        return True
    
    def decide_ship_movement(self,ship_index, game_state):
        ship = game_state['players'][self.player_num-1]['units'][ship_index]
        if ship['location'][0] != game_state['board_size'][0]-1:
           return (1, 0)
        else:
            return (0,0)
    
    def decide_purchases(self,game_state):
        units = []
        money = game_state['players'][self.player_num-1]['cp']
        while money - 6 >= 0:
            units.append('Scout')
            money -= 6
        return {'units':units,'tech':[]}
    
    def decide_removals(self, game_state):
        ship_removals = []
        i = 0
        exess_cp = sum([unit['hull_size'] for unit in game_state['players'][self.player_num-1]['units']]) - game_state['players'][self.player_num-1]['money']
        while exess_cp>0:
            ship_removals.append(game_state['players'][self.player_num - 1]['units'][i]['unit_num'])
            exess_cp -= game_state['players'][self.player_num - 1]['units'][i]['hull_size']
            i+=1
        return ship_removals

    def decide_which_unit_to_attack(self, combat_state, attacking_ship_index):
        for entry in combat_state:
            if entry['player'] != combat_state['order'][attacking_ship_index]['player']:
                return combat_state.index(entry)

    def decide_which_units_to_screen(self, combat_state):
        return []