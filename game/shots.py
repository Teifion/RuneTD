from game import classes

class PinkBullet (classes.Bullet):
    def __init__(self, game, position, target):
        super(PinkBullet, self).__init__(game, position, target)
        self.image = game.resources['PinkBullet']
