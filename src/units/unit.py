import random
class Unit:
    def __init__(self,team, location, unit_num, age = 0):
        self.team = team
        self.location = location
        self.unit_num = unit_num
        self.age = age

    def unit_state(self):
        unit_state = {}
        unit_state['location'] = self.location
        unit_state['type'] = self.unit_type
        unit_state['technology'] = {attr:value for attr, value in self.__dict__.items() if 'tech' in attr}
        unit_state['unit_num'] = self.unit_num
        unit_state['team']  =self.team
        return unit_state

