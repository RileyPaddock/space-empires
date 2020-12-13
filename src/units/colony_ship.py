from units.unit import Unit

class ColonyShip(Unit):
    
    def __init__(self, team, location, attack_tech, defense_tech, unit_num, age = 0):
        super().__init__(team, location, unit_num, age)
        self.attack_tech = attack_tech
        self.defense_tech = defense_tech
        self.unit_type = 'Colony Ship'
        self.shorthand = 'CS'
        self.attack_grade = 'Z'
        self.price = 8
        self.speed = 1
        self.armor = 1
        self.hull_size = 1
        self.defense = 0
        self.strength = 0

