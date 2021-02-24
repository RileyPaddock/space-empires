class RileyStrategy2:
    def __init__(self, player_index):
        self.player_index = player_index

    def decide_ship_movement(self, unit_index, hidden_game_state):
        myself = hidden_game_state['players'][self.player_index]
        opponent_index = 1 - self.player_index
        opponent = hidden_game_state['players'][opponent_index]

        unit = myself['units'][unit_index]
        x_unit, y_unit = unit['coords']
        x_home, y_home = myself['home_coords']
        x_opp, y_opp = opponent['home_coords']

        if myself['units'][unit_index]['technologies']['movement'] > 1:
            opponent_move = False
            for unit in opponent['units']:
                    if tuple(unit['coords']) != (x_opp, y_opp):
                        opponent_move = True
                        break
            if hidden_game_state['turn'] > 10 or opponent_move:
                best_translation = self.best_move(unit, opponent, myself)
            else:
                best_translation = (0,0)
        else:
            return (0,0)

        return best_translation

    def best_move(self,unit, opponent, myself):
        x_unit, y_unit = unit['coords']
        x_home, y_home = myself['home_coords']
        x_opp, y_opp = opponent['home_coords']
        translations = [(0,0), (1,0), (-1,0), (0,1), (0,-1)]
        best_translation = (0,0)
        smallest_distance_to_opponent = 999999999999

        if (x_unit, y_unit) == (x_home,y_home):#move unit 1 to the right at begining
            best_translation = (1,0)
        elif  abs(x_unit - x_opp) + abs(y_unit - y_opp) > 1:#move unit to 1 to the right of enemy home
            for translation in translations:
                delta_x, delta_y = translation
                x = x_unit + delta_x
                y = x_unit + delta_y
                dist = abs(x - (x_opp+1)) + abs(y - y_opp)
                if dist < smallest_distance_to_opponent:
                    best_translation = translation
                    smallest_distance_to_opponent = dist
        else:#move into the enemy home
            best_translation = (-1,0)
        return best_translation

    def decide_which_unit_to_attack(self, hidden_game_state,combat_state, coords, attacker_index):
        # attack opponent's first ship in combat order

        combat_order = combat_state[coords]
        player_indices = [unit['player'] for unit in combat_order]

        opponent_index = 1 - self.player_index
        for combat_index, unit in enumerate(combat_order):
            if unit['player'] == opponent_index:
                return combat_index

    def decide_purchases(self,game_state):
        units = []
        tech = []
        sc = ['Scout',6] 
        spawn_loc = game_state['players'][self.player_num]['home_coords']
        cp = game_state['players'][self.player_num]['cp']
        movement_tech = game_state['players'][self.player_num]['technology']['movement']
        move = ['movement',game_state['technology_data']['movement'][movement_tech]]
        ship_choice = move

        if game_state['turn'] > 1:
            while cp >= ship_choice[1]:
                if movement_tech<2:
                        movement_tech+=1
                        tech.append(ship_choice[0])
                        cp -= ship_choice[1]
                        ship_choice = sc
                else:
                    units.append({'type':ship_choice[0], 'coords':spawn_loc})
                    cp -= ship_choice[1]
        return {'units':units,'technology':tech}