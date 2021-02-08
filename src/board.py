from planet import Planet
import random
class Board:
    def __init__(self,size,game, spawns, level):
        self.size = size
        self.game = game
        self.spawns = spawns
        self.level = level
        self.game_data = {}
        self.planets = []
        self.set_up()
        self.generate_planets()

    def set_up(self):
        for x in range(self.size[0]):
            for y in range(self.size[1]):
                self.game_data[(x,y)] = []

    def generate_planets(self):
        for spawn in self.spawns:
            new_planet = Planet(spawn)
            self.planets.append(new_planet)
        if self.level > 2:
            while len(self.planets) < 8:
                rand_loc = (random.randint(0,self.size[0] - 1), random.randint(0, self.size[1] - 1))

                if rand_loc not in [planet.location for planet in self.planets]:
                    new_planet = Planet(rand_loc)
                    self.planets.append(new_planet)

    def update(self, players):
        all_units = []
        for player in players:
            for unit in player.units:
                all_units.append(unit)
        for space in self.game_data:
            self.game_data[space] = []
            for unit in all_units:
                if tuple(unit.location) == space:
                    self.game_data[space].append(unit)

    def get_all_active_data(self):
        board = {}
        for board_space in self.game_data:
            if len([unit for unit in self.game_data[board_space]]) >= 2:
                board[board_space] = [unit for unit in self.game_data[board_space] if unit.unit_type != 'Planet']
        return board