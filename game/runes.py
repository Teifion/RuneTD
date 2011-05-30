from game import classes, shots

class BasicRune (classes.Rune):
    cost = 10
    shot_range = 10
    fire_speed = 1000
    
    image_name = 'Pink rune'
    shot_type = shots.StandardBullet

class SlowRune (classes.Rune):
    cost = 10
    shot_range = 10
    fire_speed = 1000
    
    image_name = 'Blue rune'
    shot_type = shots.SlowBullet

class SplashRune (classes.Rune):
    cost = 10
    shot_range = 10
    fire_speed = 1000
    
    image_name = 'Yellow rune'
    shot_type = shots.SplashBullet

class PoisonRune (classes.Rune):
    cost = 10
    shot_range = 10
    fire_speed = 1000
    
    image_name = 'Green rune'
    shot_type = shots.PoisonBullet
