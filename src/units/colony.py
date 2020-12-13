from units.unit import Unit

class Colony(Unit):
    
    def __init__(self,team,location, attack_tech, defense_tech, unit_num,shipyards,base):
        super().__init__(team, location, unit_num)
        self.attack_tech = attack_tech
        self.defense_tech = defense_tech
        self.shipyards = shipyards
        self.base = base
        self.speed = 0
        self.armor = 3
        self.defense = 0
        self.strength = 0
        self.unit_type = 'Colony'
        self.shorthand = 'Col'
        self.attack_grade = 'Z'
        
        
