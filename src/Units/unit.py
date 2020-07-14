import random
class Unit:
    def __init__(self,team, location):
        self.team = team
        self.location = location
    
    def move(self):
        if self.location is not None:
            if self.location[0] == 0 and self.location[1] == 0:
                N = random.choice([1, 3, 5])
            elif self.location[0] == 6 and self.location[1] == 0:
                N = random.choice([2, 3, 5])
            elif self.location[0] == 0 and self.location[1] == 6:
                N = random.choice([1, 4, 5]) 
            elif self.location[0] == 6 and self.location[1] == 6:
                N = random.choice([2, 4, 5])
            elif self.location[0] == 6:
                N = random.choice([2, 3, 4, 5])
            elif self.location[0] == 0:
                N = random.choice([1, 3, 4, 5])
            elif self.location[1] == 6:
                N = random.choice([1, 2, 4, 5])
            elif self.location[1] == 0:
                N = random.choice([1, 2, 3, 5])
            else: 
                N = random.randint(1, 5)
            if N == 1:
                self.location = (self.location[0] + 1, self.location[1])
            elif N == 2:
                self.location = (self.location[0] - 1, self.location[1])
            elif N == 3:
                self.location = (self.location[0], self.location[1] + 1)
            elif N == 4:
                self.location = (self.location[0], self.location[1] - 1)
            elif N == 5:
                self.location = self.location