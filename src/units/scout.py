from units.unit import Unit

class Scout(Unit):
    
    def __init__(self, team, location, attack_tech, defense_tech,age = 0):
        super().__init__(team, location, age)
        self.attack_tech = attack_tech
        self.defense_tech = defense_tech
        self.unit_type = 'Scout'
        self.price = 6
        self.attack_grade = 'E'
        self.strength = 3
        self.defense = 0
        self.shorthand = 'S'
        self.speed = 1
        self.armor = 1
        self.hull_size = 1
        
