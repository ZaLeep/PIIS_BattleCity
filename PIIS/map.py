import pygame as pg
import pygame.surface
import numpy as np
import random
import trans

class map(pg.sprite.Sprite):
    def __init__(self, width, height):
        pg.sprite.Sprite.__init__(self)
        self.digitmap = None
        self.small_digitmap = None
        self.width = width
        self.height = height
        self.image = []
        self.rect = []
        self.menu_image = []
        self.menu_rect = []
        self.enemy_count = []
        self.hp = []
        self.hp_rect = []

    def select_map(self, map):
        if map < 4:
            self.digitmap = np.loadtxt("Map" + str(map) + ".txt", delimiter = ",", dtype = "i")
            self.small_digitmap = np.loadtxt("digitmap" + str(map) + ".txt", delimiter = ",", dtype = "i")
        else:
            self.digitmap = []
            self.small_digitmap = []
            first = np.loadtxt("digitmap" + str(map) + ".txt", delimiter = ",", dtype = "i")
            for i in range(len(first)):
                for j in range(len(first[i])):
                    if first[i][j] == 7:
                        if random.randint(1, 100) <= 30:
                            first[i][j] = 2
                        else:
                            first[i][j] = 0
            trans.trans(4, first)
            self.small_digitmap = np.loadtxt("Map4.txt", delimiter = ",", dtype = "i")
            trans.trans(5, self.small_digitmap)
            self.digitmap = np.loadtxt("Map5.txt", delimiter = ",", dtype = "i")

        self.enemy_count.clear()
        self.enemy_count = [True, True, True, True, True, True, True, True, True, True]
        self.image.clear( )
        self.rect.clear()
        self.menu_image.clear()
        self.menu_rect.clear()
        self.hp.clear()
        self.hp_rect.clear()
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
        
        for j in range(10):
            self.menu_image.append(pg.image.load("images\\menu_tank.png").convert_alpha())
            self.menu_rect.append(self.menu_image[j].get_rect(center = (9 + j * 24, 488)))
        for j in range(3):
            self.hp.append(pg.image.load("images\\hp.png").convert_alpha())
            self.hp_rect.append(self.menu_image[j].get_rect(center = (423 + 24 * j, 488)))

    def is_path_free(self, x, y, is_bullet = 0, pos = 1):
        j = int(x / 8)
        i = int(y / 8)
        if self.digitmap[i][j] != 0 and self.digitmap[i][j] != 4:
            if is_bullet == 1:
                self.boom(i, j, pos)
                self.update_smallmap()
            if is_bullet == 1 and self.digitmap[i][j] == 5:
                return True
            return False
        else:
            return True

    def boom(self, i, j, pos):
        i = i // 2 * 2
        j = j // 2 * 2
        for a in range(4):
            for b in range(4): 
                if self.digitmap[i + a][j + b] == 2:
                    self.digitmap[i + a][j + b] = 0
                    self.image[j + b + (i + a) * (len(self.digitmap[0] + 1))] = pg.image.load("images\\none.png").convert_alpha()

    def ucs(self, start, finish):
        j_s = int(start[0] / 32)
        i_s = int(start[1] / 32)
        j_f = int(finish[0] / 32)
        i_f = int(finish[1] / 32)
        if (start[0] - 13) // 32 != j_s:
            j_s = j_s * 2
        elif (start[0] + 13) // 32 != j_s:
            j_s = j_s * 2 + 2
        else:
            j_s = j_s * 2 + 1

        if (start[1] - 13) // 32 != i_s:
            i_s = i_s * 2
        elif (start[1] + 13) // 32 != i_s:
            i_s = i_s * 2 + 2
        else:
            i_s = i_s * 2 + 1

        if (finish[0] - 13) // 32 != j_f:
            j_f = j_f * 2
        elif (finish[0] + 13) // 32 != j_f:
            j_f = j_f * 2 + 2
        else:
            j_f = j_f * 2 + 1

        if (finish[1] - 13) // 32 != i_f:
            i_f = i_f * 2
        elif (finish[1] + 13) // 32 != i_f:
            i_f = i_f * 2 + 2
        else:
            i_f = i_f * 2 + 1
            
        path_matrix = []
        for i in range(len(self.small_digitmap)):
            line = []
            for j in range(len(self.small_digitmap[i])):
                line.append((-1, -1))
            path_matrix.append(line)
        q = [[(i_s, j_s), (-2, -2)]]
        f = True
        while q and f:
            curr = q[0][0]
            prev = q[0][1]
            q.pop(0)
            path_matrix[curr[0]][curr[1]] = prev
            if curr[0] == i_f and curr[1] == j_f:
                f = False
            if f and path_matrix[curr[0] + 1][curr[1]] == (-1, -1) and self.check((curr[0] + 1, curr[1])):
                path_matrix[curr[0] + 1][curr[1]] = (-2, -2)
                q.append([(curr[0] + 1, curr[1]), curr])
            if f and path_matrix[curr[0]][curr[1] + 1] == (-1, -1) and self.check((curr[0], curr[1] + 1)):
                path_matrix[curr[0]][curr[1] + 1] = (-2, -2)
                q.append([(curr[0], curr[1] + 1), curr])
            if f and path_matrix[curr[0] - 1][curr[1]] == (-1, -1) and self.check((curr[0] - 1, curr[1])):
                path_matrix[curr[0] - 1][curr[1]] = (-2, -2)
                q.append([(curr[0] - 1, curr[1]), curr])
            if f and path_matrix[curr[0]][curr[1] - 1] == (-1, -1) and self.check((curr[0], curr[1] - 1)):
                path_matrix[curr[0]][curr[1] - 1] = (-2, -2)
                q.append([(curr[0], curr[1] - 1), curr])
        path = []
        f = True
        curr = (i_f, j_f)
        if curr == (-1, -1):
            return path
        while q and f:
            path.append(path_matrix[curr[0]][curr[1]])
            if path_matrix[curr[0]][curr[1]] == (i_s, j_s):
                f = False
            else:
                curr = path_matrix[curr[0]][curr[1]]
        return path

    def Fmin(self, q):
        i = 0
        min = q[i][2][0] + q[i][2][1]
        for j in range(len(q) - 1):
            if min > q[j + 1][2][0] + q[j + 1][2][1]:
                i = j
                min = q[j + 1][2][0] + q[j + 1][2][1]
        return i

    def RandBlock(self):
        f = True
        i = -1
        j = -1
        while f:
            i = random.randint(1, 13)
            j = random.randint(1, 13)
            if self.small_digitmap[i * 2][j * 2] % 4 == 0 and self.small_digitmap[i * 2 + 1][j * 2] % 4 == 0 and self.small_digitmap[i * 2][j * 2 + 1] % 4 == 0 and self.small_digitmap[i * 2 + 1][j * 2 + 1] % 4 == 0:
                f = False
        return (i * 2 + 1, j * 2 + 1)

    def A_star(self, start, finish):
        j_s = int(start[0] / 32)
        i_s = int(start[1] / 32)
        j_f = int(finish[0] / 32)
        i_f = int(finish[1] / 32)
        if (start[0] - 13) // 32 != j_s:
            j_s = j_s * 2
        elif (start[0] + 13) // 32 != j_s:
            j_s = j_s * 2 + 2
        else:
            j_s = j_s * 2 + 1

        if (start[1] - 13) // 32 != i_s:
            i_s = i_s * 2
        elif (start[1] + 13) // 32 != i_s:
            i_s = i_s * 2 + 2
        else:
            i_s = i_s * 2 + 1

        if (finish[0] - 13) // 32 != j_f:
            j_f = j_f * 2
        elif (finish[0] + 13) // 32 != j_f:
            j_f = j_f * 2 + 2
        else:
            j_f = j_f * 2 + 1

        if (finish[1] - 13) // 32 != i_f:
            i_f = i_f * 2
        elif (finish[1] + 13) // 32 != i_f:
            i_f = i_f * 2 + 2
        else:
            i_f = i_f * 2 + 1
            
        path_matrix = []
        for i in range(len(self.small_digitmap)):
            line = []
            for j in range(len(self.small_digitmap[i])):
                line.append((-1, -1))
            path_matrix.append(line)
        q = [[(i_s, j_s), (-2, -2), (0, 3228)]]
        f = True
        while q and f:
            i = self.Fmin(q)
            curr = q[i][0]
            prev = q[i][1]
            evr = q[i][2]
            q.pop(i)
            path_matrix[curr[0]][curr[1]] = prev
            if curr[0] == i_f and curr[1] == j_f:
                f = False
            if f and path_matrix[curr[0] + 1][curr[1]] == (-1, -1) and self.check((curr[0] + 1, curr[1])):
                path_matrix[curr[0] + 1][curr[1]] = (-2, -2)
                q.append([(curr[0] + 1, curr[1]), curr, (evr[0] + 1, self.distance((curr[0] + 1, curr[1]), (i_f, j_f)))])
            if f and path_matrix[curr[0]][curr[1] + 1] == (-1, -1) and self.check((curr[0], curr[1] + 1)):
                path_matrix[curr[0]][curr[1] + 1] = (-2, -2)
                q.append([(curr[0], curr[1] + 1), curr, (evr[0] + 1, self.distance((curr[0], curr[1] + 1), (i_f, j_f)))])
            if f and path_matrix[curr[0] - 1][curr[1]] == (-1, -1) and self.check((curr[0] - 1, curr[1])):
                path_matrix[curr[0] - 1][curr[1]] = (-2, -2)
                q.append([(curr[0] - 1, curr[1]), curr, (evr[0] - 1, self.distance((curr[0] + 1, curr[1]), (i_f, j_f)))])
            if f and path_matrix[curr[0]][curr[1] - 1] == (-1, -1) and self.check((curr[0], curr[1] - 1)):
                path_matrix[curr[0]][curr[1] - 1] = (-2, -2)
                q.append([(curr[0], curr[1] - 1), curr, (evr[0] + 1, self.distance((curr[0], curr[1] - 1), (i_f, j_f)))])
        path = []
        f = True
        curr = (i_f, j_f)
        if curr == (-1, -1):
            return path
        path.append(curr)
        while q and f:
            path.append(path_matrix[curr[0]][curr[1]])
            if path_matrix[curr[0]][curr[1]] == (i_s, j_s):
                f = False
            else:
                curr = path_matrix[curr[0]][curr[1]]
        return path

    def copy(self, l1, l2):
        l1.clear()
        for i in l2:
            l1.append(i)

    def distance(self, point1, point2):
        return ((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2) ** 0.5

    def check(self, point):
        if self.small_digitmap[point[0]][point[1]] % 4 != 0:
            return False
        if self.small_digitmap[point[0] - 1][point[1]] % 4 != 0:
            return False
        if self.small_digitmap[point[0]][point[1] - 1] % 4 != 0:
            return False
        if self.small_digitmap[point[0] - 1][point[1] - 1] % 4 != 0:
            return False
        return True

    def bottomright(self, point):
        j = point[0] // 32
        i = point[1] // 32
        if (point[0] - 13) // 32 != j:
            j = j * 2
        elif (point[0] + 13) // 32 != j:
            j = j * 2 + 2
        else:
            j = j * 2 + 1

        if (point[1] - 13) // 32 != i:
            i = i * 2
        elif (point[1] + 13) // 32 != i:
            i = i * 2 + 2
        else:
            i = i * 2 + 1
        return (i, j)
    
    def update_smallmap(self):
        for i in range(len(self.small_digitmap)):
            for j in range(len(self.small_digitmap[i])):
                if self.small_digitmap[i][j] == 2:
                    if self.digitmap[i*2][j*2] == 0 and self.digitmap[i*2 + 1][j*2] == 0 and self.digitmap[i*2][j*2 + 1] == 0 and self.digitmap[i*2 + 1][j*2 + 1] == 0:
                        self.small_digitmap[i][j] = 0