from game import classes

class PinkBullet (classes.Bullet):
    damage = 1
    
    def __init__(self, game, position, target):
        super(PinkBullet, self).__init__(game, position, target)
        self.image = game.resources['PinkBullet']
