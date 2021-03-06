import sys
sys.path.append('src')
from strategies.Level1.beserker_strategy1 import BerserkerStrategyLevel1

class DefenseBerserkerLevel2(BerserkerStrategyLevel1):
    def __init__(self,player_num):
        super().__init__(player_num)

    def decide_purchases(self,game_state):
        units = []
        tech = []
        sc = ['Scout',6] 
        spawn_loc = game_state['players'][self.player_num]['home_coords']
        cp = game_state['players'][self.player_num]['cp']
        defense_tech = game_state['players'][self.player_num]['technology']['defense']
        d_fence = ['defense',game_state['technology_data']['defense'][defense_tech]]
        ship_choice = d_fence

        while cp >= ship_choice[1]:
            if defense_tech<1:
                    defense_tech+=1
                    tech.append(ship_choice[0])
                    cp -= ship_choice[1]
                    ship_choice = sc
            else:
                units.append({'type':ship_choice[0], 'coords':spawn_loc})
                cp -= ship_choice[1]
        return {'units':units,'technology':tech}