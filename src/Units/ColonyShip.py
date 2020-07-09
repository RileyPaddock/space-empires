from Units.Unit import Unit

class ColonyShip(Unit):
    def __init__(self,team,location):
        super().__init__(team, location)
        self.unit_type = 'Colony Ship'
        self.shorthand = 'CS'
        self.attack_grade = 'Z'
        self.price = 8
        self.speed = 1
        self.armor = 1
        self.hull_size = 1
        self.defense = 0
        self.strength = 0
