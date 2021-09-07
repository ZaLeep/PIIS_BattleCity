import pygame as pg
from fire import fire

class my_tank(pg.sprite.Sprite):
    def __init__(self, x, y, speed, filename):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load(filename).convert_alpha()
        self.rect = self.image.get_rect(center = (x, y))
        self.speed = speed
        self.is_fire = False
        self.position = 1
        self.fire = fire(0, 0, 2, "images\\fire.png", self.position)
        self.is_destroyed = False

    def Fire(self):
        self.is_fire = True
        if self.position == 1:
            self.fire = fire(self.rect.midtop[0], self.rect.midtop[1] + 6, 2, "images\\fire.png", self.position)
        elif self.position == 2:
            self.fire = fire(self.rect.midright[0] - 6, self.rect.midright[1], 2, "images\\fire.png", self.position)
        elif self.position == 3:
            self.fire = fire(self.rect.midbottom[0], self.rect.midbottom[1] - 6, 2, "images\\fire.png", self.position)
        else:
            self.fire = fire(self.rect.midleft[0] + 6, self.rect.midleft[1], 2, "images\\fire.png", self.position)