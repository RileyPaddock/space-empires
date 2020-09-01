from units.unit import Unit

class Destroyer(Unit):
  def __init__(self, team, location, attack_tech, defense_tech,age = 0):
        super().__init__(team, location, age)
        self.attack_tech = attack_tech
        self.defense_tech = defense_tech
        self.unit_type = 'Destroyer'
        self.price = 9
        self.attack_grade = 'D'
        self.strength = 4
        self.defense = 0
        self.shorthand = 'DS'
        self.speed = 1
        self.armor = 1
        self.hull_size = 1
