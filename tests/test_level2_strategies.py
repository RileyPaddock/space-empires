import random
import math
import sys
sys.path.append('src')
from game import Game
from strategies.Level2.attack_berserker2 import AttackBerserkerLevel2
from strategies.Level2.defense_berserker2 import DefenseBerserkerLevel2
from strategies.Level2.movement_berserker2 import MovementBerserkerLevel2
from strategies.Level2.numbers_berserker2 import NumbersBerserkerLevel2
from strategies.Level2.flank_strategy2 import FlankerStrategyLevel2
from strategies.Level2.riley_strategy2 import RileyStrategy2


strategy_1 = AttackBerserkerLevel2
strategy_2 = DefenseBerserkerLevel2
strategy_3 = MovementBerserkerLevel2
strategy_4 = NumbersBerserkerLevel2
strategy_5 = FlankerStrategyLevel2
strategy_6 = RileyStrategy2

def run_game(strategy1, strategy2, game_num):
    strats = {'Attack':strategy_1, 'Defense':strategy_2, 'Movement':strategy_3, 'Numbers':strategy_4, 'Flank':strategy_5, 'Riley':strategy_6}
    new_game = Game(logs = False, die_rolls = 'random', level = 2)
    new_game.add_player(strats[strategy1](0), [2,0])
    new_game.add_player(strats[strategy2](1), [2,4])
    new_game.initialize_game()
    new_game.combat_engine.seed = random.seed(game_num+1)
    return new_game.run_to_completion()
    

results = []
for _ in range(500):
    winner = run_game('Numbers','Riley',_)
    if winner == 0:
        results.append('Numbers')
    elif winner == 1:
        results.append('Riley')
    else:
        results.append('Draw')

for _ in range(500):
    winner = run_game('Riley','Numbers',_+500)
    if winner == 0:
        results.append('Riley')
    elif winner == 1:
        results.append('Numbers')
    else:
        results.append('Draw')

actual_results = [elem for elem in results if elem != 'Draw']
print('- Numbers wins ' + str(actual_results.count('Numbers')/len(actual_results)) + '% of the time')
print('- Riley wins ' + str(actual_results.count('Riley')/len(actual_results)) + '% of the time')
print('- Draw wins ' + str(results.count('Draw')/len(results)) + '% of the time')