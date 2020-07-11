import random
from Units.Scout import Scout
from Units.Base import Base
from Units.Battlecruiser import Battlecruiser
from Units.Battleship import Battleship
from Units.ColonyShip import ColonyShip
from Units.Cruiser import Cruiser
from Units.Decoy import Decoy
from Units.Destroyer import Destroyer
from Units.Dreadnaught import Dreadnaught
from Units.ShipYard import ShipYard

class Player:
    def __init__(self, player_num, start_pos):
        self.player_num = player_num
        self.start_pos = start_pos
        self.money = 20
        self.attack_tech = 0
        self.defense_tech = 0
        self.movement_tech = 1
        self.ship_yard_tech = 1
        self.ship_size_tech = 1
        self.shipyard_capacity = 0.5 + 0.5*self.ship_yard_tech
        self.colonies = []
        self.save_goal = random.randint(6,70)
        self.units = self.generate_fleet()
        
        




    def generate_fleet(self):
        player_units = [ColonyShip(self.player_num,self.start_pos),ColonyShip(self.player_num,self.start_pos),ColonyShip(self.player_num,self.start_pos),
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

        return player_units

    def locate_colony_with_shipyard(self):
        colonies_with_shipyard = []
        for colony in self.colonies:
            if len(colony.shipyards) > 0 :
                colonies_with_shipyard.append(colony)
        return colonies_with_shipyard

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
            rand_colony = random.choice(self.colonies)
            while rand_colony.location is None:
                rand_colony = random.choice(self.colonies)
            rand_colony.shipyards.append(ShipYard(self.player_num, rand_colony.location))
            self.money -= ShipYard(self.player_num, rand_colony.location).price
        elif rand_unit == 'Base':
            rand_colony = random.choice(self.colonies)
            while rand_colony.location is None:
                rand_colony = random.choice(self.colonies)
            if not rand_colony.base:
                rand_colony.base = Base(self.player_num, rand_colony.location)
                self.money -= Base(self.player_num, rand_colony.location).price
        else:
            while True:
                rand_shipyard = random.choice(self.locate_colony_with_shipyard())
                if rand_shipyard.location is not None:
                    break
            shipyard_level = self.shipyard_capacity
            for colony in self.colonies:
                for shipyard in colony.shipyards:
                    if shipyard.location == rand_shipyard.location:
                        shipyard_level+=self.shipyard_capacity
            if self.create_unit(rand_unit,rand_shipyard.location).hull_size <= shipyard_level:
                self.units.append(self.create_unit(rand_unit,rand_shipyard.location))
                self.money -= self.create_unit(rand_unit,rand_shipyard.location).price

    def create_unit(self, unit_type, location):
        print("\n       Player "+str(self.player_num)+" bought a new " + str(unit_type)+". It spawned at "+str(location))
        if unit_type == 'Scout':
            return Scout(self.player_num, location)
        elif unit_type == 'Destroyer':
            return Destroyer(self.player_num, location)
        elif unit_type == 'Cruiser':
            return Cruiser(self.player_num, location)
        elif unit_type == 'Battlecruiser':
            return Battlecruiser(self.player_num, location)
        elif unit_type == 'Battleship':
            return Battleship(self.player_num, location)
        elif unit_type == 'Dreadnaught':
            return Dreadnaught(self.player_num, location)
        elif unit_type == 'Colony':
            return ColonyShip(self.player_num, location)
        elif unit_type == 'Decoy':
            return Decoy(self.player_num, location)
        


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
            

        