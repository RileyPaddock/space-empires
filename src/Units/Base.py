from Units.Unit import Unit

class Base(Unit):
    def __init__(self, team, location):
        super().__init__(team, location)
        self.unit_type = 'Base'
        self.price = 12
        self.attack_grade = 'A'
        self.strength = 7
        self.defense = 2
        self.shorthand = 'B'
        self.armor = 3
        self.hull_size = 3
