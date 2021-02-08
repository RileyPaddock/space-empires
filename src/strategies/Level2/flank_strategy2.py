class FlankerStrategyLevel2:

    def __init__(self, player_index):
        self.player_index = player_index
        self.name = 'flanker'
        self.flank_direction = (1,0)

    def decide_ship_movement(self, unit_index, hidden_game_state):
        myself = hidden_game_state['players'][self.player_index]
        opponent_index = 1 - self.player_index
        opponent = hidden_game_state['players'][opponent_index]

        unit = myself['units'][unit_index]
        x_unit, y_unit = unit['coords']
        x_opp, y_opp = opponent['home_coords']

        translations = [(0,0), (1,0), (-1,0), (0,1), (0,-1)]

        if hidden_game_state['players'][self.player_index]['units'][unit_index]['technology']['movement'] == 2:
            dist = abs(x_unit - x_opp) + abs(y_unit - y_opp)
            delta_x, delta_y = self.flank_direction
            reverse_flank_direction = (-delta_x, -delta_y)


            if unit['coords'] == myself['home_coords']:
                return self.flank_direction

            elif dist == 1:
                reverse_flank_direction
            else:
                translations.remove(self.flank_direction)

        best_translation = (0,0)
        smallest_distance_to_opponent = 999999999999
        for translation in translations:
            delta_x, delta_y = translation
            x = x_unit + delta_x
            y = x_unit + delta_y
            dist = abs(x - x_opp) + abs(y - y_opp)
            if dist < smallest_distance_to_opponent:
                best_translation = translation
                smallest_distance_to_opponent = dist

        return best_translation

    def decide_which_unit_to_attack(self, combat_state, coords, attacker_index):

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
        spawn_loc = game_state['players'][self.player_index]['home_coords']
        cp = game_state['players'][self.player_index]['cp']
        movement_tech = game_state['players'][self.player_index]['technology']['movement']
        move = ['movement',game_state['technology_data']['movement'][movement_tech]]
        ship_choice = move

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