import random
import math
import sys
sys.path.append('src')
from game import Game
from strategies.Level3.riley_strategy_level_3 import RileyStrategyLevel3
from strategies.Level3.david_strategy_level_3 import DavidStrategyLevel3
from strategies.Level3.colby_strategy_level_3 import ColbyStrategyLevel3
from strategies.Level3.numbers_berserker_level_3 import NumbersBerserkerLevel3
from strategies.Level3.elijah_strategy_level_3 import ElijahStrategyLevel3
from strategies.Level3.george_strategy_level_3 import GeorgeStrategyLevel3

strategy_1 = GeorgeStrategyLevel3
strategy_2 = ElijahStrategyLevel3
strategy_3 = ColbyStrategyLevel3
strategy_5 = DavidStrategyLevel3
strategy_4 = NumbersBerserkerLevel3
strategy_6 = RileyStrategyLevel3

def run_game(strategy1, strategy2, game_num, games_with_logs = [0]):
    strats = {'George':strategy_1,'Elijah':strategy_2,'Colby':strategy_3,'Numbers':strategy_4, 'David': strategy_5, 'Riley':strategy_6}
    if game_num in games_with_logs:
        new_game = Game(logs = True, die_rolls = 'random', level = 3)
    else:
        new_game = Game(logs = False, die_rolls = 'random', level = 3)
    new_game.add_player(strats[strategy1](0), [3,0])
    new_game.add_player(strats[strategy2](1), [3,6])
    new_game.initialize_game()
    new_game.combat_engine.seed = random.seed(game_num+1)
    return new_game.run_to_completion()
    

def run_sims(p1, p2, num_matchups):
    results = []
    half = num_matchups//2
    for _ in range(half):
        winner = run_game(p1,p2,_)
        if winner == 0:
            results.append(p1)
        elif winner == 1:
            results.append(p2)
        else:
            results.append('Draw')

    for _ in range(half):
        winner = run_game(p2,p1,_+half)
        if winner == 0:
            results.append(p2)
        elif winner == 1:
            results.append(p1)
        else:
            results.append('Draw')


    print('- '+p1+' wins ' + str(results.count(p1)/len(results)*100) + '% of the time')
    print('- '+p2+' wins ' + str(results.count(p2)/len(results)*100) + '% of the time')
    print('- Draw wins ' + str(results.count('Draw')/len(results)*100) + '% of the time')

#print(run_game('George', 'Riley', 27, games_with_logs=[27]))

run_sims('Colby','George',100)
run_sims('Riley','Elijah',100)
run_sims('Numbers','David',100)
run_sims('Colby','Riley',100)
run_sims('Colby','Elijah',100)
run_sims('Colby','David',100)
run_sims('George','Riley',100)
run_sims('George','Elijah',100)
run_sims('George','David',100)
run_sims('Riley','David',100)
run_sims('Elijah','David',100)
run_sims('Numbers','Colby',100)
run_sims('Numbers','George',100)
run_sims('Numbers','Riley',100)
run_sims('Numbers','Elijah',100)
