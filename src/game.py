from players.random_player import RandomPlayer
from players.dumb_player import DumbPlayer
from players.combat_testing_player import CombatTestPlayer
from board import Board
from combat_engine import CombatEngine
from units.colony import Colony

class Game:
    def __init__(self,logging = True):
        self.logging = logging
        self.num_turns = 0
        self.winner = None 
        self.board = Board([5,5])
        self.players = [CombatTestPlayer(1,(2,0), self.board.game_data,self.logging), CombatTestPlayer(2,(2,4), self.board.game_data,self.logging)]
        
    def update_board(self):
        for player in self.players:
            temp = player.game_data
            player.game_data = {}
            for x in range(5):
                for y in range(5):
                    player.game_data[(x,y)] = []
            for elem in temp:
                for unit in temp[elem]:
                    if unit.location is not None:
                        player.game_data[unit.location].append(unit)

            for coord in player.game_data:
                for planet in player.game_data[coord]:
                    if planet.unit_type == 'Planet' and planet.has_a_colony:
                        if planet.colony.location == None:
                            planet.reset()
    
    
    def check_for_and_initiate_combat(self):
        p1_units = []
        p2_units = []
        self.update_board()
        for player in self.players:
            for coord in player.game_data:
                for unit in player.game_data[coord]:
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
                        self.update_board()
                        for player in self.players:
                            for unit in player.game_data[p1_ship.location]:
                                if unit.unit_type != "Planet":
                                    if unit.team == 1 and unit not in p1_ships:
                                        p1_ships.append(unit)
                                    elif unit.team == 2 and unit not in p2_ships:
                                        p2_ships.append(unit)
        #sort all units at location of combat by attack grade
                        ships_in_combat = p1_ships + p2_ships
                        combat = CombatEngine(ships_in_combat,False)
                        combat.resolve_combat(p1_type = self.players[0].player_type,p2_type = self.players[1].player_type)
                        self.update_board()
                    
    def check_for_and_initiate_colony_combat(self):
        planets = [planet  for coord in self.board.game_data for planet in self.board.game_data[coord] if planet.unit_type == "Planet" and planet.has_a_colony]
        for planet in planets:
            units = [unit for unit in self.players[0].game_data[planet.location] if unit.unit_type != 'Planet' and unit.team != planet.player]
            if len(units) > 0:
                combat = CombatEngine(units,False)
                combat.find_enemy_ships_at_colonies(planet.player)
                self.update_board()

    


    def check_for_planet(self, colony_ship):
        for player in self.players:
            for coord in player.game_data:
                for unit in player.game_data[coord]:
                    if unit.unit_type == "Planet":
                        if unit.location == colony_ship.location and not unit.has_a_colony:
                            colony_ship.location = None
                            self.update_board()
                            unit.player = colony_ship.team   
                            unit.has_a_colony = True 
                            attack_tech = self.players[colony_ship.team -1].attack_tech
                            defense_tech = self.players[colony_ship.team -1].defense_tech
                            unit.colony = Colony(colony_ship.team, unit.location,attack_tech,defense_tech,[],False)
                            self.board.game_data[unit.location].append(Colony(colony_ship.team, unit.location,attack_tech,defense_tech,[],False))

                
                        
    def distribute_player_income(self):
        player_income = [0 for player in self.players]
        player_colonies = [0 for player in self.players]
        self.update_board()
        for coord in self.players[0].game_data:
            for unit in self.players[0].game_data[coord]:
                if unit.unit_type == "Colony":
                    self.players[unit.team - 1].money += unit.armor
                    player_income[unit.team - 1] += unit.armor
                    player_colonies[unit.team -1] += 1
        if self.logging:
            print("\n       Player 1 earned "+str(player_income[0])+" CP's from thier "+str(player_colonies[0])+" colonies")
            print("\n       Player 2 earned "+str(player_income[1])+" CP's from thier "+str(player_colonies[1])+" colonies")

    def collect_player_maintenence_costs(self):
        for player in self.players:
            for coord in player.game_data:
                for unit in player.game_data[coord]:
                    if unit.unit_type != "Planet" and unit.unit_type != "Colony" and  unit.unit_type != 'CS' and unit.shorthand != 'Dc' and unit.location is not None and unit.team==player.player_num:
                        maintenence = unit.hull_size
                        
                        if self.players[unit.team - 1].money - maintenence < 0:
                            unit.location = None
                            self.update_board()
                            if self.logging:
                                print("\n       Player "+str(unit.team)+" cannot sustain thier "+str(unit.unit_type)+" due to maintenence.")
                        else:
                            self.players[unit.team - 1].money -= maintenence
                            if self.logging:
                                print("\n       Player "+str(unit.team)+" sustained thier "+str(unit.unit_type)+" for " +str(unit.hull_size))

   
    def spend_player_money(self):
        for player in self.players:
            start_money = player.money
            player.spend()
            if player.money == start_money:
                if self.logging:
                    print("\n       Player "+str(player.player_num)+" didn't buy anything this turn")

    def complete_movement_phase(self):
        self.num_turns += 1
        print("\n TURN " + str(self.num_turns) + "  MOVEMENT PHASE")
        for player in self.players:
            player.move_player_units()
            self.update_board()
        for coord in self.board.game_data:
            for unit in self.board.game_data[coord]:
                if unit.unit_type == "Colony Ship":
                    self.check_for_planet(unit)
        
        print("\n ------------- End of Movement Phase--------------")
    
    def complete_combat_phase(self):
        print("\n TURN " + str(self.num_turns) + "  COMBAT PHASE")
        self.check_for_and_initiate_combat()
        self.check_for_and_initiate_colony_combat()
        print("\n ------------- End of Combat Phase--------------")
        
    


    def complete_economic_phase(self):
        print("\n TURN " + str(self.num_turns) + "  ECONOMIC PHASE")
        if self.logging:
            print("\n   Income From Colonies:")
        self.distribute_player_income()
        self.update_board()
        if self.logging:
            print("\n   Maintenence:")
        self.collect_player_maintenence_costs()
        self.update_board()
        if self.logging:
            print("\n   New ships and Tech upgrades:")
        self.spend_player_money()
        self.update_board()
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
        p1_check = [unit for coord in self.players[0].game_data for unit in self.players[0].game_data[coord] if unit.unit_type != 'Planet' and unit.unit_type != 'Colony' and unit.team == 1]
        p2_check = [unit for coord in self.players[1].game_data for unit in self.players[1].game_data[coord] if unit.unit_type != 'Planet' and unit.unit_type != 'Colony' and unit.team == 2]
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
