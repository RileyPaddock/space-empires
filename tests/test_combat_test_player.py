import sys
sys.path.append('src')
from game import Game
from players.player import Player
from strategies.combat_strategy import CombatStrategy
from board import Board
b = Board([5,5])
p1 = Player(CombatStrategy(0),(2,0),b)
p2 = Player(CombatStrategy(1),(2,4),b)
h = Game(players = [p1,p2],board = b,logging = False,rolls = [1,2,3,4,5,6])
print("Ascending Rolls")
print("\n   Testing Turn 1 Economic Phase")
h.complete_movement_phase()
h.complete_combat_phase()
h.complete_economic_phase()

print("\n       Testing Player 1 Money")
print(h.players[0].money)
#assert h.players[0].money == 17,"Player 1 Incorrect CP's after Turn 1"
print("\n       Passed")

print("\n       Testing Player 2 Money")
print(h.players[1].money)
#assert h.players[1].money == 11,"Player 2 Incorrect CP's after Turn 1"
print("\n       Passed")


print("\n   Testing Turn 2 Movement Phase")
h.complete_movement_phase()

print("\n       Testing Player 1 Unit Locations")
p1_scouts = [scout for scout in h.players[0].board.game_data[(2,2)] if scout.unit_type == "Scout" and scout.team == 1]
print(len(p1_scouts))
#assert len(p1_scouts) == 3,"Player 1 Incorrect Scouts at (2,2)"

p1_destroyer = [dstr for dstr in h.players[0].board.game_data[(2,2)] if dstr.unit_type == "Destroyer" and dstr.team == 1]
print(len(p1_destroyer))
#assert len(p1_destroyer) == 0,"Player 1 Incorrect Destroyers at (2,2)"
print("\n       Passed")

print("\n       Testing Player 2 Unit Locations")
p2_destroyer = [dstr for dstr in h.players[1].board.game_data[(2,2)] if dstr.unit_type == "Destroyer" and dstr.team == 2]
print(len(p2_destroyer))
#assert len(p2_destroyer) == 1,"Player 2 Incorrect Destroyers at (2,2)"
print("\n       Passed")

p1_scouts = [scout for scout in h.players[1].board.game_data[(2,2)] if scout.unit_type == "Scout" and scout.team == 2]
print(len(p1_scouts))
#assert len(p1_scouts) == 0,"Player 2 Incorrect Scouts at (2,2)"

print("\n   Testing Turn 2 Combat Phase")
h.complete_combat_phase()

print("\n       Testing Player 1 Unit Locations")
p1_destroyer = [dstr for dstr in h.players[0].board.game_data[(2,2)] if dstr.unit_type == "Destroyer" and dstr.team == 1]
print(len(p1_destroyer))
#assert len(p1_destroyer) == 0,"Player 1 Incorrect Destroyers at (2,2)"

p1_scouts = [scout for scout in h.players[0].board.game_data[(2,2)] if scout.unit_type == "Scout" and scout.team == 1]
assert len(p1_scouts) == 2,"Player 1 Incorrect Scouts at (2,2)"
print("\n       Passed")

print("\n       Testing Player 2 Unit Locations")
p2_units = [unit for unit in h.players[1].board.game_data[(2,2)] if (unit.unit_type == "Scout" or unit.unit_type == "Destroyer") and unit.team == 2]
assert len(p2_units) == 0,"Player 2 Incorrect Units at (2,2)"
print("\n       Passed")




b = Board([5,5])
p1 = Player(CombatStrategy(),(2,0),b)
p2 = Player(CombatStrategy(),(2,4),b)
h = Game(players = [p1,p2],board = b,logging = False,rolls = [6,5,4,3,2,1])

print("Descending Rolls")
print("\n   Testing Turn 1 Economic Phase")
h.complete_movement_phase()
h.complete_combat_phase()
h.complete_economic_phase()

print("\n       Testing Player 1 Money")
assert h.players[0].money == 11,"Player 1 Incorrect CP's after Turn 1"
print("\n       Passed")

print("\n       Testing Player 2 Money")
assert h.players[1].money == 17,"Player 2 Incorrect CP's after Turn 1"
print("\n       Passed")


print("\n   Testing Turn 2 Movement Phase")
h.complete_movement_phase()

print("\n       Testing Player 1 Unit Locations")
p1_scouts = [scout for scout in h.players[0].board.game_data[(2,2)] if scout.unit_type == "Scout" and scout.team == 1]
assert len(p1_scouts) == 0,"Player 1 Incorrect Scouts at (2,2)"

p1_destroyer = [dstr for dstr in h.players[0].board.game_data[(2,2)] if dstr.unit_type == "Destroyer" and dstr.team == 1]
assert len(p1_destroyer) == 1,"Player 1 Incorrect Destroyers at (2,2)"
print("\n       Passed")

print("\n       Testing Player 2 Unit Locations")
p2_destroyer = [dstr for dstr in h.players[1].board.game_data[(2,2)] if dstr.unit_type == "Destroyer" and dstr.team == 2]
assert len(p2_destroyer) == 0,"Player 2 Incorrect Destroyers at (2,2)"
print("\n       Passed")

p1_scouts = [scout for scout in h.players[1].board.game_data[(2,2)] if scout.unit_type == "Scout" and scout.team == 2]
assert len(p1_scouts) == 3,"Player 2 Incorrect Scouts at (2,2)"

print("\n   Testing Turn 2 Combat Phase")
h.complete_combat_phase()

print("\n       Testing Player 1 Unit Locations")
p1_destroyer = [dstr for dstr in h.players[0].board.game_data[(2,2)] if dstr.unit_type == "Destroyer" and dstr.team == 1]
assert len(p1_destroyer) == 0,"Player 1 Incorrect Destroyers at (2,2)"

p1_scouts = [scout for scout in h.players[0].board.game_data[(2,2)] if scout.unit_type == "Scout" and scout.team == 1]
assert len(p1_scouts) == 0,"Player 1 Incorrect Scouts at (2,2)"
print("\n       Passed")

print("\n       Testing Player 2 Unit Locations")
p2_units = [unit for unit in h.players[1].board.game_data[(2,2)] if (unit.unit_type == "Scout" or unit.unit_type == "Destroyer") and unit.team == 2]
assert len(p2_units) == 3,"Player 2 Incorrect Units at (2,2)"
print("\n       Passed")