import random
import math
import sys
sys.path.append('src')
from game import Game
from strategies.Level3.riley_strategy_level_3 import RileyStrategy3
from strategies.Level3.numbers_berserker_level_3 import NumbersBerserkerLevel3


strategy_4 = NumbersBerserkerLevel3
strategy_6 = RileyStrategy3

def run_game(strategy1, strategy2, game_num):
    strats = {'Numbers':strategy_4, 'Riley':strategy_6}
    new_game = Game(logs = True, die_rolls = 'random', level = 3)
    new_game.add_player(strats[strategy1](0), [3,0])
    new_game.add_player(strats[strategy2](1), [3,6])
    new_game.initialize_game()
    new_game.combat_engine.seed = random.seed(game_num+1)
    return new_game.run_to_completion()
    

results = []
for _ in range(50):
    print(_)
    winner = run_game('Numbers','Riley',_)
    if winner == 0:
        results.append('Numbers')
    elif winner == 1:
        results.append('Riley')
    else:
        results.append('Draw')

for _ in range(50):
    print(_+50)
    winner = run_game('Riley','Numbers',_+50)
    if winner == 0:
        results.append('Riley')
    elif winner == 1:
        results.append('Numbers')
    else:
        results.append('Draw')


print('- Numbers wins ' + str(results.count('Numbers')/len(results)) + '% of the time')
print('- Riley wins ' + str(results.count('Riley')/len(results)) + '% of the time')
print('- Draw wins ' + str(results.count('Draw')/len(results)) + '% of the time')