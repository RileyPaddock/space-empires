# At the end of Turn 1 Movement Phase:

# Player 1 has 3 scouts at (4,0)
# Player 2 has 3 scouts at (4,4)
# At the end of Turn 1 Economic Phase:

# Player 1 has 3 scouts at (4,0) and 3 scouts at (2,0)
# Player 2 has 3 scouts at (4,4) and 3 scouts at (2,0)
# Players 1/2 have 2 CPs each
# At the end of Turn 2 Movement Phase:

# Player 1 has 6 scouts at (4,0)
# Player 2 has 6 scouts at (4,4)
# At the end of Turn 2 Economic Phase:

# Player 1 has 5 scouts at (4,0)
# Player 2 has 5 scouts at (4,4)
# Players 1/2 have 0 CPs each
# At the end of Turn 3 Movement Phase:

# Player 1 has 3 scouts at (4,0)
# Player 2 has 3 scouts at (4,4)
# At the end of Turn 3 Economic Phase:

# Player 1 has 3 scouts at (4,0)
# Player 2 has 3 scouts at (4,4)
# Players 1/2 have 0 CPs each
# At the end of Turn 4 Movement Phase:

# Player 1 has 3 scouts at (4,0)
# Player 2 has 3 scouts at (4,4)
# At the end of Turn 4 Economic Phase:

# Player 1 has 3 scouts at (4,0)
# Player 2 has 3 scouts at (4,4)
# Players 1/2 have 0 CPs each
correct_positions_p1 = [[(4,0)],[(4,0),(2,0)],[(4,0)],[(4,0)],[(4,0)],[(4,0)],[(4,0)],[(4,0)]]
correct_positions_p2 = [[(4,4)],[(4,4),(2,4)],[(4,4)],[(4,4)],[(4,4)],[(4,4)],[(4,4)],[(4,4)]]
correct_positions = [correct_positions_p1,correct_positions_p2]
correct_num_units = [[3],[3,3],[6],[5],[5],[3],[3],[3]]
import sys
sys.path.append('src')
from game import Game

def check(turn):
    correct_check = []
    for position_set in correct_positions:
        for i in range(len(position_set[turn])):
            for unit in g.players[correct_positions.index(position_set)].game_data[position_set[turn][i]]:
                if unit.unit_type == "Scout":
                    correct_check.append(unit)
            print("\nTesting Player "+str(correct_positions.index(position_set)+1)+" for "+str(correct_num_units[turn][i])+" Scouts at "+str(position_set[turn][i]))
            assert len(correct_check) == correct_num_units[turn][i],str(turn)+" "+str(len(correct_check))+" "+str(correct_num_units[turn][i])
            correct_check = []
            print("\nPassed")

g = Game(logging = False)
g.complete_movement_phase()
check(0)
g.complete_economic_phase()
check(1)
g.complete_movement_phase()
check(2)
g.complete_economic_phase()
check(3)
g.complete_movement_phase()
check(4)
g.complete_economic_phase()
check(5)
g.complete_movement_phase()
check(6)
g.complete_economic_phase()
check(7)

