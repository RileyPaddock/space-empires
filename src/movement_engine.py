class MovementEngine():

    def generate_movement_state(self,round):
        return {'round': round}

    def move(self, unit, desired_move):
        if self.is_valid(unit, desired_move):
            self.unit.location = desired_move
    
    def is_valid(self,unit,desired_move):
        if desired_move == (unit.location[0],unit.location[1]+1) or desired_move == (unit.location[0],unit.location[1]-1) or desired_move == (unit.location[0]+1,unit.location[1]) or desired_move == (unit.location[0]-1,unit.location[1]):
            return True
        else:
            return False