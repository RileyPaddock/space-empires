from player.player import Player
from Units.scout import Scout
from Units.ship_yard import ShipYard
from Units.colony import Colony
from planet import Planet

class DumbPlayer(Player):
    def __init__(self, player_num, start_pos, game_data):
        super().__init__(player_num, start_pos, game_data)
        self.money = 20
        self.attack_tech = 0
        self.defense_tech = 0
        self.movement_tech = 1
        self.ship_yard_tech = 1
        self.ship_size_tech = 1
        self.shipyard_capacity = 0.5 + 0.5*self.ship_yard_tech
        self.generate_fleet()

    def generate_fleet(self):
        units = [Planet(self.start_pos), Colony(self.player_num,self.start_pos, [ShipYard(self.player_num, self.start_pos) for _ in range(4)],None),Scout(self.player_num, self.start_pos),Scout(self.player_num, self.start_pos),Scout(self.player_num, self.start_pos)]
        for unit in units:
            self.game_data[unit.location].append(unit)
    
    def spend(self):
        units = []
        while self.money - 6 >= 0:
            units.append(Scout(self.player_num, self.start_pos))
            print("\n       Player "+str(self.player_num)+" bought a new Scout. It spawned at "+str(self.start_pos))
            self.money -= 6
        for unit in units:
            self.game_data[unit.location].append(unit)
            print(self.game_data[unit.location])
    def movement_calcs(self, output):
        if output == 'price':
            if self.movement_tech < 4:
                return (self.movement_tech + 1)*10
            else:
                return 40
        elif output == 'movements':
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


    def movement(self):
        for i in range(len(self.movement_calcs('movements'))):
            print("\n Player "+str(self.player_num)+" - Move " + str(i+1))
            for coord in self.game_data:
                for unit in self.game_data[coord]:
                    if unit.unit_type != 'Planet' and unit.unit_type != 'Colony' and unit.team == self.player_num and unit.location is not None:
                        if unit.unit_type == 'Colony Ship':
                            self.move(unit)
                        else:
                            old_loc = unit.location
                            for i in range(self.movement_calcs('movements')[i]):
                                self.move(unit)
                            if unit.location is not None and unit.location != old_loc:
                                print("\n   Unit "+str(self.game_data[coord].index(unit))+" ("+str(unit.unit_type)+") moves from "+str(old_loc)+" to "+str(unit.location))
                            elif unit.location is not None:
                                print("\n   Unit "+str(self.game_data[coord].index(unit))+" ("+str(unit.unit_type)+") did not move from"+str(unit.location))

    def move(self, unit):
        if unit.location[0] != 4:
           unit.location = (unit.location[0]+1,unit.location[1])