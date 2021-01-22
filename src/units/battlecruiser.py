from units.unit import Unit 

class Battlecruiser(Unit):
    cost = 15
    attack_grade = 'B'
    strength = 5
    defense = 1
    class_num = 4
    shorthand = 'BC'
    unit_type = 'Battlecruiser'
    armor = 2
    speed = 1
    hull_size = 2
    ship_size = 4
    movement = 1

    def __init__(self, location, unit_num, player, technologies, game, turn_created):
        super().__init__(location, unit_num, player, technologies, game, turn_created)
        self.strength = self.strength + technologies['attack']
        self.defense += technologies['defense']
        self.maintenance = 2