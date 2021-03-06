from units.scout import Scout
from units.cruiser import Cruiser
from units.colony_ship import ColonyShip
from units.colony import Colony
from units.base import Base
from planet import Planet
from units.ship_yard import ShipYard


class Player:

    def __init__(self, strategy, player_num, starting_coords, game):
        self.strategy = strategy
        self.player_num = player_num
        self.home_coords = starting_coords
        self.game = game
        self.level = self.game.level
        self.home_planet = None
        self.last_purchase = None
        self.unit_counter = {unit_type:1 for unit_type in self.game.unit_data}
        self.unit_counter['Colony'] = 0
        self.units = []
        self.cp = 0
        self.technologies = {'attack' : 0, 'defense' : 0, 'movement' : 1, 'shipyard' : 1, 'shipsize' : 1}

    def player_state(self, state_type):
        player_state = {}
        player_state['player_num'] = self.player_num
        if state_type == 'regular':
            player_state['cp'] = self.cp
        player_state['last_purshase'] = self.last_purchase
        techs = ['shipsize', 'attack', 'defense', 'movement', 'shipyard']
        player_state['technology'] = {techs[techs.index(tech)] : self.technologies[tech] for tech in self.technologies.keys()}
        player_state['home_coords'] = self.home_coords
        player_state['units'] = [self.unit_state(unit, state_type) for unit in self.units if unit.alive]
        return player_state

    def unit_state(self,unit, state_type):
        unit_state = {}
        unit_state['player'] = self.player_num
        unit_state['coords'] = unit.location
        unit_state['num'] = unit.unit_num
        if unit.unit_type == 'Shipyard':
            unit_state['build_capacity'] = unit.build_capacity
        if state_type != 'hidden':
            unit_state['type'] = unit.unit_type
            unit_state['hits_left'] = unit.armor
            unit_state['turn_created'] = unit.turn_created
            unit_state['maintenance'] = unit.maintenance
            unit_state['alive'] = unit.alive
            techs = ['attack', 'defense', 'movement']
            unit_state['technology'] = {techs[techs.index(tech)] : unit.technologies[tech] for tech in unit.technologies.keys()}
            if unit.can_atk:
                unit_state['class_num'] = unit.attack_grade
            return unit_state

    def create_unit(self, unit_name, coords, pay = True):
        name = unit_name.unit_type
        colony = self.find_colony(coords)
        if name == 'Base':
            if colony.base is not None:
                return False
        ship_tech = {key: self.technologies[key] for key in self.technologies if key in ['attack', 'defense', 'movement']}
        new_unit = unit_name(coords, name+" "+str(self.unit_counter[name]), self, ship_tech, self.game, self.game.num_turns)
        self.unit_counter[name] += 1
        if pay:
            self.cp -= new_unit.cost
            self.last_purchase = unit_name
        self.units.append(new_unit)

    def find_colony(self, coords):
        for unit in self.units:
            if unit.unit_type == 'Colony':
                if unit.location == coords:
                    return unit

    def build_colony(self, coords, col_type = 'Normal', colony_ship = None):
        ship_tech = {key: val for key,val in self.technologies.items() if key in ['attack', 'defense']}
        if col_type == 'Home':
            
            home_colony = Colony(coords, "Homeworld", self, ship_tech, self.game, self.game.num_turns,colony_type = 'Home')
            for planet in self.game.board.planets:
                if tuple(planet.location) == tuple(self.home_coords):
                    self.home_planet = planet
                    planet.colonize(home_colony)
            self.units.append(home_colony)
        else:
            new_colony = Colony(coords, "Colony "+str(self.unit_counter["Colony"]), self, ship_tech, self.game, self.game.turn_count, colony_type = 'Normal')
            new_colony.turn_colonized = self.game.num_turns
            for planet in self.game.board.planets:
                if planet.location == new_colony.location:
                    planet.colonize(new_colony)
            self.units.append(new_colony)
            if colony_ship is not None:
                colony_ship.destroy()

    def initialize_units(self):
        self.build_colony(self.home_coords, col_type = 'Home')
        for i in range(3):
            self.create_unit(Scout, self.home_coords, pay = False)
        for i in range(4):
                self.create_unit(ShipYard, self.home_coords, pay = False)
        self.units[0].set_builders()

        

        if self.level > 1:
            for i in range(4):
                self.create_unit(ShipYard, self.home_coords, pay = False)
            self.units[0].set_builders()


        

        self.last_purchase = 'Scout'

        if self.level > 3:
            for i in range(3):
                self.create_unit(ColonyShip, self.home_coords, pay = False)
        

    def check_colony(self, build_size, ship, coords):
        for unit in self.units:
            if unit.unit_type == 'Colony' and unit.location == coords:
                if self.technologies['shipsize'] >= ship.ship_size:
                    if unit.builders >= build_size:
                        unit.builders -= build_size
                        return unit.location
                    else:
                        return None
                else:
                    return None


    def update_shipyards(self):
        ship_size_capacity = {'1' : 1.0, '2':1.5, '3' : 2.0}
        for unit in self.units:
            if unit.unit_type == 'Shipyard':
                unit.build_capacity = ship_size_capacity[str(self.technologies['shipyard'])]
        self.set_colony_builders()

    def set_colony_builders(self):
        for unit in self.units:
            if unit.unit_type == 'Colony':
                unit.set_builders()

    def calc_maintenance(self):
        total_maintenance = 0
        for unit in self.units:
            if unit.maintenance is not None:
                total_maintenance += unit.maintenance
        return total_maintenance

    def calc_income(self):
        income = 0
        for unit in self.units:
            if unit.unit_type == 'Colony':
                income += unit.capacity
        return income
        
    
