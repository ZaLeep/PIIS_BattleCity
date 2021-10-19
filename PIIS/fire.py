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

    def where_i_fly(self, target, map):
        if self.position == 1:
            if self.rect.center[1] > target.rect.center[1] and self.rect.center[0] - 4 >= target.rect.left and self.rect.center[0] + 4 <= target.rect.right:
                flag = True
                curr = self.rect.top
                while curr > target.rect.bottom and flag:
                    block = map.digitmap[curr // 8][self.rect.center[0] // 8]
                    if block == 1 or block == 2:
                        flag = False
                    curr -= 8
                if flag:
                    return (map.distance(self.rect.midtop, target.rect.midbottom) // 16 + 1)
        elif self.position == 2:
            if self.rect.center[0] < target.rect.center[0] and self.rect.center[1] - 4 >= target.rect.top and self.rect.center[1] + 4 <= target.rect.bottom:
                flag = True
                curr = self.rect.right
                while curr < target.rect.left and flag:
                    block = map.digitmap[self.rect.center[1] // 8][curr // 8]
                    if block == 1 or block == 2:
                        flag = False
                    curr += 8
                if flag:
                    return (map.distance(self.rect.midright, target.rect.midleft) // 16 + 1)
        elif self.position == 3:
            if self.rect.center[1] < target.rect.center[1] and self.rect.center[0] - 4 >= target.rect.left and self.rect.center[0] + 4 <= target.rect.right:
                flag = True
                curr = self.rect.bottom
                while curr < target.rect.top and flag:
                    block = map.digitmap[curr // 8][self.rect.center[0] // 8]
                    if block == 1 or block == 2:
                        flag = False
                    curr += 8
                if flag:
                    return (map.distance(self.rect.midbottom, target.rect.midtop) // 16 + 1)
        elif self.position == 4:
            if self.rect.center[0] > target.rect.center[0] and self.rect.center[1] - 4 >= target.rect.top and self.rect.center[1] + 4 <= target.rect.bottom:
                flag = True
                curr = self.rect.left
                while curr > target.rect.right and flag:
                    block = map.digitmap[self.rect.center[1] // 8][curr // 8]
                    if block == 1 or block == 2:
                        flag = False
                    curr -= 8
                if flag:
                    (map.distance(self.rect.midleft, target.rect.midright) // 16 + 1)
        return 100000