import logging
class MovementEngine:

    def __init__(self, board, game):
        self.board = board
        self.game = game
        if self.game.level <= 2:
            self.phases = 3
        else:
            self.phases = 3
        self.movement_data = {'1' : [1,1,1,2,2,2], '2': [1,2,2,2,2,3], '3': [1,2,2,2,3,3]}
        self.movement_phase = None


    def complete_movement_phase(self):
        if self.game.logging:
            self.game.logger.info("BEGINNING OF TURN %s MOVEMENT PHASE",str(self.game.num_turns))
        self.game.movement_phase = 'Movement'
        for i in range(self.phases):
            self.movement_phase = i+1;
            if self.game.logging:
                self.game.logger.info("\n\tMovement Round %s",str(self.movement_phase))
            for player in self.game.players:
                self.move_player_units(player, i+1)
                
                self.board.update(self.game.players)
                
        self.game.combat_engine.colonize()
        self.board.update(self.game.players)
        if self.game.logging:
            self.game.logger.info("\n\tEnding Unit Locations\n")
            for player in self.game.players:
                for unit in player.units:
                    self.game.logger.info("\t\tPlayer %s %s: %s",str(unit.player.player_num),str(unit.unit_num), str(tuple(unit.location)))
                self.game.logger.info("\n")
            self.game.logger.info("END OF TURN %s MOVEMENT PHASE\n",str(self.game.num_turns))

    def move_player_units(self, player, movement_round):
        self.game.current_player = player.player_num
        for unit in player.units:
            if unit.moveable:
                ship_movements = self.movement_data[str(movement_round)][unit.movement - 1]
                for _  in range(ship_movements):
                    if len([enemy for enemy in self.game.players[player.player_num-2].units if enemy.location == unit.location]) == 0:
                        translation = player.strategy.decide_ship_movement(unit.unit_num, self.game.game_state())
                        translation = [translation[0], translation[1]]
                        unit.move(translation, self.game.board_size)
            
    
    def generate_movement_state(self):
        movement_dict = {}
        movement_dict['Phase'] = self.movement_phase
        return movement_dict