from units.unit import Unit

class Battlecruiser(Unit):
    def __init__(self, team, location, attack_tech, defense_tech,age = 0):
        super().__init__(team, location, age)
        self.attack_tech = attack_tech
        self.defense_tech = defense_tech
        self.unit_type = 'Battlecruiser'
        self.price = 15
        self.attack_grade = 'B'
        self.strength = 5
        self.defense = 1
        self.shorthand = 'BC'
        self.speed = 1
        self.armor = 2
        self.hull_size = 2