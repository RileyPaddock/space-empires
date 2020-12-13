from units.scout import Scout
from units.base import Base
from units.battlecruiser import Battlecruiser
from units.battleship import Battleship
from units.colony_ship import ColonyShip
from units.cruiser import Cruiser
from units.decoy import Decoy
from units.destroyer import Destroyer
from units.dreadnaught import Dreadnaught
from units.ship_yard import ShipYard
from units.colony import Colony
from planet import Planet

class Player():
    def __init__(self, strategy, start_pos, board, player_num = 0,logging = True):
        self.strategy = strategy
        self.player_num = player_num
        self.start_pos = start_pos
        self.board = board
        self.logging = logging
        self.num_turns = 0
        self.money = 0
        self.units = []
        self.tech = {'attack':(0,3),'defense':(0,3),'movement':(1,6),'ship_yard':(1,3),'ship_size':(1,6)}
        self.shipyard_capacity = 0.5 + 0.5*self.tech['ship_yard'][0]

    def generate_fleet(self):
        units = [Planet(self.start_pos), Colony(self.player_num,self.start_pos,self.tech['attack'][0], self.tech['defense'][0],0, [ShipYard(self.player_num, self.start_pos,i+1) for i in range(4)],None),Scout(self.player_num, self.start_pos,self.tech['attack'][0], self.tech['defense'][0],5),Scout(self.player_num, self.start_pos,self.tech['attack'][0], self.tech['defense'][0],6),Scout(self.player_num, self.start_pos,self.tech['attack'][0], self.tech['defense'][0],7),ColonyShip(self.player_num, self.start_pos,self.tech['attack'][0], self.tech['defense'][0],8),ColonyShip(self.player_num, self.start_pos,self.tech['attack'][0], self.tech['defense'][0],9),ColonyShip(self.player_num, self.start_pos,self.tech['attack'][0], self.tech['defense'][0],10)]
        self.units = units
        for unit in units:
            self.board.game_data[unit.location].append(unit)
    
    def player_state(self):
        player_state = {}
        player_state['cp'] = self.money
        player_state['technology'] = self.tech
        player_state['units'] = [unit.unit_state() for unit in self.units if unit.unit_type != 'Planet' and unit.location != None]
        return player_state
    
    def spend(self,game_state):
        wanted_purchases = self.strategy.decide_purchases(game_state,self.player_num)
        units = []
        for unit in wanted_purchases['units']:
            cost = self.create_unit(unit,self.start_pos,False).price
            if self.money - cost >= 0:
                units.append(self.create_unit(unit,self.start_pos))
                if self.logging:
                    print("\n       Player "+str(self.player_num)+" bought a new "+str(unit)+". It spawned at "+str(self.start_pos))
            self.money -= cost

        for tech in wanted_purchases['tech']:
            self.tech_upgrade(tech)

        for unit in units:
            self.units.append(unit)
            self.board.game_data[unit.location].append(unit)

    def tech_upgrade(self, upgrade_choice):
        tech_costs = {'attack':((self.tech['attack'] + 2) * 10)
        ,'defense':((self.tech['defense'] + 2) * 10),
        'movement':self.get_movement_price('movements'),
        'ship_yard':((self.tech['ship_yard'] + 1)*10),
        'ship_size':((self.tech['ship_size'] + 1)*5)}

        if tech_costs[upgrade_choice] <= self.money and self.tech[upgrade_choice][0]<self.tech[upgrade_choice][1]:
            self.money -= tech_costs[upgrade_choice]
            self.tech[upgrade_choice][0]+=1
            if self.logging:
                print("\n       Player "+str(self.player_num)+" upgraded thier "+str(upgrade_choice)+" technology to level "+str(self.tech[upgrade_choice][0])) 

    def get_movement_phases(self):
            if self.tech['movement'][0] == 1:
                return (1,1,1)
            elif self.tech['movement'][0] == 2:
                return (1,1,2)
            elif self.tech['movement'][0] == 3:
                return (1,2,2)
            elif self.tech['movement'][0] == 4:
                return (2,2,2)
            elif self.tech['movement'][0] == 5:
                return (2,2,3)
            elif self.tech['movement'][0] == 6:
                return (2,3,3)

    def get_movement_price(self):
            if self.tech['movement'][0] < 4:
                return (self.tech['movement'][0] + 1)*10
            else:
                return 40

    def move_player_units(self,game_state):
        for i in range(len(self.get_movement_phases())):
            if self.logging:
                print("\n Player "+str(self.player_num)+" - Move " + str(i+1))
            for coord in self.board.game_data:
                for unit in self.board.game_data[coord]:
                    if unit.unit_type != 'Planet' and unit.unit_type != 'Colony' and unit.team == self.player_num and unit.location is not None:
                        old_loc = unit.location
                        if unit.unit_type == 'Colony Ship':
                            new_loc = self.movement_from_translation(self.strategy.decide_ship_movement(unit.unit_num,game_state))
                            unit.location = new_loc
                        else:
                            old_loc = unit.location
                            for i in range(self.get_movement_phases()[i]):
                               new_loc = self.movement_from_translation(self.strategy.decide_ship_movement(unit.unit_num,game_state))
                               unit.location = new_loc
                        self.board.update_board()
                        if unit.location is not None and unit.location != old_loc and self.logging:
                            print("\n   Unit "+str(unit.unit_num)+" ("+str(unit.unit_type)+") moves from "+str(old_loc)+" to "+str(unit.location))
                        elif unit.location is not None and self.logging:
                            print("\n   Unit "+str(self.board.game_data[coord].index(unit))+" ("+str(unit.unit_type)+") did not move from"+str(unit.location))

    def will_colonize(self,colony_ship,game_state):
        return self.strategy.will_colonize(self,colony_ship.location, game_state)



    def locate_colonies_with_shipyard(self):
        colonies_with_shipyard = []
        colonies = [colony for coord in self.board.game_data for colony in self.board.game_data[coord] if colony.unit_type == "Colony" and colony.location is not None and colony.team == self.player_num]
        for colony in colonies:
            if len(colony.shipyards) > 0 and colony.location is not None:
                colonies_with_shipyard.append(colony)
        return colonies_with_shipyard

    def decide_removals(self,game_state):
        removals = self.strategy.removals(game_state)
        for i in removals:
            self.units[i].location = None
            self.board.update_board()

    def movement_from_translation(self,ship,translation):
        return [ship.location[i]+ translation[i] for i in range(len(translation))]

    def decide_which_ships_to_attack(self,ship,combat_state):
        return self.strategy.decide_which_ships_to_attack(self,ship,combat_state)

    def create_unit(self, unit_type, location, logging = False):
        unit_num = len(self.units)
        if logging:
            print("\n       Player "+str(self.player_num)+" bought a new " + str(unit_type)+". It spawned at "+str(location))
        if unit_type == 'Scout':
            return Scout(self.player_num, location,self.tech['attack'][0], self.tech['defense'][0],unit_num)
        elif unit_type == 'Destroyer':
            return Destroyer(self.player_num, location,self.tech['attack'][0], self.tech['defense'][0],unit_num)
        elif unit_type == 'Cruiser':
            return Cruiser(self.player_num, location,self.tech['attack'][0], self.tech['defense'][0],unit_num)
        elif unit_type == 'Battlecruiser':
            return Battlecruiser(self.player_num, location,self.tech['attack'][0], self.tech['defense'][0],unit_num)
        elif unit_type == 'Battleship':
            return Battleship(self.player_num, location,self.tech['attack'][0], self.tech['defense'][0],unit_num)
        elif unit_type == 'Dreadnaught':
            return Dreadnaught(self.player_num, location,self.tech['attack'][0], self.tech['defense'][0],unit_num)
        elif unit_type == 'Colony':
            return ColonyShip(self.player_num, location,self.tech['attack'][0],self.tech['defense'][0],unit_num)
        elif unit_type == 'Decoy':
            return Decoy(self.player_num, location,self.tech['attack'][0], self.tech['defense'][0],unit_num)
        elif unit_type == "Base":
            return Base(self.player_num, location,self.tech['attack'][0], self.tech['defense'][0],unit_num)