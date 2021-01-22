import random

class CombatEngine:

    def __init__(self, game):
        self.game = game
        self.battles = []
        self.allies = []
        self.enemies = []
        self.battle_order = []
        self.dead_ships = []
        self.roll_type = self.game.dice_rolls
        self.dice = {'ascending' : [1,2,3,4,5,6], 'descending' : [6,5,4,3,2,1], 'random' : self.generate_random_rolls()}
        self.roll_index = -1
        self.dice_roll = 0
        self.combat_state = None

    def roll_dice(self):
        if self.roll_index < 5:
            self.roll_index += 1
        else:
            self.roll_index = 0
        self.dice_roll = self.dice[self.roll_type][self.roll_index]
    
    def generate_random_rolls(self):
        rolls = []
        possible_rolls = [1,2,3,4,5,6]
        while len(rolls)<6:
            rand_choice = random.choice([possible_rolls])
            rolls.append(rand_choice)
            del possible_rolls[possible_rolls.index(rand_choice)]

    def find_battles(self):
        potential_battles = self.game.board.get_all_active_data()
        non_combat_coords = {}
        for coords, units in potential_battles.items():
            self.reset_stats()
            self.sort_units(units, units[0].player)
            if len(self.enemies) == 0:
                non_combat_coords[coords] = units
            self.reset_stats()
        for coords, units in non_combat_coords.items():
            del potential_battles[coords]
        self.combat_state = potential_battles
        return potential_battles

    def complete_combat_phase(self):
        if self.game.logging:
            print('START OF COMBAT PHASE')
        battles = self.find_battles()
        for coords, units in battles.items():
            if self.game.logging:
                print('Battle at: '+ str(coords))
            self.combat_finished = False
            self.resolve_combat(units)
            self.reset_stats()
            self.game.board.update(self.game.players)
        self.game.board.update(self.game.players)
        if self.game.logging:
            print('END OF COMBAT PHASE')


    def sort_units(self, units, player):
        self.enemies = []
        self.allies = []
        self.units = units
        for unit in self.units:
            if unit.alive:
                if unit.player == player:
                    self.allies.append(unit)
                else:
                    self.enemies.append(unit)

    def reset_stats(self):
        self.units = []
        self.battle_order = []
        self.enemies = []
        self.allies = []
        self.dead_ships = []

    def check_battle_status(self, units):
        units = [unit for unit in units if unit.alive]
        self.combat_finished = False
        if len(units) > 1:
            self.sort_units(units, units[0].player)
            if len(self.enemies) > 0:
                self.combat_finished = False
                return
            self.combat_finished = True
            return
        else:
            self.combat_finished = True
            return

    def which_ship_to_attack(self, player, attacker, units):
        self.sort_units(units, player)
        units = [unit for unit in units if unit.alive]
        targeted_unit_data = player.strategy.decide_which_unit_to_attack(self.get_combat_state(), tuple(attacker.location), units.index(attacker))
        targeted_unit_data = self.get_combat_state()[tuple(attacker.location)][targeted_unit_data]
        targeted_enemy = None
        for unit in units:
            if unit.unit_num == targeted_unit_data['unit'] and unit.player.player_num == targeted_unit_data['player']:
                targeted_enemy = unit
        return targeted_enemy

    def sort_by_attack_grade(self, units):
        for i in range(len(units)):
            for j in range(i + 1, len(units)):
                unit1 = units[i]
                unit2 = units[j]
                unit1_ability = unit1.player.technologies['attack'] + unit1.player.technologies['defense']
                unit2_ability = unit2.player.technologies['attack'] + unit2.player.technologies['defense']
                if (unit1.attack_grade + unit1_ability) < (unit2.attack_grade + unit2_ability):
                    units[i], units[j] = units[j], units[i]
                elif (unit1.attack_grade + unit1_ability) == (unit2.attack_grade + unit2_ability):
                    if unit1.player.player_num > unit2.player.player_num:
                        units[i], units[j] = units[j], units[i]
        return units

    def attack(self, attacker, defender):
        self.roll_dice()
        hit_threshold = attacker.attack - defender.defense
        if self.game.logging:
            print('Player',attacker.player.player_num, attacker.unit_type, attacker.unit_num,'Shoots at','Player',defender.player.player_num, defender.unit_type, defender.unit_num)
            print('Threshold:', hit_threshold)
            print('Player',attacker.player.player_num,'Rolled a',self.dice_roll)
        if self.dice_roll <= hit_threshold or self.dice_roll == 1:
            if self.game.logging:
                print('Hit!')
            defender.hit()
            if not defender.alive:
                self.dead_ships.append(defender)
                if self.game.logging:
                    print('Unit Destroyed')
        else:
            if self.game.logging:
                print('Miss!')

    def remove_non_fighters(self, units):
        non_combat_coords = []
        for unit in units:
            if unit.unit_type == 'Colonyship':
                non_combat_coords.append(unit)
        if len(non_combat_coords) == len(units):
            self.combat_finished = True
            return units
        else:
            for passive in non_combat_coords:
                units.remove(passive)
                passive.destroy()
            status = self.check_battle_status(units)
            return units

    def remove_dead_ships(self, units):
        self.units = units
        for unit in units:
            if unit in self.dead_ships:
                self.units.remove(unit)
        return self.units

    
    def resolve_combat(self, units):
        units = self.remove_non_fighters(units)
        if self.combat_finished:
            return
        else:
            self.combat_finished = False
            self.units = units
            self.battle_order = self.sort_by_attack_grade(self.units)
            if self.game.logging:
                print('In Combat: ')
                for unit in self.battle_order:
                    print(' Player: '+ str(unit.player.player_num) + ', '+str(unit.unit_type) + ', '+str(unit.unit_num))
            while not self.combat_finished:
                self.battle_order = self.sort_by_attack_grade(self.units)
                self.units = self.battle_order
                for unit in self.battle_order:
                    if unit.alive:
                        if not unit.can_attack:
                            continue
                        self.sort_units(units, unit.player)
                        enemy = self.which_ship_to_attack(unit.player, unit, self.units)
                        self.attack(unit, enemy)
                        self.check_battle_status(self.units)
                        if self.combat_finished:
                            if len(self.units) >= 1:
                                self.remove_dead_ships(self.units)
                                if self.game.logging:
                                    print('Battle Is combat_finished')
                                    print('Player', self.units[0].player.player_num,'Units Win!')
                                    print('Survivors:')
                                    for unit in self.units:
                                        if unit.alive:
                                            print(" ",unit.unit_type, unit.unit_num)
                                return
                self.units = self.remove_dead_ships(self.units)

    def colonize(self):
        planet_coords = [planet.location for planet in self.game.board.planets]
        self.game.board.update(self.game.players)
        for player in self.game.players:
            for unit in player.units:
                if unit.unit_type == 'Colony Ship':
                    if unit.location in planet_coords:
                        planet = self.game.board.planets[planet_coords.index(unit.location)]
                        if not planet.colonized:
                            if player.strategy.will_colonize_planet(unit.location, self.game.game_state()):
                                player.build_colony(unit.location, col_type = 'Normal', colony_ship = unit)
                                if self.game.logging:
                                    print('Player', player.player_num,'colonized a planet at',unit.location)

    def attack_colony(self):
        planet_coords = [planet.location for planet in self.game.board.planets]
        self.game.board.update(self.game.players)
        for player in self.game.players:
            for unit in player.units:
                if unit.location in planet_coords:
                    planet = self.game.board.planets[planet_coords.index(unit.location)]
                    if planet.colonized:
                        if unit.can_attack and planet.colony.player != unit.player:
                            self.attack(attacker = unit, defender = planet.colony)

    def get_combat_state(self):
        combat_state = {}
        for coords,units in self.combat_state.items():
            ordered_units = self.sort_by_attack_grade(units)
            ordered_units = [unit for unit in ordered_units if unit.alive]
            unit_dicts = [{'player' : unit.player.player_num, 'unit': unit.unit_num} for unit in ordered_units]
            combat_state[coords] = unit_dicts
        return combat_state
                        