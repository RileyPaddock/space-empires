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

import sys
sys.path.append('src')
from game import Game
g = Game()
while g.num_turns<5:
    g.complete_movement_phase()
    g.complete_economic_phase()
