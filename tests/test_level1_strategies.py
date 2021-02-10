import random
import math
import sys
sys.path.append('src')
from game import Game
from strategies.Level1.dumb_strategy1 import DumbStrategyLevel1
from strategies.Level1.random_strategy1 import RandomStrategyLevel1
from strategies.Level1.beserker_strategy1 import BerserkerStrategyLevel1
from strategies.Level1.flank_strategy import FlankerStrategyLevel1
from strategies.riley_strategy import RileyStrategy


strategy_1 = DumbStrategyLevel1
strategy_2 = RandomStrategyLevel1
strategy_3 = BerserkerStrategyLevel1
strategy_4 = FlankerStrategyLevel1
strategy_5 = RileyStrategy

def run_game(strategy1, strategy2, game_num):
    strats = {'Dumb':DumbStrategyLevel1, 'Random':RandomStrategyLevel1, 'Berserker':BerserkerStrategyLevel1, 'Flanker':FlankerStrategyLevel1, 'Riley':RileyStrategy}
    new_game = Game(logs = False, die_rolls = 'random', level = 1)
    new_game.add_player(strats[strategy1](0), [2,0])
    new_game.add_player(strats[strategy2](1), [2,4])
    new_game.initialize_game()
    new_game.combat_engine.seed = random.seed(game_num+1)
    new_game.run_to_completion()
    return strategy1 if new_game.winner == 0 else strategy2


print('Flanker vs Berserker: ')
results = []
loss_indices = []
for _ in range(10):
    winner = run_game('Flanker','Berserker',_)
    results.append(winner)
    if winner == 'Flanker':
        loss_indices.append(_)

for _ in range(10):
    winner = run_game('Berserker','Flanker',_+10)
    results.append(winner)
    if winner == 'Flanker':
        loss_indices.append(_+10)

print('- Flanker wins ' + str(results.count('Flanker')/len(results)) + '% of the time')
print('- Berserker wins ' + str(results.count('Berserker')/len(results)) + '% of the time')
print(loss_indices)

