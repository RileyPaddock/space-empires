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
        self.technologies = {'attack' : 0, 'defense' : 0, 'movement' : 1, 'shpyrd' : 1, 'ss' : 1}
        self.home_coords = starting_coords
        self.home_planet = None
        self.game = game
        self.units = []
        self.cp = 0
    
    def build_unit(self, unit_name, coords, pay = True):
        colony = self.find_colony(coords)
        if unit_name.unit_type == 'Base':
            if colony.base is not None:
                return False
        if unit_name.unit_type == 'Shipyard':
            if len(colony.shipyards) == 4:
                return False
        ship_tech = {key: val for key,val in self.technologies.items() if key in ['attack', 'defense', 'movement']}
        new_unit = unit_name(coords, len(self.units) + 1, self, ship_tech, self.game, self.game.turn_count)
        if pay:
            self.cp -= new_unit.cost
        self.units.append(new_unit)

    def find_colony(self, coords):
        for unit in self.units:
            if unit.unit_type == 'Colony':
                if unit.location == coords:
                    return unit

    def build_colony(self, coords, col_type = 'Normal', colony_ship = None):
        ship_tech = {key: val for key,val in self.technologies.items() if key in ['attack', 'defense']}
        if col_type == 'Home':
            home_colony = Colony(coords, len(self.units) + 1, self, ship_tech, self.game, self.game.turn_count,colony_type = 'Home')
            self.units.append(home_colony)
        else:
            new_colony = Colony(coords, len(self.units) + 1, self, ship_tech, self.game, self.game.turn_count, colony_type = 'Normal')
            self.game.board.grid[tuple(coords)].planet.colonize(self, new_colony)
            self.units.append(new_colony)
            if colony_ship is not None:
                colony_ship.destroy()

    def initialize_units(self):
        self.build_colony(self.home_coords, col_type = 'Home')
        home_planet = Planet(self.home_coords, colonized = True, colony = self.units[0])
        self.home_planet = home_planet
        self.game.board.planets.append(home_planet)
        self.game.board.grid[tuple(self.home_coords)].planet = home_planet
        for i in range(4):
            self.build_unit(ShipYard, self.home_coords, pay = False)
        self.units[0].set_builders()
        for i in range(3):
            self.build_unit(Scout, self.home_coords, pay = False)
        for i in range(3):
            self.build_unit(ColonyShip, self.home_coords, pay = False)

    def check_colony(self, build_size, ship, coords):
        for unit in self.units:
            if unit.unit_type == 'Colony' and unit.location == coords:
                if self.technologies['ss'] >= ship.ship_size_needed:
                    if unit.builders >= build_size:
                        unit.builders -= build_size
                        return unit.location
                    else:
                        if self.game.logging:
                            print('Player does not have enough builders at colonies to build ship')
                        return None
                else:
                    if self.game.logging:
                        print('Player does not have proper ship size level')
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

    def get_maintenance(self):
        total_maintenance = 0
        for unit in self.units:
            if unit.maintenance is not None:
                total_maintenance += unit.maintenance
        return total_maintenance

    def get_income(self):
        income = 0
        for unit in self.units:
            if unit.unit_type == 'Colony':
                income += unit.capacity
        return income
    
    def player_state(self):
        player_state = {}
        player_state['player_num'] = self.player_num
        player_state['cp'] = self.cp
        techs = ['shipsize', 'attack', 'defense', 'movement', 'shipyard']
        player_state['technology'] = {techs[techs.index(tech)] : self.technologies[tech] for tech in self.technologies.keys()}
        player_state['home_coords'] = self.start_pos
        player_state['units'] = [self.unit_state(unit) for unit in self.units if unit.alive]
        return player_state

    def unit_state(self,unit):
        unit_state = {}
        unit_state['player'] = self.player_num
        unit_state['coords'] = unit.location
        unit_state['type'] = unit.unit_type
        unit_state['technology'] = {attr:value for attr, value in unit.__dict__.items() if 'tech' in attr}
        unit_state['speed'] = unit.speed
        unit_state['hits_left'] = unit.armor
        unit_state['defense'] = unit.defense
        unit_state['speed'] = unit.strength
        unit_state['unit_num'] = unit.unit_num
        unit_state['team']  =unit.team
        unit_state['turn_created'] = unit.turn_created
        unit_state['class_num'] = unit.attack_grade
        unit_state['maintenance'] = unit.maintenance
        unit_state['alive'] = unit.alive
        techs = ['attack', 'defense', 'movement']
        unit_state['technology'] = {techs[techs.index(tech)] : unit.technologies[tech] for tech in unit.technologies.keys()}
        return unit_state
        
    