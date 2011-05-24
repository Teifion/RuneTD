from game import classes

class PinkBullet (classes.Bullet):
    move_speed = 0.5
    damage = 1
    
    def __init__(self, game, position, target):
        super(PinkBullet, self).__init__(game, position, target)
        self.image = game.resources['Pink bullet']

class BlueBullet (classes.Bullet):
    move_speed = 0.5
    damage = 2
    
    def __init__(self, game, position, target):
        super(BlueBullet, self).__init__(game, position, target)
        self.image = game.resources['Blue bullet']

class YellowBullet (classes.Bullet):
    move_speed = 0.5
    damage = 3
    
    def __init__(self, game, position, target):
        super(YellowBullet, self).__init__(game, position, target)
        self.image = game.resources['Yellow bullet']

class GreenBullet (classes.Bullet):
    move_speed = 0.5
    damage = 4
    
    def __init__(self, game, position, target):
        super(GreenBullet, self).__init__(game, position, target)
        self.image = game.resources['Green bullet']
