from player.player import Player
import random
from Units.scout import Scout
from Units.base import Base
from Units.battlecruiser import Battlecruiser
from Units.battleship import Battleship
from Units.colony_ship import ColonyShip
from Units.cruiser import Cruiser
from Units.decoy import Decoy
from Units.destroyer import Destroyer
from Units.dreadnaught import Dreadnaught
from Units.ship_yard import ShipYard
from Units.colony import Colony
from planet import Planet

class RandomPlayer(Player):
    def __init__(self, player_num, start_pos, game_data):
        super().__init__(player_num, start_pos, game_data)
        self.money = 20
        self.attack_tech = 0
        self.defense_tech = 0
        self.movement_tech = 1
        self.ship_yard_tech = 1
        self.ship_size_tech = 1
        self.shipyard_capacity = 0.5 + 0.5*self.ship_yard_tech
        self.save_goal = random.randint(6,70)
        self.generate_fleet()
    
    def generate_fleet(self):
        player_units = [Planet(self.start_pos), Colony(self.player_num,self.start_pos, [ShipYard(self.player_num, self.start_pos) for _ in range(4)],None),ColonyShip(self.player_num,self.start_pos),ColonyShip(self.player_num,self.start_pos),
                        Scout(self.player_num,self.start_pos),Scout(self.player_num,self.start_pos),
                        Scout(self.player_num,self.start_pos)]
        possible_units = ['Decoy', 'Scout', 'Colony']
        rand = random.randint(0, 2)
        while self.money - self.create_unit(possible_units[rand],self.start_pos).price > 0:
            player_units.append(self.create_unit(possible_units[rand],self.start_pos))
            self.money -= self.create_unit(possible_units[rand],self.start_pos).price

            if self.money - self.create_unit(possible_units[1],self.start_pos).price <= 0:
                rand = 0
            elif self.money - self.create_unit(possible_units[2],self.start_pos).price <= 0:
                rand = random.randint(0, 1)
            else:
                rand = random.randint(0,2)

        for unit in player_units:
            self.game_data[unit.location].append(unit)

    def spend(self):
        if self.money > self.save_goal:
                self.how_to_spend()
                self.save_goal = random.randint(6,70)

    def how_to_spend(self):
        while self.money >= 15:
            random.choice([self.get_new_ships(), self.tech_upgrade('attack'), self.tech_upgrade('defense'), self.tech_upgrade('movement'), self.tech_upgrade('ship yard'), self.tech_upgrade('ship size')])

    def get_rand_unit(self):
        units = [['Scout', 'Colony', 'Shipyard', 'Decoy'], ['Destroyer','Base'], ['Cruiser'], ['Battlecruiser'], ['Battleship'], ['Dreadnaught']]
        buildable_units = []
        for i in range(self.ship_size_tech):
            for unit in units[i]:
                buildable_units.append(unit)
        return buildable_units

    def get_new_ships(self):
        rand_unit = random.choice(self.get_rand_unit())
        if rand_unit == 'Shipyard':
            rand_colony = random.choice([colony for coord in self.game_data for colony in self.game_data[coord] if colony.unit_type == "Colony" and colony.location is not None])
            while rand_colony.location is None:
                rand_colony = random.choice([colony for coord in self.game_data for colony in self.game_data[coord] if colony.unit_type == "Colony" and colony.location is not None])
            rand_colony.shipyards.append(ShipYard(self.player_num, rand_colony.location))
            self.money -= ShipYard(self.player_num, rand_colony.location).price
        elif rand_unit == 'Base':
            rand_colony = random.choice([colony for coord in self.game_data for colony in self.game_data[coord] if colony.unit_type == "Colony" and colony.location is not None])
            while rand_colony.location is None:
                rand_colony = random.choice([colony for coord in self.game_data for colony in self.game_data[coord] if colony.unit_type == "Colony" and colony.location is not None])
            if not rand_colony.base:
                rand_colony.base = Base(self.player_num, rand_colony.location)
                for coord in self.game_data:
                    for colony in self.game_data[coord]:
                        if colony.location == rand_colony.location and colony.unit_type == "Colony":
                            colony.base = Base(self.player_num, rand_colony.location)
                self.money -= Base(self.player_num, rand_colony.location).price
        else:
            while True:
                rand_shipyard = random.choice(self.locate_colony_with_shipyard())
                if rand_shipyard.location is not None:
                    break
            shipyard_level = self.shipyard_capacity
            for colony in [colony for coord in self.game_data for colony in self.game_data[coord] if colony.unit_type == "Colony" and colony.location is not None]:
                for shipyard in colony.shipyards:
                    if shipyard.location == rand_shipyard.location:
                        shipyard_level+=self.shipyard_capacity
            if self.create_unit(rand_unit,rand_shipyard.location).hull_size <= shipyard_level:
                self.game_data[rand_shipyard.location].append(self.create_unit(rand_unit,rand_shipyard.location))
                self.money -= self.create_unit(rand_unit,rand_shipyard.location).price
    
    def tech_upgrade(self, upgrade_choice):
        attack_price = ((self.attack_tech + 2) * 10)
        defense_price = ((self.defense_tech + 2) * 10)
        movement_price = self.movement_calcs('price')
        ship_yard_price = ((self.ship_yard_tech + 1)*10)
        ship_size_price = ((self.ship_size_tech + 1)*5)
        
        if attack_price <= self.money and self.attack_tech < 3 and upgrade_choice == 'attack':
            self.money -= attack_price
            self.attack_tech += 1
            print("\n       Player "+str(self.player_num)+" upgraded thier attack technology to level "+str(self.attack_tech))
            

        if defense_price <= self.money and self.defense_tech < 3 and upgrade_choice == 'defense':
            self.money -= defense_price
            self.defense_tech += 1
            print("\n       Player "+str(self.player_num)+" upgraded thier defense technology to level "+str(self.defense_tech))


        if movement_price <= self.money and self.movement_tech < 6 and upgrade_choice == 'movement':
            self.money -= movement_price
            self.movement_tech += 1
            print("\n       Player "+str(self.player_num)+" upgraded thier movement technology to level "+str(self.movement_tech))

        if ship_yard_price <= self.money and self.ship_yard_tech < 3 and upgrade_choice == 'ship yard':
            self.money -= ship_yard_price
            self.ship_yard_tech += 1
            print("\n       Player "+str(self.player_num)+" upgraded thier shipyard technology to level "+str(self.ship_yard_tech))

        if ship_size_price <= self.money and self.ship_size_tech < 6 and upgrade_choice == 'ship size':
            self.money -= ship_size_price
            self.ship_size_tech += 1
            print("\n       Player "+str(self.player_num)+" upgraded thier ship size technology and can now build ships of hull size " + str(self.ship_size_tech)) 
    
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
        if unit.location[0] == 0 and unit.location[1] == 0:
            N = random.choice([1, 3, 5])
        elif unit.location[0] == 4 and unit.location[1] == 0:
            N = random.choice([2, 3, 5])
        elif unit.location[0] == 0 and unit.location[1] == 4:
            N = random.choice([1, 4, 5]) 
        elif unit.location[0] == 4 and unit.location[1] == 4:
            N = random.choice([2, 4, 5])
        elif unit.location[0] == 4:
            N = random.choice([2, 3, 4, 5])
        elif unit.location[0] == 0:
            N = random.choice([1, 3, 4, 5])
        elif unit.location[1] == 4:
            N = random.choice([1, 2, 4, 5])
        elif unit.location[1] == 0:
            N = random.choice([1, 2, 3, 5])
        else: 
            N = random.randint(1, 5)
        if N == 1:
            unit.location = (unit.location[0] + 1, unit.location[1])
        elif N == 2:
            unit.location = (unit.location[0] - 1, unit.location[1])
        elif N == 3:
            unit.location = (unit.location[0], unit.location[1] + 1)
        elif N == 4:
            unit.location = (unit.location[0], unit.location[1] - 1)
        elif N == 5:
            unit.location = unit.location
