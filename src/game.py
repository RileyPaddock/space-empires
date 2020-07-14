from player import Player
from board import Board
import random
from Units.colony import Colony

class Game:
    def __init__(self):
        self.num_turns = 0
        self.winner = None 
        self.board = Board([7,7])
        self.players = [Player(1,(3,1), self.board.game_data), Player(2,(3,5), self.board.game_data)]
        
    def correct_board(self):
        temp = self.board.game_data
        self.board.game_data = {}
        for x in range(self.board.size[0]):
            for y in range(self.board.size[1]):
                self.board.game_data[(x,y)] = []
        for elem in temp:
            for unit in temp[elem]:
                if unit.location is not None:
                    self.board.game_data[unit.location].append(unit)
    
    

    def locate_combat(self,p1_ship,p2_ship):
        p1_ships = []
        p2_ships = []
        for unit in self.board.game_data[p1_ship.location]:
            if unit.unit_type != "Planet":
                if unit.team == 1:
                    p1_ships.append(unit)
                elif unit.team == 2:
                    p2_ships.append(unit)
        order_of_combat = self.sort_by_attack_grade(p1_ships + p2_ships)
        while len([p1_ship.location for p1_ship in p1_ships if p1_ship.location is not None]) > 0 and len([p2_ship.location for p2_ship in p2_ships if p2_ship.location is not None]) > 0:
            for ship in order_of_combat:
                if ship.unit_type == 'Colony Ship':
                    ship.location = None
                    self.correct_board()
                else:
                    if ship.location is not None:
                        if ship.team == 1:
                            rand = random.choice(p2_ships)
                            print("\n Combat at "+str(ship.location)+" between Player 1's "+str(ship.unit_type)+" and Player 2's "+str(rand.unit_type)+".")
                            self.attack(ship, rand)
                        elif ship.team == 2:
                            rand = random.choice(p1_ships)
                            print("\n Combat at "+str(ship.location)+" between Player 1's "+str(rand.unit_type)+" and Player 2's "+str(ship.unit_type)+".")
                            self.attack(ship, rand)

    def colony_combat(self):
        planets = [planet  for coord in self.board.game_data for planet in self.board.game_data[coord] if planet.unit_type == "Planet"]
        p1_colonies = [colony for coord in self.board.game_data for colony in self.board.game_data[coord] if colony.unit_type == "Colony" and colony.team == 1]
        p2_colonies = [colony for coord in self.board.game_data for colony in self.board.game_data[coord] if colony.unit_type == "Colony" and colony.team == 2]
        colonies = [p1_colonies, p2_colonies]
        for planet in planets:
            if planet.has_a_colony:
                for ship in self.board.game_data[planet.location]:
                    if ship.unit_type != "Planet" and ship.team != planet.player:
                        colony_in_combat = planet.colony
                        if ship.shorthand == 'Dc':
                            ship.location = None
                            self.correct_board()
                            pass
                        else:
                            for player_colonies in colonies:
                                for colony in player_colonies:
                                    if colony.location == planet.location:
                                        colony_in_combat = colony
                            if colony_in_combat.base != False:
                                if ord(ship.attack_grade) < ord(colony_in_combat.base.attack_grade):
                                    self.attack(ship, colony_in_combat.base)
                                elif ord(ship.attack_grade) > ord(colony_in_combat.base.attack_grade):
                                    self.attack(colony_in_combat.base, ship)
                            else:
                                if colony.armor == 1:
                                    for colony in self.board.game_data[planet.location]:
                                        if colony.unit_type == "Colony":
                                            colony.shipyards = []
                                    planet.reset()
                                else:
                                    self.attack(ship,colony_in_combat)


    def sort_by_attack_grade(self,set_of_units):
        for i in range(len(set_of_units)):  
            for j in range(0, len(set_of_units)-(i+1)):  
                if (ord(set_of_units[j].attack_grade) > ord(set_of_units[j + 1].attack_grade)):  
                    temp = set_of_units[j]  
                    set_of_units[j]= set_of_units[j + 1]  
                    set_of_units[j + 1]= temp  
        return set_of_units 

    def attack(self, p1_ship, p2_ship):
        if p1_ship.shorthand == 'Dc' and p2_ship.shorthand == 'Dc':
            p1_ship.location = None
            p2_ship.location = None
            self.correct_board()
            print("\n   Player 1's Decoy and Player 2's Decoy destroyed each other")
        elif p1_ship.shorthand == 'Dc':
            p1_ship.location = None
            self.correct_board()
            print("\n   Player " + str(p2_ship.team) + "'s "+str(p2_ship.unit_type)+" destroyed Player " + str(p1_ship.team) + "'s " +str(p1_ship.unit_type))
        elif p2_ship.shorthand == 'Dc':
            p2_ship.location = None
            self.correct_board()
            print("\n   Player " + str(p1_ship.team) + "'s "+str(p1_ship.unit_type)+" destroyed Player " + str(p2_ship.team) + "'s " +str(p2_ship.unit_type))
        else:
            rand = random.randint(1,6)
            hit_threshold = ((p1_ship.strength + self.players[0].attack_tech) - (p2_ship.defense  + self.players[1].defense_tech)) - rand

            if rand == 1 or hit_threshold >= 0:
                if p2_ship.armor == 1:
                    p2_ship.location = None
                    self.correct_board()
                    print("\n   Player " + str(p1_ship.team) + "'s "+str(p1_ship.unit_type)+" destroyed Player " + str(p2_ship.team) + "'s " +str(p2_ship.unit_type))
                else:
                    p2_ship.armor -= 1
                    print("\n   Player " + str(p1_ship.team) + "'s "+str(p1_ship.unit_type)+" hit Player " + str(p2_ship.team) + "'s "+ str(p2_ship.unit_type) + " but it still has " + str(p2_ship.armor) + " armor remaining!")

            else:
                print("\n   Player "+str(p1_ship.team)+"'s "+ str(p1_ship.unit_type)+" missed Player "+str(p2_ship.team)+"'s " + str(p2_ship.unit_type))


    def check_for_planet(self, colony_ship):
        for coord in self.board.game_data:
            for unit in self.board.game_data[coord]:
                if unit.unit_type == "Planet":
                    if unit.location == colony_ship.location and not unit.has_a_colony:
                        colony_ship.location = None
                        unit.player = colony_ship.team   
                        unit.has_a_colony = True 
                        unit.colony = Colony(colony_ship.team, unit.location,[],False)
                        self.board.game_data[unit.location].append(Colony(colony_ship.team, unit.location,[],False))

                
                        
    def money_from_colonies(self):
        player_1_income = 0
        player_2_income = 0
        for coord in self.board.game_data:
            for planet in self.board.game_data[coord]:
                if planet.unit_type == "Planet":
                    if planet.has_a_colony:
                        if planet.player == 1:
                            self.players[0].money += planet.colony.armor
                            player_1_income += planet.colony.armor
                        elif planet.player == 2:
                            self.players[1].money += planet.colony.armor
                            player_2_income += planet.colony.armor 
        print("\n       Player 1 earned "+str(player_1_income)+" CP's from thier "+str(len([colony for coord in self.board.game_data for colony in self.board.game_data[coord] if colony.unit_type == "Colony" and colony.location is not None]))+" colonies")
        print("\n       Player 2 earned "+str(player_2_income)+" CP's from thier "+str(len([colony for coord in self.board.game_data for colony in self.board.game_data[coord] if colony.unit_type == "Colony" and colony.location is not None]))+" colonies")

    def maintenence(self):
        for coord in self.board.game_data:
            for unit in self.board.game_data[coord]:
                if unit.unit_type != "Planet" and unit.unit_type != "Colony" and  unit.unit_type != 'CS' and unit.shorthand != 'Dc' and unit.location is not None:
                    maintenence = unit.hull_size
                    if self.players[unit.team - 1].money - maintenence < 0:
                        unit.location = None
                        print("\n       Player "+str(unit.team)+" cannot sustain thier "+str(unit.unit_type)+" due to maintenence.")
                    else:
                        self.players[unit.team - 1].money -= maintenence

   
    def save_goal_check(self):
        for player in self.players:
            if player.money > player.save_goal:
                player.how_to_spend()
                player.save_goal = random.randint(6,70)
            else:
                print("\n       Player "+str(self.players.index(player) + 1)+" didn't buy anything this turn")

    def complete_movement_phase(self):
        self.num_turns += 1
        print("\n TURN " + str(self.num_turns) + "  MOVEMENT PHASE")
        units = [[],[]]
        for coords in self.board.game_data:
            for unit in self.board.game_data[coords]:
                if unit.unit_type != "Planet" and unit.unit_type != "Colony" and unit.unit_type != "ShipYard":
                    units[unit.team - 1].append(unit)
        for j in range(len(units)):
            for i in range(len(self.players[j].movement_calcs('movements'))):
                print("\n Player "+str(j + 1)+" - Move " + str(i+1))
                for unit in units[j]:
                    if unit.unit_type == 'Colony Ship':
                        self.check_for_planet(unit)
                        unit.move()
                        self.correct_board()
                    else:
                        old_loc = unit.location
                        for i in range(self.players[j].movement_calcs('movements')[i]):
                            unit.move()
                            self.correct_board()
                        if unit.location is not None and unit.location != old_loc:
                            print("\n   Unit "+str(units[j].index(unit))+" ("+str(unit.unit_type)+") moves from "+str(old_loc)+" to "+str(unit.location))
        print("\n ------------- End of Movement Phase--------------")
    
    def complete_combat_phase(self):
        print("\n TURN " + str(self.num_turns) + "  COMBAT PHASE")
        p1_units = []
        p2_units = []
        for coord in self.board.game_data:
            for unit in self.board.game_data[coord]:
                if unit.unit_type != "Planet" and unit.unit_type != "Colony":
                    if unit.team == 1:
                        p1_units.append(unit)
                    elif unit.team == 2:
                        p2_units.append(unit)
        for p1_ship in p1_units:
            for p2_ship in p2_units:
                if p1_ship.location == p2_ship.location and p1_ship.location is not None:
                        self.locate_combat(p1_ship,p2_ship)
        self.colony_combat()
        print("\n ------------- End of Combat Phase--------------")
        
    


    def complete_economic_phase(self):
        print("\n TURN " + str(self.num_turns) + "  ECONOMIC PHASE")
        print("\n   Income From Colonies:")
        self.money_from_colonies()
        print("\n   Maintenence:")
        self.maintenence()
        print("\n   New ships and Tech upgrades:")
        self.save_goal_check()
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
            p1_check = [unit for coord in self.board.game_data for unit in self.board.game_data[coord] if unit.unit_type != "Planet" and unit.unit_type != "Colony" and unit.team == 1 and unit.location is not None]
            p2_check = [unit for coord in self.board.game_data for unit in self.board.game_data[coord] if unit.unit_type != "Planet" and unit.unit_type != "Colony" and unit.team == 2 and unit.location is not None]
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
