from Units.unit import Unit

class Scout(Unit):
  def __init__(self, team, location):
        super().__init__(team, location)
        self.unit_type = 'Scout'
        self.price = 6
        self.attack_grade = 'E'
        self.strength = 3
        self.defense = 0
        self.shorthand = 'S'
        self.speed = 1
        self.armor = 1
        self.hull_size = 1
