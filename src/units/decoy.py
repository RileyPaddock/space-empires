from units.unit import Unit

class Decoy(Unit):
    
    def __init__(self, team, location, attack_tech, defense_tech, unit_num, age = 0):
        super().__init__(team, location, unit_num, age)
        self.attack_tech = attack_tech
        self.defense_tech = defense_tech
        self.unit_type = 'Decoy'
        self.price = 1
        self.shorthand = 'Dc'
        self.speed = 1
        self.attack_grade = ' '
        self.strength = ' '
        self.defense = ' '
        self.armor = ' '
        self.hull_size = 0

