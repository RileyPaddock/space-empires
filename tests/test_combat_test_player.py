import sys
sys.path.append('src')
from game import Game
g = Game(logging = False)

print("\nTesting Turn 1 Economic Phase")
g.complete_movement_phase()
g.complete_combat_phase()
g.complete_economic_phase()

print("\n   Testing Player 1 Money")
assert g.players[0].money == 1,"Player 1 Incorrect CP's after Turn 1"
print("\n   Passed")

print("\n   Testing Player 2 Money")
assert g.players[1].money == 4,"Player 2 Incorrect CP's after Turn 1"
print("\n   Passed")

print("\n   Testing Player 1 Unit Locations")
p1_scouts = [scout for scout in g.players[0].game_data[(2,2)] if scout.unit_type == "Scout"]
assert len(p1_scouts) == 3,"Player 1 Incorrect Scouts at (2,2)"

p1_destroyer = [dstr for dstr in g.players[0].game_data[(2,0)] if dstr.unit_type == "Destroyer"]
assert len(p1_destroyer) == 1,"Player 1 Incorrect Destroyers at (2,4)"
print("\n   Passed")

print("\n   Testing Player 2 Unit Locations")
p2_destroyer = [dstr for dstr in g.players[1].game_data[(2,4)] if dstr.unit_type == "Destroyer"]
assert len(p2_destroyer) == 1,"Player 2 Incorrect Destroyers at (2,4)"
print("\n   Passed")


print("\nTesting Turn 2 Movement Phase")
g.complete_movement_phase()

print("\n   Testing Player 1 Unit Locations")
p1_units = [unit for unit in g.players[0].game_data[(2,2)] if (unit.unit_type == 'Scout' or unit.unit_type == 'Destroyer') and unit.team == 1]
assert len(p1_units) == 4,"Player 1 incorrect Units at (2,2)"
print("\n   Passed")

print("\n   Testing Player 2 Unit Locations")
p2_units = [unit for unit in g.players[1].game_data[(2,2)] if (unit.unit_type == 'Scout' or unit.unit_type == 'Destroyer') and unit.team == 2]
assert len(p2_units) == 1,"Player 2 incorrect Units at (2,2)"
print("\n   Passed")

print("\nTesting Turn 2 Combat Phase")
g.complete_combat_phase()

print("\n   Testing Player 1 Unit Locations")
p1_units = [unit for unit in g.players[0].game_data[(2,2)] if (unit.unit_type == 'Scout' or unit.unit_type == 'Destroyer') and unit.team == 1]
assert len(p1_units) == 4,"Player 1 incorrect Units at (2,2)"

print("\n   Testing Player 2 Unit Locations")
p2_units = [unit for coord in g.players[1].game_data for unit in g.players[1].game_data[coord] if (unit.unit_type == 'Scout' or unit.unit_type == 'Destroyer') and unit.team == 2]
assert len(p2_units) == 0,"Player 2 incorrect units"


print("\nTesting Turn 2 Economic Phase")
g.complete_economic_phase()

print("\n   Testing Player 1 Money")
assert g.players[0].money == 0,"Player 1 Incorrect CP's after Turn 1"
print("\n   Passed")

print("\n   Testing Player 2 Money")
assert g.players[1].money == 1,"Player 2 Incorrect CP's after Turn 1"
print("\n   Passed")

print("\n   Testing Player 1 Unit Locations")
p1_scouts = [scout for scout in g.players[0].game_data[(2,2)] if scout.unit_type == "Scout"]
assert len(p1_scouts) == 3,"Player 1 Incorrect Scouts at (2,2)"

p1_destroyer = [dstr for dstr in g.players[0].game_data[(2,2)] if dstr.unit_type == "Destroyer"]
assert len(p1_destroyer) == 1,"Player 1 Incorrect Destroyers at (2,2)"
print("\n   Passed")

print("\n   Testing Player 2 Unit Locations")
p2_destroyer = [dstr for dstr in g.players[1].game_data[(2,4)] if dstr.unit_type == "Scout"]
assert len(p2_destroyer) == 1,"Player 2 Incorrect Scouts at (2,4)"
print("\n   Passed")

print("\nTesting Turn 3 Movement Phase")
g.complete_movement_phase()

print("\n   Testing Player 1 Unit Locations")
p1_units = [unit for unit in g.players[0].game_data[(2,2)] if (unit.unit_type == 'Scout' or unit.unit_type == 'Destroyer') and unit.team == 1]
assert len(p1_units) == 4,"Player 1 incorrect Units at (2,2)"
print("\n   Passed")

print("\n   Testing Player 2 Unit Locations")
p2_units = [unit for unit in g.players[1].game_data[(2,2)] if (unit.unit_type == 'Scout' or unit.unit_type == 'Destroyer') and unit.team == 2]
assert len(p2_units) == 1,"Player 2 incorrect Units at (2,2)"
print("\n   Passed")

print("\nTesting Turn 3 Combat Phase")
g.complete_combat_phase()

print("\n   Testing Player 1 Unit Locations")
p1_units = [unit for unit in g.players[0].game_data[(2,2)] if (unit.unit_type == 'Scout' or unit.unit_type == 'Destroyer') and unit.team == 1]
assert len(p1_units) == 4,"Player 1 incorrect Units at (2,2)"

print("\n   Testing Player 2 Unit Locations")
p2_units = [unit for coord in g.players[1].game_data for unit in g.players[1].game_data[coord] if (unit.unit_type == 'Scout' or unit.unit_type == 'Destroyer') and unit.team == 2]
assert len(p2_units) == 0,"Player 2 incorrect units"


print("\nTesting Turn 3 Economic Phase")
g.complete_economic_phase()

print("\n   Testing Player 1 Money")
assert g.players[0].money == 0,"Player 1 Incorrect CP's after Turn 1"
print("\n   Passed")

print("\n   Testing Player 2 Money")
assert g.players[1].money == 4,"Player 2 Incorrect CP's after Turn 1"
print("\n   Passed")

print("\n   Testing Player 1 Unit Locations")
p1_scouts = [scout for scout in g.players[0].game_data[(2,2)] if scout.unit_type == "Scout"]
assert len(p1_scouts) == 2,"Player 1 Incorrect Scouts at (2,2)"

p1_destroyer = [dstr for dstr in g.players[0].game_data[(2,2)] if dstr.unit_type == "Destroyer"]
assert len(p1_destroyer) == 1,"Player 1 Incorrect Destroyers at (2,2)"
print("\n   Passed")

print("\n   Testing Player 2 Unit Locations")
p2_destroyer = [dstr for dstr in g.players[1].game_data[(2,4)] if dstr.unit_type == "Scout"]
assert len(p2_destroyer) == 0,"Player 2 Incorrect Scouts at (2,4)"
print("\n   Passed")


# At the end of Turn 3 Economic Phase:

# Player 1 has 0 CP, 2 scouts and 1 destroyer at (2,0).
# Player 2 has 4 CP, no ships other than its home colony/shipyards
