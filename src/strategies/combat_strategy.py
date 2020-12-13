class CombatStrategy:
    def __init__(self,player_num):
        self.player_num = player_num

    def will_colonize(self,colony_ship_loc,game_state):
        return False
    
    def decide_ship_movement(self,ship_index, game_state):
        ship = game_state['players'][self.player_num]['units'][ship_index]
        if ship['location'][0]>2:
            return (-1,0)
        elif ship['location'][0]<2:
             return (1,0)
        elif ship['location'][1]>2:
             return (0,-1)
        elif ship['location'][1]<2:
             return (0,1)
        else:
            return (0,0)
    
    def decide_purchases(self,game_state):
        units = []
        tech = []
        ds = ['Destroyer',9]
        sc = ['Scout',6] 
        ship_choice = ds
        cp = game_state['players'][self.player_num-1]['cp']
        ship_size_tech = game_state['players'][self.player_num-1]['technology']['ship_size'][0]
        while cp >= ship_choice[1]:
            if ship_size_tech<2:
                ship_size_price = ((ship_size_tech + 1)*5)
                if cp > ship_size_price:
                    ship_size_tech+=1
                    tech.append('ship_size')
                    cp -= ship_size_price
            else:
                if cp >= ship_choice[1]:
                    units.append(ship_choice[0])
                    cp -= ship_choice[1]
                    
                    if ship_choice == ds:
                        ship_choice = sc
                    elif ship_choice == sc:
                        ship_choice = ds
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

    def decide_which_unit_to_attack(self, attacking_ship_index, combat_state):
        for entry in combat_state:
            if entry['player'] != combat_state['order'][attacking_ship_index]['team']:
                return combat_state.index(entry)

    def decide_which_units_to_screen(self, combat_state):
        return []