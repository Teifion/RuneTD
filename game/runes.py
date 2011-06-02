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
    
    def shoot(self):
        """Overriden to force finding of the least slowed target within range"""
        best_target = (None, 99999999)
        
        for e in self.game.enemies:
            if self.distance(e) <= self.shot_range:
                if e.slowed < best_target[1]:
                    best_target = (e, e.slowed)
        
        self.target = best_target[0]
        
        return super(SlowRune, self).shoot()

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
