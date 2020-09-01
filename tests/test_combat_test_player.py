import sys
sys.path.append('src')
from game import Game
g = Game(logging = False)
print("\nDescending Rolls")
print("\n   Testing Turn 1 Economic Phase")
g.complete_movement_phase()
g.complete_combat_phase()
g.complete_economic_phase()

print("\n       Testing Player 1 Money")
assert g.players[0].money == 0,"Player 1 Incorrect CP's after Turn 1"
print("\n       Passed")

print("\n       Testing Player 2 Money")
assert g.players[1].money == 3,"Player 2 Incorrect CP's after Turn 1"
print("\n       Passed")


print("\n   Testing Turn 2 Movement Phase")
g.complete_movement_phase()

print("\n       Testing Player 1 Unit Locations")
p1_scouts = [scout for scout in g.players[0].game_data[(2,2)] if scout.unit_type == "Scout" and scout.team == 1]
assert len(p1_scouts) == 2,"Player 1 Incorrect Scouts at (2,2)"

p1_destroyer = [dstr for dstr in g.players[0].game_data[(2,2)] if dstr.unit_type == "Destroyer" and dstr.team == 1]
assert len(p1_destroyer) == 2,"Player 1 Incorrect Destroyers at (2,2)"
print("\n       Passed")

print("\n       Testing Player 2 Unit Locations")
p2_destroyer = [dstr for dstr in g.players[1].game_data[(2,2)] if dstr.unit_type == "Destroyer" and dstr.team == 2]
assert len(p2_destroyer) == 2,"Player 2 Incorrect Destroyers at (2,2)"
print("\n       Passed")

p1_scouts = [scout for scout in g.players[1].game_data[(2,2)] if scout.unit_type == "Scout" and scout.team == 2]
assert len(p1_scouts) == 4,"Player 2 Incorrect Scouts at (2,2)"

print("\n   Testing Turn 2 Combat Phase")
g.complete_combat_phase()

print("\n       Testing Player 2 Unit Locations")
p2_destroyer = [dstr for dstr in g.players[1].game_data[(2,2)] if dstr.unit_type == "Destroyer" and dstr.team == 2]
assert len(p2_destroyer) == 2,"Player 2 Incorrect Destroyers at (2,2)"

p1_scouts = [scout for scout in g.players[1].game_data[(2,2)] if scout.unit_type == "Scout" and scout.team == 2]
assert len(p1_scouts) == 4,"Player 2 Incorrect Scouts at (2,2)"
print("\n       Passed")

print("\n       Testing Player 1 Unit Locations")
p1_units = [unit for unit in g.players[0].game_data[(2,2)] if (unit.unit_type == "Scout" or unit.unit_type == "Destroyer") and unit.team == 1]
assert len(p1_units) == 0,"Player 1 Incorrect Units at (2,2)"
print("\n       Passed")







h = Game(logging = False)
h.rolls = [1,2,3,4,5,6]
print("\nAscending Rolls")
print("\n   Testing Turn 1 Economic Phase")
h.complete_movement_phase()
h.complete_combat_phase()
h.complete_economic_phase()

print("\n       Testing Player 1 Money")
assert h.players[0].money == 3,"Player 1 Incorrect CP's after Turn 1"
print("\n       Passed")

print("\n       Testing Player 2 Money")
assert h.players[1].money == 0,"Player 2 Incorrect CP's after Turn 1"
print("\n       Passed")


print("\n   Testing Turn 2 Movement Phase")
h.complete_movement_phase()

print("\n       Testing Player 1 Unit Locations")
p1_scouts = [scout for scout in h.players[0].game_data[(2,2)] if scout.unit_type == "Scout" and scout.team == 1]
assert len(p1_scouts) == 4,"Player 1 Incorrect Scouts at (2,2)"

p1_destroyer = [dstr for dstr in h.players[0].game_data[(2,2)] if dstr.unit_type == "Destroyer" and dstr.team == 1]
assert len(p1_destroyer) == 2,"Player 1 Incorrect Destroyers at (2,2)"
print("\n       Passed")

print("\n       Testing Player 2 Unit Locations")
p2_destroyer = [dstr for dstr in h.players[1].game_data[(2,2)] if dstr.unit_type == "Destroyer" and dstr.team == 2]
assert len(p2_destroyer) == 2,"Player 2 Incorrect Destroyers at (2,2)"
print("\n       Passed")

p1_scouts = [scout for scout in h.players[1].game_data[(2,2)] if scout.unit_type == "Scout" and scout.team == 2]
assert len(p1_scouts) == 2,"Player 2 Incorrect Scouts at (2,2)"

print("\n   Testing Turn 2 Combat Phase")
h.complete_combat_phase()

print("\n       Testing Player 1 Unit Locations")
p1_destroyer = [dstr for dstr in h.players[0].game_data[(2,2)] if dstr.unit_type == "Destroyer" and dstr.team == 1]
assert len(p1_destroyer) == 2,"Player 1 Incorrect Destroyers at (2,2)"

p1_scouts = [scout for scout in h.players[0].game_data[(2,2)] if scout.unit_type == "Scout" and scout.team == 1]
assert len(p1_scouts) == 4,"Player 1 Incorrect Scouts at (2,2)"
print("\n       Passed")

print("\n       Testing Player 2 Unit Locations")
p2_units = [unit for unit in h.players[1].game_data[(2,2)] if (unit.unit_type == "Scout" or unit.unit_type == "Destroyer") and unit.team == 2]
assert len(p2_units) == 0,"Player 2 Incorrect Units at (2,2)"
print("\n       Passed")

