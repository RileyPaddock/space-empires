from units.unit import Unit

class ShipYard(Unit):
    
    def __init__(self,team,location,unit_num):
        super().__init__(team,location,unit_num)
        self.unit_type = 'Ship yard'
        self.shorthand = 'SY'
        self.attack_grade = 'C'
        self.strength = 3
        self.defense = 0
        self.price = 6
        self.hull_size = 1
        
