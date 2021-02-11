from units.unit import Unit 

class Cruiser(Unit):
    cost = 12
    attack_grade = 'C'
    strength = 4
    defense = 1
    class_num = 3
    shorthand = 'C'
    unit_type = 'Cruiser'
    armor = 2
    hull_size = 3
    maintenance = 3
    ship_size = 2
    movement = 1

    def __init__(self, location, unit_num, player, technologies, game, turn_created):
        super().__init__(location, unit_num, player, technologies, game, turn_created)