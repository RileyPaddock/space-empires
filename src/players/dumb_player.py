from players.player import Player
from units.scout import Scout
from units.ship_yard import ShipYard
from units.colony import Colony
from planet import Planet

class DumbPlayer(Player):
    def __init__(self, player_num, start_pos, board,logging):
        super().__init__(player_num, start_pos, board,logging)
        self.player_type = "dumb"
        self.num_turns = 0
        self.money = 0
        self.attack_tech = 0
        self.defense_tech = 0
        self.movement_tech = 1
        self.ship_yard_tech = 1
        self.ship_size_tech = 1
        self.shipyard_capacity = 0.5 + 0.5*self.ship_yard_tech
        self.generate_fleet()

    def generate_fleet(self):
        units = [Planet(self.start_pos), Colony(self.player_num,self.start_pos,self.attack_tech, self.defense_tech, [ShipYard(self.player_num, self.start_pos) for _ in range(4)],None),Scout(self.player_num, self.start_pos,self.attack_tech, self.defense_tech),Scout(self.player_num, self.start_pos,self.attack_tech, self.defense_tech),Scout(self.player_num, self.start_pos,self.attack_tech, self.defense_tech)]
        for unit in units:
            self.board.game_data[unit.location].append(unit)
    
    def spend(self):
        units = []
        while self.money - 6 >= 0:
            units.append(Scout(self.player_num, self.start_pos,self.attack_tech, self.defense_tech))
            if self.logging:
                print("\n       Player "+str(self.player_num)+" bought a new Scout. It spawned at "+str(self.start_pos))
            self.money -= 6
        for unit in units:
            self.board.game_data[unit.location].append(unit)
            if self.logging:
                print(self.board.game_data[unit.location])

    def get_movement_phases(self):
            if self.movement_tech == 1:
                return (1,1,1)
            elif self.movement_tech == 2:
                return (1,1,2)
            elif self.movement_tech == 3:
                return (1,2,2)
            elif self.movement_tech == 4:
                return (2,2,2)
            elif self.movement_tech == 5:
                return (2,2,3)
            elif self.movement_tech == 6:
                return (2,3,3)

    def get_movement_price(self):
            if self.movement_tech < 4:
                return (self.movement_tech + 1)*10
            else:
                return 40

    def move_player_units(self):
        for i in range(len(self.movement_calcs('movements'))):
            if self.logging:
                print("\n Player "+str(self.player_num)+" - Move " + str(i+1))
            for coord in self.board.game_data:
                for unit in self.board.game_data[coord]:
                    if unit.unit_type != 'Planet' and unit.unit_type != 'Colony' and unit.team == self.player_num and unit.location is not None:
                        if unit.unit_type == 'Colony Ship':
                            self.move_unit(unit)
                        else:
                            old_loc = unit.location
                            for i in range(self.movement_calcs('movements')[i]):
                                self.move_unit(unit)
                            if unit.location is not None and unit.location != old_loc and self.logging:
                                print("\n   Unit "+str(self.board.game_data[coord].index(unit))+" ("+str(unit.unit_type)+") moves from "+str(old_loc)+" to "+str(unit.location))
                            elif unit.location is not None and self.logging:
                                print("\n   Unit "+str(self.board.game_data[coord].index(unit))+" ("+str(unit.unit_type)+") did not move from"+str(unit.location))

    def move_unit(self, unit):
        if unit.location[0] != 4:
           unit.move('right')

    def will_colonize(self):
        return False