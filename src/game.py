from players.player import Player
from board import Board
from movement_engine import MovementEngine
from economic_engine import EconomicEngine
from combat_engine import CombatEngine

class Game:

    def __init__(self, board_size = [5,5],max_turns = 10, logging = True, die_rolls = 'descending', level = 3):
        self.board_size = board_size
        self.max_turns = max_turns
        self.logging = logging
        self.dice_rolls = die_rolls
        self.level = level
        self.players = []
        self.defeated_players = []
        self.num_turns = 0
        self.num_combats = 0
        self.complete = False
        self.current_player = None
        self.board = None
        self.phase = None
        self.winner = None
    
    def game_state(self, state_type = 'regular'):
        game_state = {}
        game_state['board_size'] = tuple(self.board.size)
        game_state['turn'] = self.num_turns
        game_state['phase'] = self.phase
        game_state['round'] = self.movement_engine.movement_phase
        game_state['player_whose_turn'] = self.current_player
        game_state['winner'] = self.winner
        game_state['players'] = [player.player_state(state_type) for player in self.players]
        if state_type == 'regular':
            game_state['planets'] = [planet.location for coord in self.board.game_data for planet in self.board.game_data[coord] if planet.unit_type == 'Planet']
        game_state['unit_data'] = {
        'Battleship': {'cp_cost': 20, 'shipsize_needed': 3},
        'Battlecruiser': {'cp_cost': 15, 'shipsize_needed': 2},
        'Cruiser': {'cp_cost': 12, 'shipsize_needed': 2},
        'Destroyer': {'cp_cost': 9, 'shipsize_needed': 1},
        'Dreadnaught': {'cp_cost': 24, 'shipsize_needed': 3},
        'Scout': {'cp_cost': 6, 'shipsize_needed': 1},
        'Shipyard': {'cp_cost': 3, 'shipsize_needed': 1},
        'Decoy': {'cp_cost': 1, 'shipsize_needed': 0},
        'Colonyship': {'cp_cost': 8, 'shipsize_needed': 1},
        'Base': {'cp_cost': 12, 'shipsize_needed': 3},}
        game_state['technology_data'] = {
        'shipsize': [0, 10, 15, 20, 25, 30],
        'attack': [20, 30, 40],
        'defense': [20, 30, 40],
        'movement': [0, 20, 30, 40, 40, 40],
        'shipyard': [0, 20, 30]}
        return game_state

    def add_player(self, strategy, home_coords):
        new_player = Player(strategy, len(self.players), home_coords, self)
        self.players.append(new_player)

    def start_engines(self):
        if self.logging:
            print('Creating Board')
        self.board = Board(self.board_size, self, [player.home_coords for player in self.players], self.level)
        self.economic_engine = EconomicEngine(self.board, self)
        self.movement_engine = MovementEngine(self.board, self)
        self.combat_engine = CombatEngine(self)

    def initialize_game(self):
        self.start_engines()
        if self.logging:
            print('Initializing Players')
        for player in self.players:
            if self.level > 1:
                player.cp = 30
            player.initialize_units()
        self.board.update(self.players)
        if self.logging:
            for s in range(len(self.players)):
                print('Player', s + 1, ':')
                print('Combat Points:',self.players[s].cp)
                for unit in self.players[s].units:
                    print(unit.name, ':', unit.coords)

    def complete_turn(self):
        self.num_turns += 1
        self.movement_engine.complete_movement_phase()
        self.combat_engine.complete_combat_phase()
        self.remove_defeated_players()
        if self.complete:
            return

        if self.level == 2:
            if self.num_turns == 1:
                self.economic_engine.complete_economic_phase()
        else:
            self.economic_engine.complete_economic_phase()

    def complete_movement_phase(self): return self.movement_engine.complete_movement_phase()

    def complete_combat_phase(self): return self.combat_engine.complete_combat_phase()

    def complete_economic_phase(self): return self.economic_engine.complete_economic_phase()

    def complete_many_turns(self, num_turns,):
        for _ in range(num_turns):
            self.complete_turn()
            if self.complete:
                print('Player', self.winner,'Won')
                return

    def run_to_completion(self):
        while not self.complete and self.num_turns <= 100:
            self.complete_turn()
            if self.complete and self.logging:
                print(str(self.dice_rolls) + " die rolls:")
                print("- num turns: "+str(self.num_turns))
                print("- num combats: "+str(self.num_combats))
                print("- winner: Player "+str(self.winner))
                for player in self.players+self.defeated_players:
                    print("- Player "+str(player.player_num)+" ending CP: "+ str(player.cp))
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
            self.defeated_players.append(player)
            self.players.remove(player)
            if self.logging:
                print('Player', player.player_num, 'Has Died')
        if len(self.players) == 1:
            player = self.players[0]
            self.winner = player.player_num
            self.complete = True

    

    
    

