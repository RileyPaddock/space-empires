import random
import math
import logging

class CombatEngine:

    def __init__(self, game):
        self.game = game
        self.battles = []
        self.allies = []
        self.enemies = []
        self.battle_order = []
        self.dead_ships = []
        self.seed = None
        self.roll_type = self.game.dice_rolls
        self.dice = {'ascending' : [1,2,3,4,5,6,7,8,9,10], 'descending' : [10,9,8,7,6,5,4,3,2,1]}
        self.roll_index = -1
        self.dice_roll = 0
        self.combat_state = None

    def roll_dice(self):
        if self.roll_type == 'random':
            self.dice_roll = math.floor(10*random.random()) + 1
        else:
            if self.roll_index < 9:
                self.roll_index += 1
            else:
                self.roll_index = 0
            self.dice_roll = self.dice[self.roll_type][self.roll_index]

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
        battles = self.find_battles()
        if self.game.logging:
            self.game.logger.info("BEGINNING OF TURN %s COMBAT PHASE\n",str(self.game.num_turns))
            if len([key for key in battles]) > 0:
                self.game.logger.info("\tCombat Locations:\n")
            for coords in battles:
                self.game.logger.info("\t\t%s\n",coords)
                for unit in self.sort_by_attack_grade(battles[coords]):
                    if unit.unit_type != "Colony":
                        self.game.logger.info("\t\t\tPlayer %s %s",str(unit.player.player_num+1), str(unit.unit_num))


        for coords, units in battles.items():
            if self.game.logging: self.game.logger.info("\n\tCombat at %s\n ",str(coords))
            self.combat_finished = False
            self.resolve_combat(units)
            if self.game.complete:
                return
            self.game.num_combats += 1
            self.reset_stats()
            self.game.board.update(self.game.players)
        self.game.board.update(self.game.players)
        if self.game.logging:
            if len([key for key in battles]) > 0:
                self.game.logger.info("\tSurvivors:\n")
            for coords in battles:
                self.game.logger.info("\t\t%s\n",coords)
                for unit in self.sort_by_attack_grade(battles[coords]):
                    if unit.unit_type != "Colony" and unit.alive:
                        self.game.logger.info("\t\t\tPlayer %s %s",str(unit.player.player_num+1), str(unit.unit_num))
            if len([coords for coords in battles]) > 0:
                self.game.logger.info("\nEND OF TURN %s COMBAT PHASE\n",str(self.game.num_turns))
            else:
                self.game.logger.info("END OF TURN %s COMBAT PHASE\n",str(self.game.num_turns))


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
        targeted_unit_data = player.strategy.decide_which_unit_to_attack(self.get_combat_state(), tuple(attacker.location), attacker.unit_num)
        targeted_unit_data = self.get_combat_state()[tuple(attacker.location)][targeted_unit_data]
        targeted_enemy = None
        for unit in units:
            if unit.unit_num == targeted_unit_data['num'] and unit.player.player_num == targeted_unit_data['player']:
                targeted_enemy = unit
        return targeted_enemy

    def sort_by_attack_grade(self, units):
        return sorted(units,key = lambda unit:
        (unit.time_at_space,-unit.class_num,unit.player.player_num),reverse=True)

    def attack(self, attacker, defender): 
        self.roll_dice()
        hit_threshold = (attacker.strength + attacker.technologies['attack']) - (defender.defense + defender.technologies['defense'])
        if self.game.logging:
            self.game.logger.info("\t\tAttacker: Player %s %s",str(attacker.player.player_num+1), str(attacker.unit_num))
            self.game.logger.info("\t\tDefender: Player %s %s",str(defender.player.player_num+1), str(defender.unit_num))
            self.game.logger.info("\t\tHighest Roll for Hit: %s",str(hit_threshold))
            self.game.logger.info("\t\tDie Roll: %s",str(self.dice_roll))
        if self.dice_roll <= hit_threshold or self.dice_roll == 1:
            if self.game.logging: self.game.logger.info("\t\tHit!")
            defender.hit()
            if not defender.alive:
                if self.game.logging: self.game.logger.info("\t\tPlayer %s %s was destroyed\n",str(defender.player.player_num+1), str(defender.unit_num))
                self.dead_ships.append(defender)
                if defender.unit_type == 'Colony':
                    if defender.colony_type == 'Home':
                        self.game.winner = attacker.player.player_num
                        self.game.complete = True
                        self.combat_finished = True
        elif self.game.logging:
            self.game.logger.info("\t\t(Miss)\n")
            
            

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
        ordered_units = self.sort_by_attack_grade(units)
        ordered_units = [unit for unit in ordered_units if unit.alive]
        unit_dicts = [{'player' : unit.player.player_num, 'unit': unit.unit_num} for unit in ordered_units]
        if self.combat_finished:
            return
        else:
            self.combat_finished = False
            self.units = units
            self.battle_order = self.sort_by_attack_grade(self.units)
            while not self.combat_finished:
                self.battle_order = self.sort_by_attack_grade(self.units)
                self.units = self.battle_order
                for unit in self.battle_order:
                    if unit.alive:
                        if not unit.can_atk:
                            continue
                        self.sort_units(units, unit.player)
                        enemy = self.which_ship_to_attack(unit.player, unit, self.units)
                        self.attack(unit, enemy)
                        self.check_battle_status(self.units)
                        if self.combat_finished:
                            if len(self.units) >= 1:
                                self.remove_dead_ships(self.units)
                                return
                                break
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
                                player.build_colony(unit.location, colony_type = 'Normal', colony_ship = unit)


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
            unit_dicts = [{'player' : unit.player.player_num, 'type': unit.unit_type, 'num': unit.unit_num} for unit in ordered_units]
            combat_state[coords] = unit_dicts
        return combat_state
