from units.unit import Unit

class Cruiser(Unit):
    
    def __init__(self, team, location, attack_tech, defense_tech, unit_num, age = 0):
        super().__init__(team, location, unit_num, age)
        self.attack_tech = attack_tech
        self.defense_tech = defense_tech
        self.unit_type = 'Cruiser'
        self.price = 12
        self.attack_grade = 'C'
        self.strength = 4
        self.defense = 1
        self.shorthand = 'C'
        self.speed = 1
        self.armor = 2
        self.hull_size = 2

