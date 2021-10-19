import pygame as pg
from fire import fire

class my_tank(pg.sprite.Sprite):
    def __init__(self, x, y, speed, hp, filename, smart = 1):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load(filename).convert_alpha()
        self.rect = self.image.get_rect(center = (x, y))
        self.speed = speed
        self.is_fire = False
        self.ready_aim_fire = False
        self.position = 1
        self.fire = fire(0, 0, 3, "images\\fire.png", self.position)
        self.is_destroyed = False
        self.move = 0
        self.move_times = 0
        self.path = None
        self.hp = hp
        self.smart = smart
        self.algh_time = 0
        self.cd = 0

    def Fire(self, file):
        self.is_fire = True
        if self.position == 1:
            self.fire = fire(self.rect.midtop[0], self.rect.midtop[1] + 6, 2, file, self.position)
        elif self.position == 2:
            self.fire = fire(self.rect.midright[0] - 6, self.rect.midright[1], 2, file, self.position)
        elif self.position == 3:
            self.fire = fire(self.rect.midbottom[0], self.rect.midbottom[1] - 6, 2, file, self.position)
        else:
            self.fire = fire(self.rect.midleft[0] + 6, self.rect.midleft[1], 2, file, self.position)

    def how_many_steps(self):
        if self.move == 1:
            a = (self.rect.bottom + 3) % 16
            if a:
                return a
            return 16
        elif self.move == 2:
            return 16 - (self.rect.right + 3) % 16
        elif self.move == 3:
            return 16 - (self.rect.bottom + 3) % 16
        elif self.move == 4:
            a = (self.rect.right + 3) % 16
            if a:
                return a
        return 16
    
    def can_i_shoot(self, enemy, map):
        if self.position == 1:
            if self.rect.centery > enemy.rect.centery and abs(self.rect.centerx - enemy.rect.centerx) < 16:
                return True
        elif self.position == 2:
            if self.rect.centerx < enemy.rect.centerx and abs(self.rect.centery - enemy.rect.centery) < 16:
                return True
        elif self.position == 3:
            if self.rect.centery < enemy.rect.centery and abs(self.rect.centerx - enemy.rect.centerx) < 16:
                return True
        elif self.position == 4:
            if self.rect.centerx > enemy.rect.centerx and abs(self.rect.centery - enemy.rect.centery) < 16:
                return True
        return False