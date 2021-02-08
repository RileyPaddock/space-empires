from units.unit import Unit
from units.scout import Scout
from units.colony_ship import ColonyShip
from units.destroyer import Destroyer
from units.battleship import Battleship
from units.cruiser import Cruiser
from units.dreadnaught import Dreadnaught
from units.ship_yard import ShipYard

class EconomicEngine:

    def __init__(self, board, game):
        self.board = board
        self.game = game
        self.current_player = None
        self.used_colonies = []#colonies that have already built shipyards this turn


    def complete_economic_phase(self):
        self.used_colonies = []
        self.game.phase = 'Economic'
        if self.game.logging:
            print('BEGINNING OF ECONOMIC PHASE')
        for player in self.game.players:
            self.current_player = player
            income = player.calc_income()
            player.cp += income
            if self.game.logging:
                print('--------------')
                print('Added', income, 'Combat Points from Colonies to Player', player.player_num)
                print('New Total:', player.cp)
                print('--------------')
            maintenance = player.calc_maintenance()
            if player.cp < maintenance:
                excess_cp = maintenance - player.cp
                while excess_cp > 0:
                    removal = self.remove_ship(player)
                    excess_cp -= removal
                maintenance = player.calc_maintenance()
            player.cp -= maintenance
            if self.game.logging:
                print('Player',player.player_num,'payed',maintenance,'in maintenance!')
            self.make_purchases(player)
            player.set_colony_builders()
            if self.game.logging:
                print('PLAYER', player.player_num,'HAS', player.cp,'LEFT')
            self.board.update(self.game.players)
        self.board.update(self.game.players)
        if self.game.logging:
            print('----------------------------')
            print('END OF ECONOMIC PHASE')


    def make_purchases(self, player):
        purchases = player.strategy.decide_purchases(self.game.game_state())
        ship_objects = [Scout, Destroyer, Dreadnaught, ColonyShip, Cruiser, Battleship, ShipYard]
        ship_names = ['Scout', 'Destroyer', 'Dreadnaught', 'Colonyship', 'Cruiser', 'Battleship', 'Shipyard']
        for technology in purchases['technology']:
            techs = ['shipsize', 'attack', 'defense', 'movement', 'shipyard']
            wanted_upgrade = techs[techs.index(technology)]
            self.buy_tech(wanted_upgrade, player)
        for unit in purchases['units']:
            ship = ship_objects[ship_names.index(unit['type'])]
            if ship.cost <= player.cp:
                if ship.shorthand == 'SY':
                    for player_unit in player.units:
                        if player_unit.unit_type == 'Colony' and player_unit.location == unit['coords']:
                            if player_unit.turn_colonized != self.game.num_turns & player_unit not in self.used_colonies:
                                self.used_colonies.append(player_unit)
                                coords = player_unit.location
                else:
                    coords = player.check_colony(ship.hull_size, ship,unit['coords'])
                if coords is not None:
                    builder = player.create_unit(ship, coords, pay = True)
                    if self.game.logging and builder is not False:
                        print('PLAYER', player.player_num,'BOUGHT A:', ship.name)
            else:
                if self.game.logging:
                    print('Could not afford to buy', ship.name)




    def buy_tech(self, tech_type, player):
        tech_data = {'attack': {'levels' : [-1,0,1,2], 'costs' : [20, 50 , 90], 'max_level' : 4},
            'defense': {'levels' : [-1,0,1,2], 'costs' : [20, 50 , 90], 'max_level' : 4},
            'movement': {'levels': [0,1,2,3,4,5], 'costs': [20, 50, 90, 130, 170], 'max_level' : 6}, 
            'shipyard': {'levels' : [0, 1, 2], 'costs' : [20, 50], 'max_level' : 3}, 
            'shipsize' : {'levels': [0,1,2,3,4,5], 'costs' : [10,15,20,25,30], 'max_level' : 6}}

        if player.technologies[tech_type] < tech_data[tech_type]['max_level']:
            current_lvl = tech_data[tech_type]['levels'].index(player.technologies[tech_type] - 1)
            cost = tech_data[tech_type]['costs'][current_lvl]
            if player.cp >= cost:
                player.cp -= cost
                new_lvl = tech_data[tech_type]['levels'][current_lvl + 1] + 1
                player.technologies[tech_type] = new_lvl
                if tech_type == 'shipyard':
                    player.update_shipyards()
                if self.game.logging:
                    print('---------')
                    print('Player', player.player_num,'Payed For:')
                    print('Level:', player.technologies[tech_type],' Of', tech_type,'Technology')
                    print('---------')
            else:
                if self.game.logging:
                    print('---------')
                    print('Player', player.player_num,'could not afford:')
                    print('Level:', player.technologies[tech_type] + 1,' Of', tech_type,'Technology')
                    print('---------')
        else:
            if self.game.logging:
                print(tech_type,'TECHNOLOGY MAXED OUT')


    def remove_ship(self, player):
        removal = player.strategy.decide_removal(self.game.game_state())
        unit = player.units[removal]
        cp = unit.maintenance
        if self.game.logging:
            print('-------')
            print('Unit:',unit.name, unit.unit_num,'could not be sustained, was destroyed!')
            print('-------')
        unit.destroy()
        return cp

    def economic_state(self):
        return [{
            'player' : player.player_num,
            'maintenance_cost': player.get_maintenance(),
            'income':player.get_income()
        } for player in self.game.players]