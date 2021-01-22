from units.unit import Unit 

class Decoy(Unit):
    cost = 1
    strength = 0          
    defense = 0
    unit_type = 'Decoy'
    shorthand = 'Dc'
    class_num = 0
    armor = 0
    attack_grade = 'Z'
    hull_size = 0
    maintenance = None
    can_atk = False
    instant_ko = True
    ship_size = 1
    movement = 1