class DumbStrategy:
    def __init__(self,player_num):
        self.player_num = player_num

    def will_colonize_planet(self,colony_ship, game_state):
      return False

    def decide_ship_movement(self,ship_index, game_state):
        if game_state['players'][self.player_num]["units"][ship_index]["coords"][1][0]<4:
             return (1,0)
        else:
            return (0,0)

    def decide_purchases(self,game_state):
        if game_state['players'][self.player_num]['cp']>=game_state['unit_data']['Scout']['cp_cost']:
          return {
           'units': [{'type': 'Scout', 'coords': (2,self.player_num*4)}],
           'technology': [] 
          }


    def decide_removals(self, game_state):
      return game_state["player"][self.player_num]["unit"][0]["unit number"]-1#assuming unit number starts at 1
  
    def decide_which_ship_to_attack(self,combat_state, coords, attacker_index):
      return None

    def decide_which_units_to_screen(self, combat_state):
      return []
