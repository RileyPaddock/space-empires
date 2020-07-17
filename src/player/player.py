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

class Player:
    def __init__(self, player_num, start_pos, game_data):
        self.player_num = player_num
        self.start_pos = start_pos
        self.game_data = game_data
        self.money = 20
        self.attack_tech = 0
        self.defense_tech = 0
        self.movement_tech = 1
        self.ship_yard_tech = 1
        self.ship_size_tech = 1
        self.shipyard_capacity = 0.5 + 0.5*self.ship_yard_tech
        self.save_goal = random.randint(6,70)
        
        




    def locate_colony_with_shipyard(self):
        colonies_with_shipyard = []
        colonies = [colony for coord in self.game_data for colony in self.game_data[coord] if colony.unit_type == "Colony" and colony.location is not None]
        for colony in colonies:
            if len(colony.shipyards) > 0 :
                colonies_with_shipyard.append(colony)
        return colonies_with_shipyard

    

    

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
            

        