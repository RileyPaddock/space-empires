from units.unit import Unit 

class ShipYard(Unit):
    attack_grade = 'C'
    class_num = 3
    strength = 3
    defense = 0
    armor = 1
    cost = 6
    unit_type = 'Shipyard'
    shorthand = 'SY'
    ship_size = 0
    build_capacity = 1
    hull_size = 0
    maintenance = None
    moveable = False
    
    def __init__(self, location, unit_num, player, technologies, game, turn_created):
        super().__init__(location, unit_num, player, technologies, game, turn_created)
        self.colony = self.find_colony()
        self.colony.shipyards.append(self)

    def find_colony(self):
        found = None
        for unit in self.player.units:
            if unit.unit_type == 'Colony':
                if unit.location == self.location:
                    found = unit
                    return unit

    def destroy(self):
        self.alive = False
        if self in self.player.units:
            self.player.units.remove(self)
        self.colony.set_builders()