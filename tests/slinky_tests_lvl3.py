import random
import math
import sys
sys.path.append('src')
from game import Game
from strategies.Level3.slinky_dev import BerserkerStrategy
from strategies.Level3.slinky_dev import StationaryStrategy


def run_game(strategy1, strategy2, game_num, games_with_logs = [0,1,2,3,4]):
    strats = {'Berserker':BerserkerStrategy ,'Stationary':StationaryStrategy}
    if game_num in games_with_logs:
        new_game = Game(logs = True, die_rolls = 'random', level = 1)
    else:
        new_game = Game(logs = False, die_rolls = 'random', level = 1)
    new_game.add_player(strats[strategy1](0), [3,0])
    new_game.add_player(strats[strategy2](1), [3,6])
    new_game.initialize_game()
    new_game.combat_engine.seed = random.seed(game_num+1)
    return new_game.run_to_completion()

for i in range(5):
    run_game('Berserker', 'Stationary',i)