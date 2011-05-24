from game import classes, shots

class PinkRune (classes.Rune):
    cost = 10
    shot_range = 10
    fire_speed = 1000
    
    image_name = 'Pink rune'
    shot_type = shots.PinkBullet
    
    def __init__(self, game, position):
        super(PinkRune, self).__init__(game, position)
    
class BlueRune (classes.Rune):
    cost = 10
    shot_range = 10
    fire_speed = 10
    
    image_name = 'Blue rune'
    shot_type = shots.BlueBullet
    
    def __init__(self, game, position):
        super(BlueRune, self).__init__(game, position)

class YellowRune (classes.Rune):
    cost = 10
    shot_range = 10
    fire_speed = 10
    
    image_name = 'Yellow rune'
    shot_type = shots.YellowBullet
    
    def __init__(self, game, position):
        super(YellowRune, self).__init__(game, position)

class GreenRune (classes.Rune):
    cost = 10
    shot_range = 10
    fire_speed = 10
    
    image_name = 'Green rune'
    shot_type = shots.GreenBullet
    
    def __init__(self, game, position):
        super(GreenRune, self).__init__(game, position)