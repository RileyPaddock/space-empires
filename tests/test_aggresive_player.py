import sys
# sys.path.append('imported_strategies')
# from colby_dumb_strategy import DumbStrategy as colby_dumb
# from elijah_dumb_strategy import DumbStrategy as eli_dumb
# from david_dumb_strategy import DumbStrategy as david_dumb
# from george_dumb_strategy import DumbStrategy as george_dumb
# del sys.path[-1]
sys.path.append('src')
from players.player import Player
from units.unit import Unit
from units.scout import Scout
from units.colony_ship import ColonyShip
from units.colony import Colony
from game import Game
from board import Board
from planet import Planet
from strategies.aggresive_strategy import AggresiveStrategy

new_game = Game(logging = False, die_rolls = 'ascending')
strategy_1 = AggresiveStrategy(0)
strategy_2 = AggresiveStrategy(1)
new_game.add_player(strategy_1, [2,0])
new_game.add_player(strategy_2, [2,4])
new_game.initialize_game()
new_game.run_to_completion()

new_game = Game(logging = False, die_rolls = 'descending')
strategy_1 = AggresiveStrategy(0)
strategy_2 = AggresiveStrategy(1)
new_game.add_player(strategy_1, [2,0])
new_game.add_player(strategy_2, [2,4])
new_game.initialize_game()
new_game.run_to_completion()