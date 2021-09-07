import pygame as pg
import pygame.surface
import numpy as np

class map(pg.sprite.Sprite):
    def __init__(self, width, height):
        pg.sprite.Sprite.__init__(self)
        self.digitmap = None
        self.width = width
        self.height = height
        self.image = []
        self.rect = []
        self.menu_image = []
        self.menu_rect = []
        self.enemy_count = []

    def select_map(self, map):
        self.digitmap = np.loadtxt("Map" + str(map) + ".txt", delimiter = ",", dtype = "i")
        self.enemy_count.clear()
        self.enemy_count = [True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True]
        self.image.clear()
        self.rect.clear()
        self.menu_image.clear()
        self.menu_rect.clear()
        for i in range(self.height):
            for j in range(self.width):
                if self.digitmap[i][j] == 0:
                    self.image.append(pg.image.load("images\\none.png").convert_alpha())
                elif self.digitmap[i][j] == 1:
                    self.image.append(pg.image.load("images\\wall.png").convert_alpha())
                elif self.digitmap[i][j] == 2:
                    self.image.append(pg.image.load("images\\brick.png").convert_alpha())
                elif self.digitmap[i][j] == 3:
                    self.image.append(pg.image.load("images\\panel.png").convert_alpha())
                elif self.digitmap[i][j] == 4:
                    self.image.append(pg.image.load("images\\Grass.png").convert_alpha())
                elif self.digitmap[i][j] == 5:
                    self.image.append(pg.image.load("images\\water.png").convert_alpha())
                self.rect.append(self.image[i].get_rect(center = (4 + 8 * j, 4 + 8 * i)))
        
        for i in range(2):
            for j in range(8):
                self.menu_image.append(pg.image.load("images\\menu_tank.png").convert_alpha())
                self.menu_rect.append(self.menu_image[i].get_rect(center = (24 + j * 24, 456 + i * 16)))
    
    def is_path_free(self, x, y, is_bullet = 0):
        j = int(x / 8)
        i = int(y / 8)
        if self.digitmap[i][j] != 0 and self.digitmap[i][j] != 4:
            if is_bullet == 1 and self.digitmap[i][j] == 2:
                self.digitmap[i][j] = 0
                self.image[j + i * (len(self.digitmap[0] + 1))] = pg.image.load("images\\none.png").convert_alpha()
                if self.digitmap[i + 1][j] == 2:
                    self.digitmap[i + 1][j] = 0
                    self.image[j + (i + 1) * (len(self.digitmap[0] + 1))] = pg.image.load("images\\none.png").convert_alpha()
                if self.digitmap[i - 1][j] == 2:
                    self.digitmap[i - 1][j] = 0
                    self.image[j + (i - 1) * (len(self.digitmap[0] + 1))] = pg.image.load("images\\none.png").convert_alpha()
                if self.digitmap[i][j + 1] == 2:
                    self.digitmap[i][j + 1] = 0
                    self.image[j + 1 + i * (len(self.digitmap[0] + 1))] = pg.image.load("images\\none.png").convert_alpha()
                if self.digitmap[i][j - 1] == 2:
                    self.digitmap[i][j - 1] = 0
                    self.image[j - 1 + i * (len(self.digitmap[0] + 1))] = pg.image.load("images\\none.png").convert_alpha()
                if self.digitmap[i - 1][j - 1] == 2:
                    self.digitmap[i - 1][j - 1] = 0
                    self.image[j - 1 + (i - 1) * (len(self.digitmap[0] + 1))] = pg.image.load("images\\none.png").convert_alpha()
                if self.digitmap[i + 1][j - 1] == 2:
                    self.digitmap[i + 1][j - 1] = 0
                    self.image[j - 1 + (i + 1) * (len(self.digitmap[0] + 1))] = pg.image.load("images\\none.png").convert_alpha()
                if self.digitmap[i - 1][j + 1] == 2:
                    self.digitmap[i - 1][j + 1] = 0
                    self.image[j + 1 + (i - 1) * (len(self.digitmap[0] + 1))] = pg.image.load("images\\none.png").convert_alpha()
                if self.digitmap[i + 1][j + 1] == 2:
                    self.digitmap[i + 1][j + 1] = 0
                    self.image[j + 1 + (i + 1) * (len(self.digitmap[0] + 1))] = pg.image.load("images\\none.png").convert_alpha()
            if is_bullet == 1 and self.digitmap[i][j] == 5:
                return True
            return False
        else:
            return True
