import random
class CombatEngine():
    def __init__(self, players, units_in_combat,logging, rolls):
        self.units = self.sort_by_attack_grade(units_in_combat)
        self.players = players
        self.logging = logging
        self.location = self.units[0].location
        self.p1_ships = [p1_ship for p1_ship in self.units if p1_ship.team == 1]
        self.p2_ships = [p2_ship for p2_ship in self.units if p2_ship.team == 2]
        self.not_random = []
        self.not_random = rolls
        self.combat_turn = 0
        self.combat_state()

    def generate_combat_array(self):
        return [{'player':unit.team,'unit_num':unit.unit_num} for unit in self.units if unit.location is not None]

    
    def update_units(self):
        temp = self.units
        self.units = []
        for unit in temp:
            if unit.location is not None:
                self.units.append(unit)
        self.p1_ships = [p1_ship for p1_ship in self.units if p1_ship.team == 1]
        self.p2_ships = [p2_ship for p2_ship in self.units if p2_ship.team == 2]


    def sort_by_attack_grade(self,set_of_units):
        for i in range(len(set_of_units)):  
            for j in range(0, len(set_of_units)-(i+1)):  
                if (ord(set_of_units[j].attack_grade) > ord(set_of_units[j + 1].attack_grade)):  
                    temp = set_of_units[j]  
                    set_of_units[j]= set_of_units[j + 1]  
                    set_of_units[j + 1]= temp  
        for i in range(len(set_of_units)):  
            for j in range(0, len(set_of_units)-(i+1)): 
                if set_of_units[j].unit_type == set_of_units[j+1].unit_type: 
                    if (set_of_units[j].age < set_of_units[j + 1].age):  
                        temp = set_of_units[j]  
                        set_of_units[j]= set_of_units[j + 1]  
                        set_of_units[j + 1]= temp  
        return set_of_units  

    def combat_state(self):
        if self.logging:
            print("\nATTACKING ORDER | PLAYER |        SHIP        | HEALTH  |")
            print("---------------------------------------------------------")
        unit_num = 1
        for unit in self.units:
            if unit.unit_type != 'Colony Ship' and unit.unit_type != 'Decoy':
                if self.logging:
                    print("       "+str(unit_num)+"        |    "+str(unit.team)+"   |         "+str(unit.unit_type)+"          |    "+str(unit.armor)+"    |")
                unit_num+=1

    def resolve_combat(self):
        for ship in self.units:
            ship.age += 1
            if ship.location is not None:
                if ship.unit_type == 'Colony Ship':
                    ship.location = None
                    self.update_units()
        while len(self.p1_ships) > 0 and len(self.p2_ships) > 0:
            for ship in self.units:
                if ship.location is not None:
                    if ship.team == 1 and len(self.p2_ships)>0:
                        self.p2_attack(ship)
                    elif ship.team == 2 and len(self.p1_ships)>0:
                        self.p1_attack(ship)
                    
    def p2_attack(self, ship):
        i = self.players[1].strategy.decide_which_unit_to_attack(ship.unit_state(), self.generate_combat_array())
        enemy_ship = self.units[i]
        if self.logging:
            print("\n Combat at "+str(ship.location)+" between Player 2's "+str(ship.unit_type)+" and Player 1's "+str(enemy_ship.unit_type)+".")
        self.attack(ship, enemy_ship)
        self.update_units()
        self.combat_state()
    
    def p1_attack(self, ship):
        i = self.players[0].strategy.decide_which_unit_to_attack(ship.unit_state(), self.generate_combat_array())
        enemy_ship = self.units[i]
        if self.logging:
            print("\n Combat at "+str(ship.location)+" between Player 1's "+str(enemy_ship.unit_type)+" and Player 2's "+str(ship.unit_type)+".")
        self.attack(ship, enemy_ship)
        self.update_units()
        self.combat_state()

    def attack(self, p1_ship, p2_ship):
        if (p1_ship.shorthand == 'Dc' or p1_ship.shorthand == 'CS') and (p2_ship.shorthand == 'Dc' or p2_ship.shorthand == 'CS'):
            p1_ship.location = None
            p2_ship.location = None
            if self.logging:
                print("\n   Player 1's "+str(p1_ship.unit_type)+" and Player 2's "+str(p2_ship.unit_type)+" destroyed each other")
        elif p1_ship.shorthand == 'Dc' or p1_ship.shorthand == 'CS':
            p1_ship.location = None
            if self.logging:
                print("\n   Player " + str(p2_ship.team) + "'s "+str(p2_ship.unit_type)+" destroyed Player " + str(p1_ship.team) + "'s " +str(p1_ship.unit_type))
        elif p2_ship.shorthand == 'Dc' or p2_ship.shorthand == 'CS':
            p2_ship.location = None
            if self.logging:
                print("\n   Player " + str(p1_ship.team) + "'s "+str(p1_ship.unit_type)+" destroyed Player " + str(p2_ship.team) + "'s " +str(p2_ship.unit_type))
        else:
            self.attack_real_battle(p1_ship, p2_ship)

    def attack_real_battle(self,p1_ship, p2_ship):
        rand = self.not_random(self.combat_turn%6)
        hit_threshold = ((p1_ship.strength + p1_ship.attack_tech) - (p2_ship.defense  + p2_ship.defense_tech)) - rand
        if self.logging:
            print("\nAttack "+str(self.combat_turn + 1)) 
            print("\n   Attacker: Player "+str(p1_ship.team)+" "+str(p1_ship.unit_type))
            print("\n   Defender: Player "+str(p2_ship.team)+" "+str(p2_ship.unit_type))
            print("\n   Hit Threshold: "+str(hit_threshold + rand))
            print("\n   Dice Roll: "+str(rand))
        self.combat_turn += 1
        if rand == 1 or hit_threshold >= 0:
            if self.logging:
                print("\n   Hit or Miss: Hit")
            if p2_ship.armor == 1:
                p2_ship.location = None
                if self.logging:
                    print("\n   Player " + str(p1_ship.team) + "'s "+str(p1_ship.unit_type)+" destroyed Player " + str(p2_ship.team) + "'s " +str(p2_ship.unit_type))
            else:
                p2_ship.armor -= 1
                if self.logging:
                    print("\n   Player " + str(p1_ship.team) + "'s "+str(p1_ship.unit_type)+" hit Player " + str(p2_ship.team) + "'s "+ str(p2_ship.unit_type) + " but it still has " + str(p2_ship.armor) + " armor remaining!")

        else:
            if self.logging:
                print("\n   Hit or Miss: Miss")
                print("\n   Player "+str(p1_ship.team)+"'s "+ str(p1_ship.unit_type)+" missed Player "+str(p2_ship.team)+"'s " + str(p2_ship.unit_type))
                
    def find_enemy_ships_at_colonies(self,player):
        colony_in_combat = None
        for ship in self.units:
                if ship.unit_type == 'Colony':
                    colony_in_combat = ship
                    break
        if colony_in_combat is not None:
            for ship in self.units:
                if ship.unit_type != "Planet" and ship.unit_type != 'Colony':
                        if ship.shorthand == 'Dc':
                            ship.location = None
                        else:
                            self.resolve_combat_at_colony(colony_in_combat,ship)

    def resolve_combat_at_colony(self,colony_in_combat,ship):
        if colony_in_combat.base != False:
            if ord(ship.attack_grade) < ord(colony_in_combat.base.attack_grade):
                self.attack(ship, colony_in_combat.base)
            elif ord(ship.attack_grade) > ord(colony_in_combat.base.attack_grade):
                self.attack(colony_in_combat.base, ship)
        else:
            if colony_in_combat.armor == 1:
                colony_in_combat.location = None
            else:
                self.attack(ship,colony_in_combat)
                        