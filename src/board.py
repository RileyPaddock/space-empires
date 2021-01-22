from planet import Planet
import random
class Board:
    def __init__(self,size,spawns):
        self.size = size
        self.spawns = spawns
        self.game_data = {}
        self.planets = []
        self.set_up()
        self.generate_planets()

    def set_up(self):
        for x in range(self.size[0]):
            for y in range(self.size[1]):
                self.game_data[(x,y)] = []

    def generate_planets(self):
        for _ in range(8):
            rand_loc = (random.randint(0,self.size[0] - 1), random.randint(0, self.size[1] - 1))

            for unit in self.game_data[rand_loc]:
                if unit.unit_type == "Planet":
                    pass
            else:
                new_planet = Planet(rand_loc)
                self.planets.append(new_planet)

        for spawn in self.spawns:
            home_planet = Planet(spawn)
            self.planets.append(home_planet)

    def update_board(self, players):
        all_units = []
        for player in players:
            for unit in player.units:
                all_units.append(unit)
        for space in self.grid.values():
            space.units = []
            for unit in all_units:
                if unit.coords == space.coords:
                    space.units.append(unit)

    def get_all_active_data(self):
        board = {}
        for board_space in self.game_data:
            if len([unit for unit in self.game_data[board_space] if unit.unit_type != 'Planet']) >= 2:
                board[board_space] = [unit for unit in self.game_data[board_space] if unit.unit_type != 'Planet']
        return board