from units.unit import Unit

class Dreadnaught(Unit):
    
    def __init__(self, team, location, attack_tech, defense_tech,age = 0):
        super().__init__(team, location, age)
        self.attack_tech = attack_tech
        self.defense_tech = defense_tech
        self.unit_type = 'Dreadnaught'
        self.price = 24
        self.attack_grade = 'A'
        self.strength = 6
        self.defense = 3
        self.shorthand = 'DN'
        self.speed = 1
        self.armor = 3
        self.hull_size = 3

