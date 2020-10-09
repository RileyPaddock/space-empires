# correct_positions_p1 = [[(4,0)],[(4,0),(2,0)],[(4,0)],[(4,0)],[(4,0)],[(4,0)],[(4,0)],[(4,0)]]
# correct_positions_p2 = [[(4,4)],[(4,4),(2,4)],[(4,4)],[(4,4)],[(4,4)],[(4,4)],[(4,4)],[(4,4)]]
# correct_positions = [correct_positions_p1,correct_positions_p2]
# correct_num_units = [[3],[3,2],[5],[5],[8],[8],[10],[10]]
import sys
sys.path.append('src')
from game import Game

# def check(turn):
#     correct_check = []
#     for position_set in correct_positions:
#         for i in range(len(position_set[turn])):
#             for unit in g.players[correct_positions.index(position_set)].game_data[position_set[turn][i]]:
#                 if unit.unit_type == "Scout":
#                     correct_check.append(unit)
#             print("\nTesting Player "+str(correct_positions.index(position_set)+1)+" for "+str(correct_num_units[turn][i])+" Scouts at "+str(position_set[turn][i]))
#             assert len(correct_check) == correct_num_units[turn][i],str(turn)+" "+str(len(correct_check))+" "+str(correct_num_units[turn][i])
#             correct_check = []
#             print("\nPassed")

# g = Game(rolls = 'random',players = ['Dumb','Dumb'],logging = False)
# g.complete_movement_phase()
# check(0)
# g.complete_economic_phase()
# check(1)
# g.complete_movement_phase()
# check(2)
# g.complete_economic_phase()
# check(3)
# g.complete_movement_phase()
# check(4)
# g.complete_economic_phase()
# check(5)
# g.complete_movement_phase()
# check(6)
# g.complete_economic_phase()
# check(7)

g = Game(rolls = 'random',players = ['Dumb','Dumb'],logging = False)
print(g.generate_state('red',g.players[0]))

