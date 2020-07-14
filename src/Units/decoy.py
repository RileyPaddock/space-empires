from Units.unit import Unit

class Decoy(Unit):
    def __init__(self,team, location):
        super().__init__(team,location)
        self.unit_type = 'Decoy'
        self.price = 1
        self.shorthand = 'Dc'
        self.speed = 1
        self.attack_grade = ' '
        self.strength = ' '
        self.defense = ' '
        self.armor = ' '
        self.hull_size = 0
