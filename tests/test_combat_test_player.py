import sys
sys.path.append('src')
from game import Game
from players.player import Player
from strategies.combat_strategy import CombatStrategy
from board import Board
from units.scout import Scout
from imported_strategies.colby_combat_strategy import CombatStrategy as CCS
from imported_strategies.elijah_combat_strategy import CombatStrategy as ECS
from imported_strategies.george_combat_strategy import CombatStrategy as GCS
from imported_strategies.david_combat_strategy import CombatStrategy as DCS

print('ASCENDING TESTS')

print('TURN 1 Economic')

new_game = Game(logging = False, die_rolls = 'ascending')
# strategy_1 = DCS(0)
# strategy_2 = DCS(1)
strategy_1 = CombatStrategy(0)
strategy_2 = CombatStrategy(1)
# strategy_1 = ECS(0)
# strategy_2 = ECS(1)
# strategy_1 = GCS(player_num = 0)
# strategy_2 = GCS(player_num = 1)
# strategy_1 = CCS(0)
# strategy_2 = CCS(1)
new_game.add_player(strategy_1, [2,0])
new_game.add_player(strategy_2, [2,4])
new_game.initialize_game()
new_game.complete_turn()
location = [2,2]

new_or_non_moveable = [[2,0], [2,4]]

p1_scouts = []

def return_scouts(game_state, player_index):
    return [unit for unit in game_state['players'][player_index]['units'] if unit['type'] == 'Scout']
def return_destroyers(game_state, player_index):
    return [unit for unit in game_state['players'][player_index]['units'] if unit['type'] == 'Destroyer']
def return_ship_size_tech(game_state, player_index):
    return game_state['players'][player_index]['tech']['shipsize']
def return_cp(game_state, player_index):
    return game_state['players'][player_index]['cp']

def check_unit_coords(units, coords):
    for unit in units:
        assert unit['coords'] == coords

assert return_cp(new_game.game_state(), 0) == 7, return_cp(new_game.game_state(), 0)
assert return_cp(new_game.game_state(), 1) == 1, return_cp(new_game.game_state(), 1)
print('Passed')

print('TURN 2 Movement')
new_game.complete_movement_phase()
check_unit_coords(return_scouts(new_game.game_state(), 0), [2,2])
assert len(return_scouts(new_game.game_state(), 0)) == 3
check_unit_coords(return_destroyers(new_game.game_state(), 0), [2,2])
assert len(return_destroyers(new_game.game_state(), 0)) == 0
check_unit_coords(return_destroyers(new_game.game_state(), 1), [2,2])
assert len(return_destroyers(new_game.game_state(), 1)) == 1

print('Passed')

print('TURN 2 Combat')
new_game.complete_combat_phase()
check_unit_coords(return_scouts(new_game.game_state(), 0), [2,2])
assert len(return_scouts(new_game.game_state(), 0)) == 1
check_unit_coords(return_destroyers(new_game.game_state(), 0), [2,2])
assert len(return_destroyers(new_game.game_state(), 0)) == 0
check_unit_coords(return_destroyers(new_game.game_state(), 1), [2,2])
assert len(return_destroyers(new_game.game_state(), 1)) == 0

print('Passed')


print('DESCENDING TESTS')

new_game = Game(logging = False, die_rolls = 'descending')
strategy_1 = CombatStrategy(player_num = 0)
strategy_2 = CombatStrategy(player_num = 1)
new_game.add_player(strategy_1, [2,0])
new_game.add_player(strategy_2, [2,4])
new_game.initialize_game()
new_game.complete_many_turns(1)

print('TURN 1 Economic')

assert return_cp(new_game.game_state(), 0) == 1
assert return_cp(new_game.game_state(), 1) == 7
print('Passed')

print('TURN 2 Movement')
new_game.complete_movement_phase()
check_unit_coords(return_scouts(new_game.game_state(), 1), [2,2])
assert len(return_scouts(new_game.game_state(), 1)) == 3
check_unit_coords(return_destroyers(new_game.game_state(), 1), [2,2])
assert len(return_destroyers(new_game.game_state(), 1)) == 0
check_unit_coords(return_destroyers(new_game.game_state(), 0), [2,2])
assert len(return_destroyers(new_game.game_state(), 0)) == 1

print('Passed')

print('TURN 2 Combat')
new_game.complete_combat_phase()
check_unit_coords(return_scouts(new_game.game_state(), 1), [2,2])
assert len(return_scouts(new_game.game_state(), 1)) == 3
check_unit_coords(return_destroyers(new_game.game_state(), 1), [2,2])
assert len(return_destroyers(new_game.game_state(), 1)) == 0
check_unit_coords(return_destroyers(new_game.game_state(), 0), [2,2])
assert len(return_destroyers(new_game.game_state(), 0)) == 0

print('Passed')