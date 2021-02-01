class RileyStategy:
    def __init__(self,player_index):
        self.player_index = player_index

    def will_colonize_planet(self,colony_ship_loc,game_state):
        enemy_base = game_state['players'][0 if self.player_index == 1 else 1]
        if self.calc_distance(enemy_base, colony_ship_loc) > 2:
            return True
        else:
            return False
    
    def decide_ship_movement(self,ship_index, game_state):
        ship = game_state['players'][self.player_index]['units'][ship_index]
        if ship['coords'][0] != game_state['board_size'][0]-1:
           return (1, 0)
        else:
            return (0,0)
    
    def decide_purchase(self, cp, ship_size_tech):
        ds = ['Destroyer',9]
        sc = ['Scout',6] 
        cr = ['Cruiser', 12]
        ss = ['shipsize', ((ship_size_tech)*5)]

        if ship_size_tech<2:
            return ss
        elif cp >= 12:
            return cr
        elif cp >= 9:
            return ds
        else:
            return sc

    def decide_purchases(self,game_state):
        units = []
        tech = []

        spawn_loc = game_state['players'][self.player_num]['home_coords']
        cp = game_state['players'][self.player_num]['cp']
        ship_size_tech = game_state['players'][self.player_num]['technology']['shipsize']

        if 'Base' not in [unit['type'] for unit in self.game_state['players'][player_num]['units']]:
            ship_choice = ['Base', 12]
        ship_choice = self.decide_purchase(self, cp, ship_size_tech)

        while cp >= ship_choice[1]:
            if ship_size_tech<2:
                ship_size_price = ((ship_size_tech)*5)
                if cp > ship_size_price:
                    ship_size_tech+=1
                    tech.append('shipsize')
                    cp -= ship_size_price
                
            else:
                if cp >= ship_choice[1]:
                    units.append({'type':ship_choice[0], 'coords':spawn_loc})
                    cp -= ship_choice[1]
                    
                    ship_choice = self.decide_purchase(self, cp, ship_size_tech)

        return {'units':units,'technology':tech}
    
    def decide_removals(self, game_state):
        i = 0
        while True:
            if game_state['players'][self.player_index]['units'][i]['alive']:
                return game_state['players'][self.player_index]['units'][i]['unit_num']
            else:
                i+=1

    def decide_which_unit_to_attack(self, combat_state, location, attacking_ship_index):
        for entry in combat_state[location]:
            if entry['player'] != combat_state[location][attacking_ship_index]['player']:
                return combat_state[location].index(entry)

    def decide_which_units_to_screen(self, combat_state):
        return []

    def calc_distance(self,unit1_loc, unit2_loc):
        return (((unit1_loc[0]-unit2_loc[0])**2) + ((unit1_loc[1] - unit2_loc[1])**2))**(0.5)