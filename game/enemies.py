from game import classes

class Goblin (classes.Enemy):
    max_hp = 100
    reward = 1
    
    move_speed = 0.1
    
    colour = (255,0,0)
    
    def __init__(self, game):
        super(Goblin, self).__init__(game)