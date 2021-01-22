from units.unit import Unit 

class Battleship(Unit):
    cost = 20
    attack_grade = 'A'
    strength = 5
    defense = 2
    class_num = 5
    shorthand = 'BS'
    unit_type = 'Battleship'
    armor = 3
    speed = 1
    hull_size = 3
    ship_size = 5
    movement = 1

    def __init__(self, location, unit_num, player, technologies, game, turn_created):
        super().__init__(location, unit_num, player, technologies, game, turn_created)
        self.strength = self.strength + technologies['attack']
        self.defense += technologies['defense']
        self.maintenance = 3