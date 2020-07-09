from Units.Unit import Unit

class Cruiser(Unit):
    def __init__(self, team, location):
        super().__init__(team, location)
        self.unit_type = 'Cruiser'
        self.price = 12
        self.attack_grade = 'C'
        self.strength = 4
        self.defense = 1
        self.shorthand = 'C'
        self.speed = 1
        self.armor = 2
        self.hull_size = 2
