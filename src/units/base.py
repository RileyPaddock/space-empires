from units.unit import Unit 

class Base(Unit):
    attack_grade = 'A'
    hull_size = 2
    class_num = 5
    strength = 7
    defense = 2
    armor = 3
    cost = 12
    ship_size = 2
    unit_type = 'Base'
    shorthand = 'B'
    can_move = False
    maintenance = None
    
    def __init__(self, location, unit_num, player, technologies, game, turn_created):
        super().__init__(location, unit_num, player, technologies, game, turn_created)
        self.colony = self.find_colony()
        self.colony.base = self

    def find_colony(self):
        found = None
        for unit in self.player.units:
            if unit.unit_typw == 'Colony':
                if unit.location == self.location:
                    found = unit
                    return unit