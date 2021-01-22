from players.player import Player
from board import Board
from movement_engine import MovementEngine
from economic_engine import EconomicEngine
from combat_engine import CombatEngine

class Game:

    def __init__(self, board_size = [5,5],max_turns = 10, logging = True, die_rolls = 'descending'):
        self.players = []
        self.defeated_players = []
        self.current_player = None
        self.board_size = board_size
        self.board = None
        self.turn_count = 0
        self.max_turns = max_turns
        self.phase = 'Bruh Moment'
        self.winner = 'None'
        self.logging = logging
        self.dice_rolls = die_rolls
        self.complete = False

    def add_player(self, strategy, home_coords):
        new_player = Player(strategy, len(self.players), home_coords, self)
        self.players.append(new_player)

    def create_assets(self):
        if self.logging:
            print('Creating Board')
        self.board = Board(self.board_size, self)
        self.economic_engine = EconomicEngine(self.board, self)
        self.movement_engine = MovementEngine(self.board, self)
        self.combat_engine = CombatEngine(self.board, self)

    def initialize_game(self):
        self.create_assets(self.planets)
        if self.logging:
            print('Initializing Players')
        for player in self.players:
            player.cp = 0
            player.initialize_units()
        self.board.update(self.players)
        if self.logging:
            for s in range(len(self.players)):
                print('----------------------------------')
                print('Player', s + 1, ':')
                print('Combat Points:',self.players[s].cp)
                for unit in self.players[s].units:
                    print(unit.name, ':', unit.coords)
                print('----------------------------------')

    def complete_turn(self):
        self.turn_count += 1
        self.movement_engine.complete_movement_phase()
        self.combat_engine.complete_combat_phase()
        self.remove_defeated_players()
        if self.complete:
            return
        self.economic_engine.complete_economic_phase()

    def complete_many_turns(self, num_turns,):
        for _ in range(num_turns):
            self.complete_turn()
            if self.complete:
                return

    def run_to_completion(self):
        while True:
            self.complete_turn()
            if self.complete:
                break

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
            self.players.remove(player)
            if self.logging:
                print('Player', player.player_num, 'Has Died')
        if len(self.players) == 1:
            player = self.players[0]
            self.winner = player.player_num
            self.complete = True
            print('Player', player.player_num,'Won')

    def generate_state(self):
        state = {}
        state['board_size'] = tuple(self.board.size)
        state['turn'] = self.num_turns
        state['phase'] = self.phase
        state['round'] = self.movement_engine.movement_phase
        state['player_whose_turn'] = self.current_player
        state['winner'] = self.winner
        state['unit_data'] = {
        'Battleship': {'cp_cost': 20, 'hullsize': 3},
        'Battlecruiser': {'cp_cost': 15, 'hullsize': 2},
        'Cruiser': {'cp_cost': 12, 'hullsize': 2},
        'Destroyer': {'cp_cost': 9, 'hullsize': 1},
        'Dreadnaught': {'cp_cost': 24, 'hullsize': 3},
        'Scout': {'cp_cost': 6, 'hullsize': 1},
        'Shipyard': {'cp_cost': 3, 'hullsize': 1},
        'Decoy': {'cp_cost': 1, 'hullsize': 0},
        'Colonyship': {'cp_cost': 8, 'hullsize': 1},
        'Base': {'cp_cost': 12, 'hullsize': 3},}
        state['technology_data'] = {
        'shipsize': [10, 15, 20, 25, 30],
        'attack': [20, 30, 40],
        'defense': [20, 30, 40],
        'movement': [20, 30, 40, 40, 40],
        'shipyard': [20, 30]}
        state['players'] = [player.player_state() for player in self.players]
        state['planets'] = [planet.location for coord in self.board.game_data for planet in self.board.game_data[coord] if planet.unit_type == 'Planet']
        return state

    
    

