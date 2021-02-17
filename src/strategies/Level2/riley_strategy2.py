import sys
sys.path.append('src')
from strategies.Level1.beserker_strategy1 import BerserkerStrategyLevel1

class RileyStrategy2(BerserkerStrategyLevel1):
    def __init__(self,player_num):
        super().__init__(player_num)

    def decide_purchases(self,game_state):
        units = []
        tech = []
        ds = ['Destroyer',9]
        sc = ['Scout',6]
        spawn_loc = game_state['players'][self.player_num]['home_coords']
        cp = game_state['players'][self.player_num]['cp']
        ship_size_tech = game_state['players'][self.player_num]['technology']['shipsize']
        ss = ['shipsize', ((ship_size_tech)*5)]

        ship_choice = ss
        while cp >= ship_choice[1]:
            if ship_size_tech<2:
                ship_size_price = ((ship_size_tech)*5)
                if cp > ship_size_price:
                    ship_size_tech+=1
                    tech.append('shipsize')
                    cp -= ship_size_price
                if ship_size_tech == 2:
                    ship_choice = ds
            else:
                if cp >= ship_choice[1]:
                    units.append({'type':ship_choice[0], 'coords':spawn_loc})
                    cp -= ship_choice[1]
                    
                    if ship_choice == ds:
                        ship_choice = sc
                    elif ship_choice == sc:
                        ship_choice = ds 
        return {'units':units,'technology':tech}