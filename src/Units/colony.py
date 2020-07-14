from Units.unit import Unit

class Colony(Unit):
    def __init__(self,team,location,shipyards,base):
        super().__init__(team, location)
        self.shipyards = shipyards
        self.base = base
        self.unit_type = 'Colony'
        self.shorthand = 'Col'
        self.attack_grade = 'Z'
        self.speed = 0
        self.armor = 3
        self.defense = 0
        self.strength = 0
