from Planet import Planet
from Player import Player
import random
from Units.Colony import Colony
from Units.ShipYard import ShipYard

class Game:
    def __init__(self):
        self.num_turns = 0
        self.winner = None 
        self.players = [Player(1,(3,1)), Player(2,(3,5))]
        self.planets = self.generate_planets()
        
    def generate_planets(self):
        planet_locations = [Planet(self.players[0].start_pos),Planet(self.players[1].start_pos)]
        while len(planet_locations) <= 10:
            rand_x = random.randint(0,6)
            rand_y = random.randint(0,6)
            if Planet((rand_x,rand_y)) not in planet_locations:
                planet_locations.append(Planet((rand_x,rand_y)))
        return planet_locations
    
    # def render_game(self, data, gridsize=[7,7], fontsize=12):
    #     fig, ax = plt.subplots()
    #     ax.xaxis.set_minor_locator(MultipleLocator(0.5))
    #     ax.yaxis.set_minor_locator(MultipleLocator(0.5))

    #     for item in data:
    #         x = item['x']
    #         y = item['y']
    #         color = item['color']
    #         label = item['label']
    #         ax.text(x, y, label, fontsize=fontsize, color=color, horizontalalignment='center', verticalalignment='center')

    #     x_max, y_max = gridsize
    #     plt.xlim(-0.5 ,x_max-0.5)
    #     plt.ylim(-0.5, y_max-0.5)

    #     plt.grid(which='minor')
    #     plt.show()

    def state(self):
        for i in range(len(self.players)):
            print("Player "+str(i+1)+":")
            print("Name          | Attack Class | Attack Strength | Attack Tech | Defense Strength | Defense Tech |    Location   |")
            for j in range(len(self.players[i].units)):
                if self.players[i].units[j].location is None:
                    pass
                else:
                    correct_num_of_sapces = [" " for k in range(14-len(self.players[i].units[j].unit_type))]
                    print(str(self.players[i].units[j].unit_type) + ''.join(correct_num_of_sapces) + "|      " + str(self.players[i].units[j].attack_grade) + "       |       " + str(self.players[i].units[j].strength) + "         |      " +str(self.players[i].attack_tech) + "      |        " + str(self.players[i].units[j].defense) + "         |       "  + str(self.players[i].defense_tech) + "      |     " + str(self.players[i].units[j].location) + "    |")
            print("__________________________________________________________________________________")


    def locate_combat(self,p1_ship,p2_ship):
        p1_ships = []
        p2_ships = []
        for unit1 in self.players[0].units:
            if unit1.location == p1_ship.location:
                p1_ships.append(unit1)
        for unit2 in self.players[1].units:
            if unit2.location == p1_ship.location:
                p2_ships.append(unit2)
        order_of_combat = self.sort_by_attack_grade(p1_ships + p2_ships)
        while len([p1_ship.location for p1_ship in p1_ships if p1_ship.location is not None]) > 0 and len([p2_ship.location for p2_ship in p2_ships if p2_ship.location is not None]) > 0:
            for ship in order_of_combat:
                if ship.unit_type == 'Colony Ship':
                    ship.location = None
                else:
                    if ship.location is not None:
                        if ship.team == 1:
                            rand = random.choice(p2_ships)
                            print("Combat at "+str(ship.location)+" between Player 1's "+str(ship.unit_type)+" and Player 2's "+str(rand.unit_type)+".")
                            self.attack(ship, rand)
                        elif ship.team == 2:
                            rand = random.choice(p1_ships)
                            print("Combat at "+str(ship.location)+" between Player 1's "+str(rand.unit_type)+" and Player 2's "+str(ship.unit_type)+".")
                            self.attack(ship, rand)

        

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
            print("Two Decoys Destroyed Each other")
        elif p1_ship.shorthand == 'Dc':
            p1_ship.location = None
            print("Player " + str(p2_ship.team) + "'s "+str(p2_ship.unit_type)+" wins!")
        elif p2_ship.shorthand == 'Dc':
            p2_ship.location = None
            print("Player " + str(p1_ship.team) + "'s "+str(p1_ship.unit_type)+" wins!")
        else:
            rand = random.randint(1,6)
            hit_threshold = ((p1_ship.strength + self.players[0].attack_tech) - (p2_ship.defense  + self.players[1].defense_tech)) - rand

            if rand == 1 or hit_threshold >= 0:
                if p2_ship.armor == 1:
                    p2_ship.location = None
                    print("Player " + str(p1_ship.team) + "'s "+str(p1_ship.unit_type)+" wins!")
                else:
                    p2_ship.armor -= 1
                    print("Player " + str(p1_ship.team) + "'s "+str(p1_ship.unit_type)+" hit Player " + str(p2_ship.team) + "'s "+ str(p2_ship.unit_type) + " but it still has " + str(p2_ship.armor) + " armor remaining!")

            else:
                print("Missed Shot!")

    def check_for_planet(self, colony_ship):
        for planet in self.planets:
            if planet.location == colony_ship.location and not planet.has_a_colony:
                colony_ship.location = None
                planet.player = colony_ship.team   
                planet.has_a_colony = True 
                planet.colony = Colony(colony_ship.team, planet.location,[],False)
                self.players[colony_ship.team -1].colonies.append(Colony(colony_ship.team, planet.location,[],False))
            for player in self.players:
                if planet.location == player.start_pos and planet.player == player.player_num:
                    for _ in range(4):
                        planet.colony.shipyards.append(ShipYard(player.player_num, player.start_pos))
                        player.colonies[0].shipyards.append(ShipYard(player.player_num, player.start_pos))
                        


    def money_from_colonies(self):
        for planet in self.planets:
            if planet.has_a_colony:
                if planet.player == 1:
                    self.players[0].money += planet.colony.armor
                elif planet.player == 2:
                    self.players[1].money += planet.colony.armor        


    def maintenence(self):
        for player in self.players:
            for unit in player.units:
                if unit.shorthand != 'CS' and unit.shorthand != 'Dc':
                    maintenence = unit.hull_size/3
                    if player.money - maintenence < 0:
                        unit.location = None
                        print("Cannot sustain Player "+ str(unit.team) +"'s "+str(unit.unit_type))
                    else:
                        player.money -= maintenence

    def complete_turn(self):
        self.num_turns += 1
        for player in self.players:
            for unit in player.units:
                if unit.unit_type == 'Colony Ship':
                    self.check_for_planet(unit)
                    unit.move()
                else:
                    for i in range(unit.speed + self.players[unit.team - 1].speed_tech):
                        unit.move()
        # self.plot_game_state()

        for p1_ship in self.players[0].units:
            for p2_ship in self.players[1].units:
                if p1_ship.location == p2_ship.location:
                    if p1_ship.shorthand == 'Dc' and p2_ship.shorthand == 'Dc':
                        p1_ship.location = None
                        p2_ship.location = None
                        pass
                    elif p1_ship.shorthand == 'Dc':
                        p1_ship.location = None
                        pass
                    elif p2_ship.shorthand == 'Dc':
                        p2_ship.location = None
                        pass
                    else:
                        self.locate_combat(p1_ship,p2_ship)

        for p1_ship in self.players[0].units:
            for planet in self.planets:
                if p1_ship.location == planet.location and planet.has_a_colony and planet.player != 1:
                    colony_in_combat = planet.colony
                    if p1_ship.shorthand == 'Dc':
                        p1_ship.location = None
                        pass
                    else:
                        for colony in self.players[planet.colony.team -1].colonies:
                            if colony.location == planet.location:
                                colony_in_combat = colony
                        if colony_in_combat.base != False:
                            if ord(p1_ship.attack_grade) < ord(colony_in_combat.base.attack_grade):
                                self.attack(p1_ship, colony_in_combat.base)
                            elif ord(p1_ship.attack_grade) > ord(colony_in_combat.base.attack_grade):
                                self.attack(colony_in_combat.base, p1_ship)
                        else:
                            if colony.armor == 1:
                                planet.reset()
                                for colony in self.players[0].colonies:
                                    if colony.location == planet.location:
                                        colony.shipyards = []
                            else:
                                self.attack(p1_ship,colony_in_combat)

        for p2_ship in self.players[1].units:
            for planet in self.planets:
                if p2_ship.location == planet.location and planet.has_a_colony and planet.player != 2:
                    colony_in_combat = planet.colony
                    if p2_ship.shorthand == 'Dc':
                        p2_ship.location = None
                        pass
                    else:
                        for colony in self.players[planet.colony.team -1].colonies:
                            if colony.location == planet.location:
                                colony_in_combat = colony
                        if colony_in_combat.base != False:
                            if ord(p2_ship.attack_grade) < ord(colony_in_combat.base.attack_grade):
                                self.attack(p2_ship, colony_in_combat.base)
                            elif ord(p2_ship.attack_grade) > ord(colony_in_combat.base.attack_grade):
                                self.attack(colony_in_combat.base, p2_ship)
                        else:
                            if colony.armor == 1:
                                planet.reset()
                                for colony in self.players[0].colonies:
                                    if colony.location == planet.location:
                                        colony.shipyards = []
                            else:
                                self.attack(p2_ship,colony_in_combat)

        self.maintenence()
        self.money_from_colonies()
        self.save_goal_check()
        
    def save_goal_check(self):
        for player in self.players:
            if player.money > player.save_goal:
                player.how_to_spend()
                player.save_goal = random.randint(6,70)

    def complete_movement_phase(self):
        self.num_turns += 1
        for player in self.players:
            for unit in player.units:
                if unit.unit_type == 'Colony Ship':
                    self.check_for_planet(unit)
                    unit.move()
                else:
                    for i in range(unit.speed + self.players[unit.team - 1].speed_tech):
                        unit.move()

    def colony_combat(self):
        for player in self.players:
            for ship in player.units:
                for planet in self.planets:
                    if ship.location == planet.location and planet.has_a_colony and planet.player != 1:
                        colony_in_combat = planet.colony
                        if ship.shorthand == 'Dc':
                            ship.location = None
                            pass
                        else:
                            for colony in self.players[planet.colony.team -1].colonies:
                                if colony.location == planet.location:
                                    colony_in_combat = colony
                            if colony_in_combat.base != False:
                                if ord(ship.attack_grade) < ord(colony_in_combat.base.attack_grade):
                                    self.attack(ship, colony_in_combat.base)
                                elif ord(ship.attack_grade) > ord(colony_in_combat.base.attack_grade):
                                    self.attack(colony_in_combat.base, ship)
                            else:
                                if colony.armor == 1:
                                    planet.reset()
                                    for colony in self.players[0].colonies:
                                        if colony.location == planet.location:
                                            colony.shipyards = []
                                else:
                                    self.attack(ship,colony_in_combat)

    def complete_combat_phase(self):
        for p1_ship in self.players[0].units:
            for p2_ship in self.players[1].units:
                if p1_ship.location == p2_ship.location:
                        self.locate_combat(p1_ship,p2_ship)
        
        


    def complete_economic_phase(self):
        self.money_from_colonies()
        self.maintenence()
        self.save_goal_check()
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

    

    def run_to_completion(self):
        while True:
            self.complete_movement_phase()
            self.complete_combat_phase()
            self.complete_economic_phase()
            p1_check = [self.players[0].units[i].location for i in range(len(self.players[0].units)) if self.players[0].units[i].location is not None]
            p2_check = [self.players[1].units[i].location for i in range(len(self.players[1].units)) if self.players[1].units[i].location is not None]
            print(p1_check,p2_check)
            if self.num_turns >= 100:
                if len(p1_check) > len(p2_check):
                    self.winner = "Player 1"
                elif len(p1_check) < len(p2_check):
                    self.winner = "Player 2"
                else:
                    self.winner = "Tie"
                break
            if len(p1_check) == 0:
                self.winner = "Player 2"
                break
            if len(p2_check) == 0:
                self.winner = "Player 1"
                break
