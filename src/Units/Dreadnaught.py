from Units.Unit import Unit

class Dreadnaught(Unit):
    def __init__(self, team, location):
        super().__init__(team, location)
        self.unit_type = 'Dreadnaught'
        self.price = 24
        self.attack_grade = 'A'
        self.strength = 6
        self.defense = 3
        self.shorthand = 'DN'
        self.speed = 1
        self.armor = 3
        self.hull_size = 3
