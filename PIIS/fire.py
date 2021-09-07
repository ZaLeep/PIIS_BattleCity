import pygame as pg

class fire(pg.sprite.Sprite):
    def __init__(self, x, y, speed, filename, position):
        pg.sprite.Sprite.__init__(self)
        self.speed = speed
        self.position = position
        if position == 1:
            self.image = pg.image.load(filename).convert_alpha()
        elif position == 2:
            self.image = pg.transform.rotate(pg.image.load(filename).convert_alpha(), 270)
        elif position == 3:
            self.image = pg.transform.rotate(pg.image.load(filename).convert_alpha(), 180)
        else:
            self.image = pg.transform.rotate(pg.image.load(filename).convert_alpha(), 90)
        self.rect = self.image.get_rect(center = (x, y))