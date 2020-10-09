from player import Player
class RileyStrategyPlayer(Player):
    def __init__(self, player_num, start_pos, game_data,logging):
        super().__init__(player_num, start_pos, game_data,logging)
        self.player_type = 'Riley'
        self.money = 0
        self.attack_tech = 0
        self.defense_tech = 0
        self.movement_tech = 1
        self.ship_yard_tech = 1
        self.ship_size_tech = 1
        self.shipyard_capacity = 0.5 + 0.5*self.ship_yard_tech


    def calc_distance(coords_1, coords_2):
        x_1, y_1 = coords_1
        x_2, y_2 = coords_2
        return abs(x_2 - x_1) + abs(y_2 - y_1)
    def will_colonize_planet(self,colony_ship, planet, game):
        closest_player_ship = [self.calc_distance(colony_ship, p1_home_colony), self.calc_distance(colony_ship, p2_home_colony)]
        for unit in game_board:
            if unit.unit_type != "colony ship" or "planet" or "decoy":
                if unit.team == 1:
                    if self.calc_distance(unit, colony_ship) < closest_player_ship[0]:
                        closest_player_ship[0] = self.calc_distance(unit, colony_ship)
                if unit.team == 2:
                    if self.calc_distance(unit, colony_ship) < closest_player_ship[1]:
                        closest_player_ship[1] = self.calc_distance(unit, colony_ship)
        if closest_player_ship.index(min(closest_player_ship)) == colony_ship.team - 1:
            return True
        else:
            return False

    def decide_ship_movement(self, ship, game):
        if ship.group == 'attack':
            attack_coords = self.closest_unit(ship,'colony')
            path = self.calc_shortest_path(ship.location, attack_coords)
        if ship.group == 'colonize':
            attack_coords = self.closest_unit('planet')
            path = self.calc_shortest_path(ship.location, attack_coords)
        desired_coords = [coord for coord in ship.location]
        for movement in path:
            if movement == 'up':
                desired_coords[1]+=1
            elif movement == 'down':
                desired_coords[1]-=1
            elif movement == 'right':
                desired_coords[0] += 1
            elif movement == 'left':
                desired_coords[0] -= 1
        return desired_coords

        
    def closest_unit(self,base_unit, seeking_unit_type):
        closest_unit = None
        for unit in game_board:
            if unit.unit_type == seeking_unit_type:
                if closest_unit is None or self.calc_distance(unit, base_unit) < self.calc_distance(closest_unit, base_unit):
                    closest_unit = unit
        return closest_unit.location

    def calc_shortest_path(self,start, end):
        path = []
        movements = ['up','down','left','right']
        active = start
        while active != end:
            possible_coords = [self.calc_distance([active[0],active[1]+1]),self.calc_distance([active[0],active[1]-1]),self.calc_distance([active[0]-1,active[1]]),self.calc_distance([active[0]+1,active[1]])]
            path.append(movements[possible_coords.index(min(possible_coords))])
        return path
