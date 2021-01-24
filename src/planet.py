class Planet:
    def __init__(self, location, colonized = False, colony = None):
        self.location = location
        self.colonized = colonized
        self.unit_type = "Planet"
        self.colony = colony

    def colonize(self, colony):
        self.colonized = True
        self.colony = colony

    def destroy(self):
        self.colonized = False
        self.colony = None