from units.unit import Unit 

class Dreadnaught(Unit):
    cost = 25
    attack_grade = 'A'
    strength = 6
    defense = 3
    class_num = 5
    shorthand = 'DR'
    unit_type = 'Dreadnaught'
    armor = 3
    speed = 1
    hull_size = 3
    ship_size = 6
    movement = 1
    maintenance = 3

    def __init__(self, location, unit_num, player, technologies, game, turn_created):
        super().__init__(location, unit_num, player, technologies, game, turn_created)