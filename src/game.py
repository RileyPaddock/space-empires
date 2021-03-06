import logging 

logging.basicConfig(filename="notes/level3_logs.log", 
                    format='%(message)s', 
                    filemode='w') 
from players.player import Player
from units.scout import Scout
from units.ship_yard import Shipyard
from units.colony import Colony
from board import Board
from movement_engine import MovementEngine
from economic_engine import EconomicEngine
from combat_engine import CombatEngine

class Game:

    def __init__(self, board_size = [7,7],max_turns = 4, logs = True, die_rolls = 'random', level = 3):
        self.board_size = board_size
        self.max_turns = max_turns
        self.logging = logs
        self.dice_rolls = die_rolls
        self.level = level
        self.mode = 'debug'
        self.logger= logging.getLogger() 
        self.logger.setLevel(logging.DEBUG) 
        self.players = []
        self.num_players = 0
        self.defeated_players = []
        self.num_turns = 0
        self.num_combats = 0
        self.complete = False
        self.current_player = None
        self.board = None
        self.phase = None
        self.winner = None
        self.unit_data = {
            'Battleship': {'cp_cost': 20, 'hullsize': 3, 'shipsize_needed': 5, 'tactics': 5, 'attack': 5, 'defense': 2, 'maintenance': 3},

            'Battlecruiser': {'cp_cost': 15, 'hullsize': 2, 'shipsize_needed': 4, 'tactics': 4, 'attack': 5, 'defense': 1, 'maintenance': 2},

            'Cruiser': {'cp_cost': 12, 'hullsize': 2, 'shipsize_needed': 3, 'tactics': 3, 'attack': 4, 'defense': 1, 'maintenance': 2},

            'Destroyer': {'cp_cost': 9, 'hullsize': 1, 'shipsize_needed': 2, 'tactics': 2, 'attack': 4, 'defense': 0, 'maintenance': 1},

            'Dreadnaught': {'cp_cost': 24, 'hullsize': 3, 'shipsize_needed': 6, 'tactics': 5, 'attack': 6, 'defense': 3, 'maintenance': 3},
            
            'Scout': {'cp_cost': 6, 'hullsize': 1, 'shipsize_needed': 1, 'tactics': 1, 'attack': 3, 'defense': 0, 'maintenance': 1},

            'Shipyard': {'cp_cost': 3, 'hullsize': 1, 'shipsize_needed': 1, 'tactics': 3, 'attack': 3, 'defense': 0, 'maintenance': 0},

            'Decoy': {'cp_cost': 1, 'hullsize': 0, 'shipsize_needed': 1, 'tactics': 0, 'attack': 0, 'defense': 0, 'maintenance': 0},

            'Colonyship': {'cp_cost': 8, 'hullsize': 1, 'shipsize_needed': 1, 'tactics': 0, 'attack': 0, 'defense': 0, 'maintenance': 0},
            
            'Base': {'cp_cost': 12, 'hullsize': 3, 'shipsize_needed': 2, 'tactics': 5, 'attack': 7, 'defense': 2, 'maintenance': 0},
            }
    
    def game_state(self, state_type = 'regular'):
        game_state = {}
        game_state['board_size'] = tuple(self.board_size)
        game_state['turn'] = self.num_turns
        game_state['phase'] = self.phase
        game_state['round'] = self.movement_engine.movement_phase
        game_state['player_whose_turn'] = self.current_player
        game_state['winner'] = self.winner
        game_state['players'] = {player.player_num +1:player.player_state(state_type) for player in self.players}
        if state_type == 'regular':
            game_state['planets'] = [planet.location for coord in self.board.game_data for planet in self.board.game_data[coord] if planet.unit_type == 'Planet']
        game_state['unit_data'] = self.unit_data
        game_state['technology_data'] = {
        'shipsize': [0, 10, 15, 20, 25, 30],
        'attack': [20, 30, 40],
        'defense': [20, 30, 40],
        'movement': [0, 20, 30, 40, 40, 40],
        'shipyard': [0, 20, 30]}
        return game_state

    def set_game_state(self,game_state,strategy):
        self.board_size = game_state['board_size']
        self.num_turns = game_state['turn']
        self.phase = game_state["phase"]
        self.round = game_state["round"]
        self.current_player = game_state["current_player"]
        for player in game_state['players']:
            self.add_player(strategy, game_state['players'][player]['homeworld']['coords'])
        for player in self.players:
            player.cp = game_state['players'][player.player_num+1]['cp']
            player.technology = game_state['players'][player.player_num+1]['technology']
            player.units = []
            home = self.unit_from_state(game_state['players'][player.player_num +1]['homeworld'])
            player.home_planet = home
            player.units.append(home)
            for unit in game_state['players'][player.player_num+1]['units']:
                player.units.append(self.unit_from_state(unit,player))
            

    def unit_from_state(self,unit_state,player):
        units = {'Scout':Scout, 'Shipyard':Shipyard,'Colony':Colony}
        unit = units[unit_state['type']](unit_state['coords'],unit_state['num'],player,unit_state['technology'],self,unit_state['turn_created'])
        return unit
        

    def add_player(self, strategy, home_coords):
        new_player = Player(strategy, len(self.players), home_coords, self)
        self.players.append(new_player)
        self.num_players += 1

    def start_engines(self):
        self.board = Board(self.board_size, self, [player.home_coords for player in self.players], self.level)
        self.economic_engine = EconomicEngine(self.board, self)
        self.movement_engine = MovementEngine(self.board, self)
        self.combat_engine = CombatEngine(self)

    def initialize_game(self):
        self.start_engines()
        for player in self.players:
            if self.level == 2:
                player.cp = 10
            else:
                player.cp = 0;
            player.initialize_units()
        self.board.update(self.players)

    def complete_turn(self):
        self.num_turns += 1
        if self.level ==2 and self.num_turns == 1:
            self.economic_engine.complete_economic_phase()
            
        self.movement_engine.complete_movement_phase()
        self.combat_engine.complete_combat_phase()
        self.remove_defeated_players()

        if self.complete:
            return
        if self.level > 2:
            self.economic_engine.complete_economic_phase()

    def complete_movement_phase(self): return self.movement_engine.complete_movement_phase()

    def complete_combat_phase(self): return self.combat_engine.complete_combat_phase()

    def complete_economic_phase(self): return self.economic_engine.complete_economic_phase()

    def complete_many_turns(self, num_turns,):
        for _ in range(num_turns):
            self.complete_turn()
            if self.complete:
                return

    def run_to_completion(self):
        while not self.complete and self.num_turns <= self.max_turns:
            self.complete_turn()
            if self.complete:
                break
        return self.winner

    def remove_defeated_players(self):
        defeated_players = []
        for player in self.players:
            colonized = player.home_planet.colonized
            colony = player.home_planet.colony
            if colonized is False and colony is None:
                defeated_players.append(player)
                for unit in player.units:
                    unit.destroy()
        for player in defeated_players:
            self.defeated_players.append(player)
            self.players.remove(player)
        if len(self.players) == 1:
            player = self.players[0]
            self.winner = player.player_num
            self.complete = True

    

    
    

