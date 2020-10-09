from planet import Planet
import random
class Board:
    def __init__(self,size):
        self.size = size
        self.game_data = {}
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
                self.game_data[rand_loc].append(Planet(rand_loc))

    def update_board(self):
            temp = self.game_data
            self.game_data = {}
            for x in range(5):
                for y in range(5):
                    self.game_data[(x,y)] = []
            for elem in temp:
                for unit in temp[elem]:
                    if unit.location is not None:
                        self.game_data[unit.location].append(unit)

            for coord in self.game_data:
                for planet in self.game_data[coord]:
                    if planet.unit_type == 'Planet' and planet.has_a_colony:
                        if planet.colony.location == None:
                            planet.reset()