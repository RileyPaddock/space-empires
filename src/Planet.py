class Planet:
    def __init__(self,location):
        self.player = None
        self.location = location
        self.has_a_colony = False
        self.colony = None
        self.shipyards = []

    def reset(self):
        self.player = None
        self.has_a_colony = False
        self.colony = None
        self.shipyards = []