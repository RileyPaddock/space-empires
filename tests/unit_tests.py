import random
import math
import sys
from imported_unit_strategies.strategies import Strategy
from imported_unit_strategies.initial_state import game_state as initial_state
from imported_unit_strategies.final_state import game_state as final_state
sys.path.append('src')
from game import Game



new_game = Game(logs = False, die_rolls = 'random', level = 1)
new_game.initialize_game()
new_game.set_game_state(initial_state,Strategy)
new_game.movement_phase.complete_economic_phase()
print(new_game.game_state())