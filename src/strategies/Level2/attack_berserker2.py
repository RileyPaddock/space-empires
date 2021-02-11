import sys
sys.path.append('src')
from strategies.Level1.beserker_strategy1 import BerserkerStrategyLevel1

class AttackBerserkerLevel2(BerserkerStrategyLevel1):
    def __init__(self,player_num):
        super().__init__(player_num)

    def decide_purchases(self,game_state):
        units = []
        tech = []
        sc = ['Scout',6] 
        spawn_loc = game_state['players'][self.player_num]['home_coords']
        cp = game_state['players'][self.player_num]['cp']
        attack_tech = game_state['players'][self.player_num]['technology']['attack']
        atk = ['attack',game_state['technology_data']['attack'][0]]
        ship_choice = atk

        while cp >= ship_choice[1]:
            if attack_tech<1:
                    attack_tech+=1
                    tech.append(ship_choice[0])
                    cp -= ship_choice[1]
                    ship_choice = sc
            else:
                units.append({'type':ship_choice[0], 'coords':spawn_loc})
                cp -= ship_choice[1]
                break

        return {'units':units,'technology':tech}