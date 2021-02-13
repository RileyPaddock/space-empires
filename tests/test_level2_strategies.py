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


strategy_1 = AttackBerserkerLevel2
strategy_2 = DefenseBerserkerLevel2
strategy_3 = MovementBerserkerLevel2
strategy_4 = NumbersBerserkerLevel2
strategy_5 = FlankerStrategyLevel2

def run_game(strategy1, strategy2, game_num):
    strats = {'Attack':strategy_1, 'Defense':strategy_2, 'Movement':strategy_3, 'Numbers':strategy_4, 'Flank':strategy_5}
    new_game = Game(logs = False, die_rolls = 'random', level = 2)
    new_game.add_player(strats[strategy1](0), [2,0])
    new_game.add_player(strats[strategy2](1), [2,4])
    new_game.initialize_game()
    new_game.combat_engine.seed = random.seed(game_num+1)
    return new_game.run_to_completion()
    

results = []
for _ in range(10):
    winner = run_game('Numbers','Attack',_)
    if winner == 0:
        results.append('Numbers')
    elif winner == 1:
        results.append('Attack')
    else:
        results.append('Draw')

for _ in range(10):
    winner = run_game('Attack','Numbers',_+10)
    if winner == 0:
        results.append('Attack')
    elif winner == 1:
        results.append('Numbers')
    else:
        results.append('Draw')

print([i for i in range(len(results)) if results[i] == 'Numbers'])
print('- Numbers wins ' + str(results.count('Numbers')/len(results)) + '% of the time')
print('- Attack wins ' + str(results.count('Attack')/len(results)) + '% of the time')
print('- Draw wins ' + str(results.count('Draw')/len(results)) + '% of the time')