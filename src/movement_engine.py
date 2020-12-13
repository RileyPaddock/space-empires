class MovementEngine():

    def generate_movement_state(self,round):
        return {'round': round}

    def move(self, unit, desired_move):
        if self.is_valid(unit, desired_move):
            self.unit.location = desired_move
    
    