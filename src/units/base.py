from units.unit import Unit

class Base(Unit):
    
    def __init__(self, team, location, attack_tech, defense_tech, unit_num, age = 0):
        super().__init__(team, location, unit_num, age)
        self.attack_tech = attack_tech
        self.defense_tech = defense_tech
        self.unit_type = 'Base'
        self.price = 12
        self.attack_grade = 'A'
        self.strength = 7
        self.defense = 2
        self.shorthand = 'B'
        self.armor = 3
        self.hull_size = 3


