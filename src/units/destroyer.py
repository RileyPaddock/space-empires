from units.unit import Unit 

class Destroyer(Unit):
    cost = 9
    attack_grade = 'D'
    strength = 4
    defense = 0
    class_num = 2
    shorthand = 'DE'
    unit_type = 'Destroyer'
    armor = 1
    speed = 1
    hull_size = 1
    ship_size = 2
    movement = 1

    def __init__(self, location, unit_num, player, technologies, game, turn_created):
        super().__init__(location, unit_num, player, technologies, game, turn_created)
        self.strength = self.strength + technologies['attack']
        self.defense += technologies['defense']
        self.movement = technologies['movement']
        self.maintenance = 1