correct_positions_p1 = [[(4, 0), (4, 0), (4, 0)], [(4, 0), (4, 0), (4, 0), (2, 0), (2, 0)], [(4, 0), (4, 0), (4, 0), (4, 0), (4, 0)], [(4, 0), (4, 0), (4, 0), (4, 0), (4, 0), (2, 0), (2, 0), (2, 0)], [(4, 0), (4, 0), (4, 0), (4, 0), (4, 0), (4, 0), (4, 0), (4, 0)], [(4, 0), (4, 0), (4, 0), (4, 0), (4, 0), (4, 0), (4, 0), (4, 0), (2, 0), (2, 0)], [(4, 0), (4, 0), (4, 0), (4, 0), (4, 0), (4, 0), (4, 0), (4, 0), (4, 0), (4, 0)], [(4, 0), (4, 0), (4, 0), (4, 0), (4, 0), (4, 0), (4, 0), (4, 0), (4, 0), (4, 0), (2, 0), (2, 0)]]

correct_positions_p2 = [[(4, 4), (4, 4), (4, 4)], [(4, 4), (4, 4), (4, 4), (2, 4), (2, 4)], [(4, 4), (4, 4), (4, 4), (4, 4), (4, 4)], [(4, 4), (4, 4), (4, 4), (4, 4), (4, 4), (2, 4), (2, 4), (2, 4)], [(4, 4), (4, 4), (4, 4), (4, 4), (4, 4), (4, 4), (4, 4), (4, 4)], [(4, 4), (4, 4), (4, 4), (4, 4), (4, 4), (4, 4), (4, 4), (4, 4), (2, 4), (2, 4)], [(4, 4), (4, 4), (4, 4), (4, 4), (4, 4), (4, 4), (4, 4), (4, 4), (4, 4), (4, 4)], [(4, 4), (4, 4), (4, 4), (4, 4), (4, 4), (4, 4), (4, 4), (4, 4), (4, 4), (4, 4), (2, 4), (2, 4)]]
correct_positions = [correct_positions_p1,correct_positions_p2]
import sys
sys.path.append('src')
from game import Game
from players.player import Player
from strategies.dumb_strategy import DumbStrategy
from board import Board
def check(turn):
    game_state = g.generate_state()
    player_0_scout_locations = [u['location'] for u in game_state['players'][0]['units'] if u['type'] == 'Scout']
    player_1_scout_locations = [u['location'] for u in game_state['players'][1]['units'] if u['type']== 'Scout']
    assert player_0_scout_locations == correct_positions[0][turn]
    assert player_1_scout_locations == correct_positions[1][turn]
b = Board([5,5])
p1 = Player(DumbStrategy(),(2,0),b)
p2 = Player(DumbStrategy(),(2,4),b)
g = Game(players = [p1,p2],board = b,logging = False)

for x in range(0,8,2):
    print("\n Testing Movement Phase "+str(x+1))
    g.complete_movement_phase()
    check(x)
    print("     passed")
    print("\n Testing Combat Phase "+str(x+1))
    g.complete_combat_phase()
    print("     passed")
    g.complete_economic_phase()
    print("\n Testing Economic Phase "+str(x+1))
    check(x+1)
    print("     passed")
    g.board.update_board()

