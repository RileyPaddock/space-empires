import random
import math
import sys
sys.path.append('src')
from game import Game
from strategies.Level2.numbers_berserker2 import NumbersBerserkerLevel2
del sys.path[-1]

sys.path.append('imported_strategies')

from david_strategy_level_2 import DavidStrategyLevel2
from elijah_strategy_level_2 import ElijahStrategyLevel2
from george_strategy_level_2 import GeorgeStrategyLevel2
from justin_strategy_level_2 import JustinStrategyLevel2
from colby_strategy_level_2 import ColbyStrategyLevel2
from strategies.Level2.riley_strategy2 import RileyStrategy2


strategy_1 = DavidStrategyLevel2
strategy_2 = ElijahStrategyLevel2
strategy_3 = GeorgeStrategyLevel2
strategy_4 = JustinStrategyLevel2
strategy_5 = ColbyStrategyLevel2
strategy_6 = RileyStrategy2
strategy_7 = NumbersBerserkerLevel2

def run_game(strategy1, strategy2, game_num):
    strats = {'David':strategy_1, 'Elijah':strategy_2, 'George':strategy_3, 'Justin':strategy_4, 'Riley':strategy_6, 'Numbers':strategy_7}
    strats['Colby'] = strategy_5
    new_game = Game(logs = False, die_rolls = 'random', level = 2)
    new_game.add_player(strats[strategy1](0), [2,0])
    new_game.add_player(strats[strategy2](1), [2,4])
    new_game.initialize_game()
    new_game.combat_engine.seed = random.seed(game_num+1)
    return new_game.run_to_completion()
    

matchups = []
matchups = [('Numbers', 'David')]
print(matchups)

for p1,p2 in matchups:
    team = [p1,p2]
    print(p1+' v. '+p2)
    results = []
    for _ in range(250):
        winner = run_game(p1,p2,_)
        
        if winner == 0:
            #print(team[winner])
            results.append(0)
        elif winner == 1:
            #print(team[winner])
            results.append(1)
        else:
            #print('Draw')
            results.append(None)

    for _ in range(250):
        #print(_+250)
        winner = run_game(p2,p1,_+250)
        if winner == 0:
            results.append(1)
        elif winner == 1:
            results.append(0)
        else:
            results.append(None)

    print('     - '+p1+ ' wins ' + str(results.count(0)/len(results)) + '% of the time')
    print('     - '+p2+ ' wins ' + str(results.count(1)/len(results)) + '% of the time')
    print('     - Draw wins ' + str(results.count(None)/len(results)) + '% of the time')
    print("\n")