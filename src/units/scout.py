from units.unit import Unit 

class Scout(Unit):
    cost = 6
    attack_grade = 'E'
    strength = 3
    defense = 0
    class_num = 1
    shorthand = 'S'
    unit_type = 'Scout'
    armor = 1
    hull_size = 1
    maintenance = 1
    ship_size = 1
    movement = 1

    def __init__(self, location, unit_num, player, technologies, game, turn_created):
        super().__init__(location, unit_num, player, technologies, game, turn_created)
        self.strength = self.strength + technologies['attack']
        self.defense += technologies['defense']
        self.movement = technologies['movement']
        self.maintenance = 1