from players.player import Player
import random
from units.scout import Scout
from units.ship_yard import ShipYard
from units.colony_ship import ColonyShip
from units.colony import Colony
from planet import Planet

class CombatTestPlayer(Player):
    def __init__(self, player_num, start_pos, game_data,logging):
        super().__init__(player_num, start_pos, game_data,logging)
        self.player_type = 'combat'
        self.money = 20
        self.attack_tech = 0
        self.defense_tech = 0
        self.movement_tech = 1
        self.ship_yard_tech = 1
        self.ship_size_tech = 1
        self.shipyard_capacity = 0.5 + 0.5*self.ship_yard_tech
        self.ship_choice = 'Destroyer'
        self.generate_fleet()
    
    def generate_fleet(self):
        units = [Planet(self.start_pos), Colony(self.player_num,self.start_pos,self.attack_tech, self.defense_tech, [ShipYard(self.player_num, self.start_pos) for _ in range(4)],None),ColonyShip(self.player_num,self.start_pos,self.attack_tech,self.defense_tech),ColonyShip(self.player_num,self.start_pos,self.attack_tech,self.defense_tech),Scout(self.player_num,self.start_pos,self.defense_tech,self.attack_tech),Scout(self.player_num,self.start_pos,self.defense_tech,self.attack_tech),Scout(self.player_num,self.start_pos,self.defense_tech,self.attack_tech)]
        
        for unit in units:
            self.game_data[unit.location].append(unit)
    
    def spend(self):
        while self.money >= self.create_unit(self.ship_choice,self.start_pos, logging = False).price:
            if self.ship_size_tech<2:
                ship_size_price = ((self.ship_size_tech + 1)*5)
                if self.money > ship_size_price:
                    self.ship_size_tech+=1
                    self.money -= ship_size_price
                    if self.logging:
                        print("\n       Player "+str(self.player_num)+" upgraded thier ship size technology and can now build ships of hull size " + str(self.ship_size_tech)) 
            else:
                rand_colony = random.choice(self.locate_colonies_with_shipyard())
                if self.money >= self.create_unit(self.ship_choice,rand_colony.location,logging = False).price:
                    self.game_data[rand_colony.location].append(self.create_unit(self.ship_choice,rand_colony.location))
                    self.money -= self.create_unit(self.ship_choice,rand_colony.location,logging = False).price
                    
                    if self.create_unit(self.ship_choice,rand_colony.location,logging = False).unit_type == 'Scout':
                        self.ship_choice = 'Destroyer'
                    elif self.create_unit(self.ship_choice,rand_colony.location,logging = False).unit_type == 'Destroyer':
                        self.ship_choice = 'Scout'
        if self.logging:
            print("\n   Player "+str(self.player_num)+" Money: "+str(self.money))



    def move_player_units(self):
        for i in range(len(self.get_movement_phases())):
            if self.logging:
                print("\n Player "+str(self.player_num)+" - Move " + str(i+1))
            for coord in self.game_data:
                for unit in self.game_data[coord]:
                    if unit.unit_type != 'Planet' and unit.unit_type != 'Colony' and unit.team == self.player_num and unit.location is not None:
                        if unit.unit_type == 'Colony Ship':
                            old_loc = unit.location
                            self.move_unit(unit)
                            if self.logging:
                                if unit.location != old_loc:
                                    print("\n   Unit "+str(self.game_data[coord].index(unit))+" ("+str(unit.unit_type)+") moves from "+str(old_loc)+" to "+str(unit.location))
                                else:
                                    print("\n   Unit "+str(self.game_data[coord].index(unit))+" ("+str(unit.unit_type)+") did not move from "+str(old_loc))
                        else:
                            old_loc = unit.location
                            for i in range(self.get_movement_phases()[i]):
                                self.move_unit(unit)
                            if unit.location is not None and unit.location != old_loc and self.logging:
                                print("\n   Unit "+str(self.game_data[coord].index(unit))+" ("+str(unit.unit_type)+") moves from "+str(old_loc)+" to "+str(unit.location))
                            elif unit.location is not None and self.logging:
                                print("\n   Unit "+str(self.game_data[coord].index(unit))+" ("+str(unit.unit_type)+") did not move from"+str(unit.location))

    def move_unit(self, unit):
        if unit.location[0]>2:
            unit.move('left')
        elif unit.location[0]<2:
            unit.move('right')
        elif unit.location[1]>2:
            unit.move('down')
        elif unit.location[1]<2:
            unit.move('up')
    
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