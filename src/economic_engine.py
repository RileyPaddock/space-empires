class EconomicEngine:
    def __init__(self, players, board, logging = True):
        self.players = players
        self.board = board
        self.logging = logging

    def generate_state(self, player):
        state = {}
        state['maintenence cost'] = sum([unit.hull_size for unit in self.active_units[player - 1]])
        state['income'] = self.calc_income()[player - 1]
        return state

    def calc_income(self):
        player_income = [0 for player in self.players]
        self.board.update_board()
        for coord in self.players[0].board.game_data:
            for unit in self.players[0].board.game_data[coord]:
                if unit.unit_type == "Colony":
                    if unit.location == self.players[unit.team - 1].start_pos:
                         player_income[unit.team - 1] += 20
                    else:
                        player_income[unit.team - 1] += unit.armor
        return player_income
        
    def distribute_income(self, player_income):
        for i in range(len(player_income)):
            self.players[i].money += player_income[i]

        if self.logging:
            print("\n       Player 1 earned "+str(player_income[0])+" CP's")
            print("\n       Player 2 earned "+str(player_income[1])+" CP's")

    
    def active_units(self):
        maintainable_units = []
        for player in self.players:
            maintainable_units.append([])
            i = self.players.index(player)
            for coord in player.board.game_data:
                for unit in player.board.game_data[coord]:
                    if unit.unit_type != "Planet" and unit.unit_type != "Colony" and  unit.unit_type != 'CS' and unit.shorthand != 'Dc' and unit.location is not None and unit.team==player.player_num:
                        maintainable_units[i].append(unit)
            maintainable_units[i] = self.sort_by_hull_size(maintainable_units[i])
        return maintainable_units
            
    def maintenence(self):
        maintainable_units = self.active_units()
        for player_units in maintainable_units:
            for unit in player_units:
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

    def spend(self):
        for player in self.players:
            player.spend()