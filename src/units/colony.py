from units.unit import Unit 

class Colony(Unit):
    strength = 0
    unit_type = 'Colony'
    class_num = 0
    defense = 1
    armor = 3
    capacity = 3
    moveable = False
    maintenance = None
    can_atk = False
    ship_size_needed = 0
    
    def __init__(self, location, unit_num, player, technologies, game, turn_created, colony_type = 'Normal'):
        super().__init__(location, unit_num, player, technologies, game, turn_created)
        self.base = None
        self.shipyards = []
        self.builders = 0
        self.colony_type = colony_type
        self.defense += technologies['defense']
        if colony_type == 'Home':
            self.capacity = 20

    def hit(self):
        if self.armor > 0:
            self.armor -= 1
            self.capacity -= 1
        else:
            self.destroy()

    def destroy(self):
        planet = self.player.home_planet
        planet.destroy()
        self.alive = False
        if self in self.player.units:
            self.player.units.remove(self)

    def set_builders(self):
        self.builders = 0
        for shipyard in self.shipyards:
            self.builders += shipyard.build_capacity