from Units.Unit import Unit

class Battleship(Unit):
    def __init__(self, team, location):
        super().__init__(team, location)
        self.unit_type = 'Battleship'
        self.price = 20
        self.attack_grade = 'A'
        self.strength = 5
        self.defense = 2
        self.shorthand = 'BS'
        self.speed = 1
        self.armor = 3
        self.hull_size = 3
