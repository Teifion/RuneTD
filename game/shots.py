from game import classes

class StandardBullet (classes.Bullet):
    move_speed = 0.5
    damage = 2
    
    def __init__(self, game, position, target):
        super(StandardBullet, self).__init__(game, position, target)
        self.image = game.resources['Pink bullet']
    
    def apply_effects(self):
        pass

class SlowBullet (classes.Bullet):
    move_speed = 0.5
    damage = 1
    
    def __init__(self, game, position, target):
        super(SlowBullet, self).__init__(game, position, target)
        self.image = game.resources['Blue bullet']
    
    def apply_effects(self):
        self.sprite_target.slowed = 50

class SplashBullet (classes.Bullet):
    move_speed = 0.5
    damage = 1
    splash_range = 10
    
    def __init__(self, game, position, target):
        super(SplashBullet, self).__init__(game, position, target)
        self.image = game.resources['Yellow bullet']
        
        # Not seeking, it'll hit and explode
        self.sprite_target = None
    
    def apply_effects(self):
        # Find all enemies withing splash reach
        within_reach = []
        
        for e in self.game.enemies:
            if self.distance(e.position) <= self.splash_range:
                within_reach.append(e)
        
        for enemy in within_reach[:]:
            enemy.hp -= self.damage
            if enemy.hp <= 0:
                enemy.kill()


class PoisonBullet (classes.Bullet):
    move_speed = 0.5
    damage = 0
    
    def __init__(self, game, position, target):
        super(PoisonBullet, self).__init__(game, position, target)
        self.image = game.resources['Green bullet']
    
    def apply_effects(self):
        self.sprite_target.poisoned += 100
    
