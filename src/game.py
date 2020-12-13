import random
from players.random_player import Player
from players.random_player import RandomPlayer
from players.combat_testing_player import CombatTestPlayer
from strategies.dumb_strategy import DumbStrategy
from movement_engine import MovementEngine
from combat_engine import CombatEngine
from economic_engine import EconomicEngine
from board import Board
from units.colony import Colony

class Game:
    def __init__(self, players, board,logging = True,rolls = None):
        self.logging = logging
        self.board = board
        self.players = players
        self.num_turns = 0
        self.winner = None 
        if rolls == None:
            self.rolls = lambda x : random.randrange(1,6)
        else:
            self.rolls = lambda x : rolls[x]
        self.build_players()
        self.movement_engine = MovementEngine()
        self.economic_engine = EconomicEngine(self.players, self.board, self.logging)
        

    def build_players(self):
        for player in self.players:
            player.logging = self.logging
            player.player_num = self.players.index(player)+1
            player.generate_fleet()

    def generate_state(self):
        state = {}
        state['board_size'] = self.board.size
        state['turn'] = self.num_turns
        state['winner'] = self.winner
        state['players'] = [player.player_state() for player in self.players]
        state['planets'] = [planet.location for coord in self.board.game_data for planet in self.board.game_data[coord] if planet.unit_type == 'Planet']
        return state

    
    
    def check_for_and_initiate_combat(self):
        p1_units = []
        p2_units = []
        self.board.update_board()
        for player in self.players:
            for coord in player.board.game_data:
                for unit in player.board.game_data[coord]:
                    if unit.unit_type != "Planet" and unit.unit_type != "Colony":
                        if unit.team == 1 and unit not in p1_units:
                            p1_units.append(unit)
                        elif unit.team == 2 and unit not in p2_units:
                            p2_units.append(unit)
        for p1_ship in p1_units:
            for p2_ship in p2_units:
                if p1_ship.location == p2_ship.location and p1_ship.location is not None:
                        p1_ships = []
                        p2_ships = []
                        #Get all the ships at the location of combat
                        self.board.update_board()
                        for player in self.players:
                            for unit in player.board.game_data[p1_ship.location]:
                                if unit.unit_type != "Planet":
                                    if unit.team == 1 and unit not in p1_ships:
                                        p1_ships.append(unit)
                                    elif unit.team == 2 and unit not in p2_ships:
                                        p2_ships.append(unit)
        #sort all units at location of combat by attack grade
                        ships_in_combat = p1_ships + p2_ships
                        combat = CombatEngine(self.players, ships_in_combat, self.logging, self.rolls)
                        combat.resolve_combat()
                        self.board.update_board()
                        self.combat_turn = combat.combat_turn
                    
    def check_for_and_initiate_colony_combat(self):
        planets = [planet  for coord in self.board.game_data for planet in self.board.game_data[coord] if planet.unit_type == "Planet" and planet.has_a_colony]
        for planet in planets:
            units = [unit for unit in self.players[0].board.game_data[planet.location] if unit.unit_type != 'Planet' and unit.team != planet.player]
            if len(units) > 0:
                combat = CombatEngine(self.players, units, self.logging, self.rolls)
                combat.find_enemy_ships_at_colonies(planet.player)
                self.board.update_board()
                self.combat_turn = combat.combat_turn

    


    def check_for_planet(self, colony_ship):
        for player in self.players:
            for coord in player.board.game_data:
                for unit in player.board.game_data[coord]:
                    if unit.unit_type == "Planet":
                        if unit.location == colony_ship.location and not unit.has_a_colony:
                            if self.players[colony_ship.team - 1].strategy.will_colonize(colony_ship.unit_state(),colony_ship.team):
                                colony_ship.location = None
                                self.board.update_board()
                                unit.player = colony_ship.team   
                                unit.has_a_colony = True 
                                attack_tech = self.players[colony_ship.team -1].attack_tech
                                defense_tech = self.players[colony_ship.team -1].defense_tech
                                unit.colony = Colony(colony_ship.team, unit.location,attack_tech,defense_tech,[],False)
                                self.board.game_data[unit.location].append(Colony(colony_ship.team, unit.location,attack_tech,defense_tech,[],False))

                
        

    def complete_movement_phase(self):
        self.num_turns += 1
        if self.logging:
            print("\n TURN " + str(self.num_turns) + "  MOVEMENT PHASE")
        for player in self.players:
            player.move_player_units(self.generate_state())
            self.board.update_board()
        for coord in self.board.game_data:
            for unit in self.board.game_data[coord]:
                if unit.unit_type == "Colony Ship":
                    self.check_for_planet(unit)
        if self.logging:
            print("\n ------------- End of Movement Phase--------------")
    
    def complete_combat_phase(self):
        if self.logging:
            print("\n TURN " + str(self.num_turns) + "  COMBAT PHASE")
        self.check_for_and_initiate_combat()
        self.check_for_and_initiate_colony_combat()
        if self.logging:
            print("\n ------------- End of Combat Phase--------------")
        
    


    def complete_economic_phase(self):
        if self.logging:
            print("\n TURN " + str(self.num_turns) + "  ECONOMIC PHASE")
        if self.logging:
            print("\n   Income From Colonies:")
        self.economic_engine.distribute_income(self.economic_engine.calc_income())
        self.board.update_board()
        if self.logging:
            print("\n   Maintenence:")
        self.economic_engine.maintenence(self.generate_state())
        self.board.update_board()
        if self.logging:
            print("\n   New ships and Tech upgrades:")
        self.economic_engine.spend(self.generate_state())
        self.board.update_board()
        if self.logging:
            print("\n ------------- End of Economic Phase--------------")

    def check_for_game_over(self):
        p1_check = [unit for coord in self.players[0].board.game_data for unit in self.players[0].board.game_data[coord] if unit.unit_type != 'Planet' and unit.unit_type != 'Colony' and unit.team == 1]
        p2_check = [unit for coord in self.players[1].board.game_data for unit in self.players[1].board.game_data[coord] if unit.unit_type != 'Planet' and unit.unit_type != 'Colony' and unit.team == 2]
        if self.num_turns >= 100:
            if len(p1_check) > len(p2_check):
                self.winner = "Player 1"
            elif len(p1_check) < len(p2_check):
                self.winner = "Player 2"
            else:
                self.winner = "Tie"
            return False
        elif len(p1_check) == 0:
            self.winner = "Player 2"
            return False
        elif len(p2_check) == 0:
            self.winner = "Player 1"
            return False
        else:
            return True

    def run_to_completion(self):
        while self.check_for_game_over():
            self.complete_movement_phase()
            self.complete_combat_phase()
            self.complete_economic_phase()
        print("\n Game Over: "+self.winner+" wins!")
