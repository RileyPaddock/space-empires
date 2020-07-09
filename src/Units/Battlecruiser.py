from Units.Unit import Unit

class Battlecruiser(Unit):
    def __init__(self, team, location):
        super().__init__(team, location)
        self.unit_type = 'Battlecruiser'
        self.price = 15
        self.attack_grade = 'B'
        self.strength = 5
        self.defense = 1
        self.shorthand = 'BC'
        self.speed = 1
        self.armor = 2
        self.hull_size = 2
