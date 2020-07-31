import random
class Unit:
    def __init__(self,team, location):
        self.team = team
        self.location = location

    def move(self,direction):
        if direction == 'up':
            self.location = (self.location[0],self.location[1]+1)
        elif direction == 'down':
            self.location = (self.location[0],self.location[1]-1)
        elif direction == 'right':
            self.location = (self.location[0]+1,self.location[1])
        elif direction == 'left':
            self.location = (self.location[0]-1,self.location[1])
        else:
            print("\n   You done messed up movement!")