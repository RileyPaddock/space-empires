import logging
class MovementEngine:

    def __init__(self, board, game):
        self.board = board
        self.game = game
        if self.game.level < 3:
            self.phases = 1
        else:
            self.phases = 3
        self.movement_data = {'1' : [1,1,1,2,2,2], '2': [1,2,2,2,2,3], '3': [1,2,2,2,3,3]}
        self.movement_phase = None


    def complete_movement_phase(self):
        self.game.movement_phase = 'Movement'
        if self.game.logging:
            print('BEGINNING OF MOVEMENT PHASE')
        for i in range(self.phases):
            if self.game.logging:
                print('Movement', i + 1)
            self.movement_phase = i
            for player in self.game.players:
                if self.game.logging:
                    print('--------------------')
                    print('Player', player.player_num,'is moving')
                self.move_player_units(player, i+1)
                self.board.update(self.game.players)
                if self.game.logging:
                    print('--------------------')
        self.game.combat_engine.colonize()
        self.board.update(self.game.players)
        if self.game.logging:
            print('END OF MOVEMENT PHASE')
                

    def move_player_units(self, player, movement_round):
        self.game.current_player = player.player_num
        for unit in player.units:
            if unit.moveable:
                ship_movements = self.movement_data[str(movement_round)][unit.movement - 1]
                unit_index = player.units.index(unit)
                for _  in range(ship_movements):
                    translation = player.strategy.decide_ship_movement(unit_index, self.game.game_state())
                    translation = [translation[0], translation[1]]

                    unit.move(translation, self.game.board_size)
    
    def generate_movement_state(self):
        movement_dict = {}
        movement_dict['Phase'] = self.movement_phase
        return movement_dict