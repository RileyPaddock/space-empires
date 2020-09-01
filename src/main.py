from game import Game
g = Game(logging = True)
g.rolls = [1,2,3,4,5,6]
g.complete_movement_phase()
g.complete_combat_phase()
g.complete_economic_phase()
g.complete_movement_phase()
g.complete_combat_phase()

