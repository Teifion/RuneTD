from game import classes

class Goblin (classes.Enemy):
    max_hp = 100
    reward = 1
    
    def __init__(self, game, color, position):
        super(Goblin, self).__init__(game, color, position)