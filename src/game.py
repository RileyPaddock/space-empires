import random
from players.random_player import Player
from players.random_player import RandomPlayer
from players.dumb_player import DumbPlayer
from players.combat_testing_player import CombatTestPlayer
from board import Board
from combat_engine import CombatEngine
from units.colony import Colony

class Game:
    def __init__(self, players, logging = True):
        self.logging = logging
        self.num_turns = 0
        self.winner = None 
        self.board = Board([5,5])
        self.combat_turn = 0
        self.players = []
        for i in range(len(players)):
            if players[i] == 'Combat':
                self.players.append(CombatTestPlayer(i+1, ((self.board.size[0] - 1)//2, (self.board.size[1] - 1)* i), self.board,self.logging))
            elif players[i] == 'Dumb':
                self.players.append(DumbPlayer(i+1, ((self.board.size[0] - 1)//2, (self.board.size[1] - 1)* i), self.board,self.logging))
        

    def generate_state(self,phase,player):
        state = {}
        state['turn'] = self.num_turns
        state['player'] = self.players.index(player)
        state['winner'] = self.winner
        state['players'] = [self.player_state(player) for player in self.players]
        state['planets'] = [planet.location for coord in self.board.game_data for planet in self.board.game_data[coord] if planet.unit_type == 'Planet']
        return state

    def player_state(self,player):
        player_state = {}
        player_state['cp'] = player.money
        player_state['technology'] = {attr:value for attr, value in player.__dict__.items() if 'tech' in attr}
        player_state['units'] = [self.unit_state(unit) for coord in player.board.game_data for unit in player.board.game_data[coord] if unit.unit_type != 'Planet' and unit.team == player.player_num]
        return player_state

    def unit_state(self,unit):
        unit_state = {}
        unit_state['location'] = unit.location
        unit_state['type'] = unit.unit_type
        unit_state['technology'] = {attr:value for attr, value in unit.__dict__.items() if 'tech' in attr}
        return unit_state
    
    
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
                        combat = CombatEngine(ships_in_combat,self.combat_turn, self.logging, 'random')
                        combat.resolve_combat(p1_type = self.players[0].player_type,p2_type = self.players[1].player_type)
                        self.board.update_board()
                        self.combat_turn = combat.combat_turn
                    
    def check_for_and_initiate_colony_combat(self):
        planets = [planet  for coord in self.board.game_data for planet in self.board.game_data[coord] if planet.unit_type == "Planet" and planet.has_a_colony]
        for planet in planets:
            units = [unit for unit in self.players[0].board.game_data[planet.location] if unit.unit_type != 'Planet' and unit.team != planet.player]
            if len(units) > 0:
                combat = CombatEngine(units,self.combat_turn, self.logging, 'random')
                combat.find_enemy_ships_at_colonies(planet.player)
                self.board.update_board()
                self.combat_turn = combat.combat_turn

    


    def check_for_planet(self, colony_ship):
        for player in self.players:
            for coord in player.board.game_data:
                for unit in player.board.game_data[coord]:
                    if unit.unit_type == "Planet":
                        if unit.location == colony_ship.location and not unit.has_a_colony:
                            if self.players[colony_ship.team - 1].will_colonize():
                                colony_ship.location = None
                                self.board.update_board()
                                unit.player = colony_ship.team   
                                unit.has_a_colony = True 
                                attack_tech = self.players[colony_ship.team -1].attack_tech
                                defense_tech = self.players[colony_ship.team -1].defense_tech
                                unit.colony = Colony(colony_ship.team, unit.location,attack_tech,defense_tech,[],False)
                                self.board.game_data[unit.location].append(Colony(colony_ship.team, unit.location,attack_tech,defense_tech,[],False))

                
                        
    def distribute_player_income(self):
        player_income = [0 for player in self.players]
        player_colonies = [0 for player in self.players]
        self.board.update_board()
        for coord in self.players[0].board.game_data:
            for unit in self.players[0].board.game_data[coord]:
                if unit.unit_type == "Colony":
                    if unit.location == self.players[unit.team - 1].start_pos:
                         self.players[unit.team - 1].money += 20
                         player_income[unit.team - 1] += 20
                    else:
                        self.players[unit.team - 1].money += unit.armor
                        player_income[unit.team - 1] += unit.armor
                    player_colonies[unit.team -1] += 1
        if self.logging:
            print("\n       Player 1 earned "+str(player_income[0])+" CP's from thier "+str(player_colonies[0])+" colonies")
            print("\n       Player 2 earned "+str(player_income[1])+" CP's from thier "+str(player_colonies[1])+" colonies")

    def collect_player_maintenence_costs(self):
        for player in self.players:
            maintainable_units = []
            for coord in player.board.game_data:
                for unit in player.board.game_data[coord]:
                    if unit.unit_type != "Planet" and unit.unit_type != "Colony" and  unit.unit_type != 'CS' and unit.shorthand != 'Dc' and unit.location is not None and unit.team==player.player_num:
                        maintainable_units.append(unit)
            maintainable_units = self.sort_by_hull_size(maintainable_units)
            for unit in maintainable_units:
                if self.players[unit.team - 1].money - unit.hull_size < 0:
                    unit.location = None
                    self.board.update_board()
                    if self.logging:
                        print("\n       Player "+str(unit.team)+" cannot sustain thier "+str(unit.unit_type)+" due to maintenence.")
                else:
                    self.players[unit.team - 1].money -= unit.hull_size
                    if self.logging:
                        print("\n       Player "+str(unit.team)+" sustained thier "+str(unit.unit_type)+" for " +str(unit.hull_size))

   
    def sort_by_hull_size(self, ships):
        for i in range(len(ships)):  
            for j in range(0, len(ships)-(i+1)):  
                if (ships[j].price < ships[j + 1].price):  
                    temp = ships[j]  
                    ships[j]= ships[j + 1]  
                    ships[j + 1]= temp  
        return ships 

    def spend_player_money(self):
        for player in self.players:
            start_money = player.money
            player.spend()
            if player.money == start_money:
                if self.logging:
                    print("\n       Player "+str(player.player_num)+" didn't buy anything this turn")

    def complete_movement_phase(self):
        self.num_turns += 1
        if self.logging:
            print("\n TURN " + str(self.num_turns) + "  MOVEMENT PHASE")
        for player in self.players:
            player.move_player_units()
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
        self.distribute_player_income()
        self.board.update_board()
        if self.logging:
            print("\n   Maintenence:")
        self.collect_player_maintenence_costs()
        self.board.update_board()
        if self.logging:
            print("\n   New ships and Tech upgrades:")
        self.spend_player_money()
        self.board.update_board()
        if self.logging:
            print("\n ------------- End of Economic Phase--------------")
	# def plot_game_state(self):
    #     game_data = []
       
    #     for planet in self.planets:
    #         color = 'orange'
    #         state = 'Planet'
    #         if planet.has_a_colony:
    #             color = 'green'
    #             if planet.player == 1:
    #                 state = 'Col(1)'
    #             else:
    #                 state = 'Col(2)'

    #         ship_info = {'x': planet.location[0] , 'y': planet.location[1], 'color': color,'label': state}
    #         game_data.append(ship_info)

    #     for player in self.players:
    #       if player.player_num == 1:
    #         team_color = 'blue'
    #       else:
    #         team_color = 'red'
    #       for i in range(len(player.units)):
    #         stagger = 0
    #         if player.units[i].location is not None:
    #           for j in range(len(player.units)):
    #             if player.units[i].location == player.units[j].location and i != j:
    #               if i < j:
    #                 stagger = -0.25
    #               else:
    #                 stagger = 0.25
    #               break
    #             else:
    #               stagger = 0

    #           ship_info = {'x': player.units[i].location[0] + stagger, 'y': player.units[i].location[1], 'color': team_color, 'label': str(player.units[i].shorthand) + str(i+1)}
    #           game_data.append(ship_info)

    #     self.render_game(game_data)

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
