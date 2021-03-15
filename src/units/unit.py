class Unit:
    moveable = True
    can_atk = True
    instant_ko = False

    def __init__(self, location, unit_num, player, technologies, game, turn_created):
        self.location = location
        self.unit_num = unit_num
        self.player = player
        self.technologies = technologies
        self.alive = True
        self.game = game
        self.maintenance = 0
        self.turn_created = turn_created

    def move(self, direction, grid_size):
        x = self.location[0] + direction[0]
        y = self.location[1] + direction[1]
        if x < 0 or x > grid_size[0] - 1:
            return
        if y < 0 or y > grid_size[1] - 1:
            return
        if self.player.game.logging:
            self.player.game.logger.info("\t\tPlayer %s %s: %s -> %s",str(self.player.player_num), str(self.unit_num),str(tuple(self.location)), str((x,y)))
        self.location = [x, y]
        

    def hit(self):
        if self.armor > 1:
            self.armor -= 1
        else:
            self.destroy()

    def destroy(self):
        self.alive = False
        if self in self.player.units:
            self.player.units.remove(self)
