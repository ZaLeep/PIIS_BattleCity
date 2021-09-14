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
                        if random.randint(1, 100) <= 40:
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
            self.menu_rect.append(self.menu_image[j].get_rect(center = (56 + j * 24, 488)))
    
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
        if self.digitmap[i][j] == 2:
            self.digitmap[i][j] = 0
            self.image[j + i * (len(self.digitmap[0] + 1))] = pg.image.load("images\\none.png").convert_alpha()
        if self.digitmap[i + 1][j] == 2:
            self.digitmap[i + 1][j] = 0
            self.image[j + (i + 1) * (len(self.digitmap[0] + 1))] = pg.image.load("images\\none.png").convert_alpha()
        elif pos == 1:
            if self.digitmap[i][j + 2] == 2:
                self.digitmap[i][j + 2] = 0
                self.image[j + 2 + i * (len(self.digitmap[0] + 1))] = pg.image.load("images\\none.png").convert_alpha()
            if self.digitmap[i][j - 2] == 2:
                self.digitmap[i][j - 2] = 0
                self.image[j - 2 + i * (len(self.digitmap[0] + 1))] = pg.image.load("images\\none.png").convert_alpha()
            if self.digitmap[i - 1][j - 2] == 2:
                self.digitmap[i - 1][j - 2] = 0
                self.image[j - 2 + (i - 1) * (len(self.digitmap[0] + 1))] = pg.image.load("images\\none.png").convert_alpha()
            if self.digitmap[i - 1][j + 2] == 2:
                self.digitmap[i - 1][j + 2] = 0
                self.image[j + 2 + (i - 1) * (len(self.digitmap[0] + 1))] = pg.image.load("images\\none.png").convert_alpha()
        if self.digitmap[i - 1][j] == 2:
            self.digitmap[i - 1][j] = 0
            self.image[j + (i - 1) * (len(self.digitmap[0] + 1))] = pg.image.load("images\\none.png").convert_alpha()
        elif pos == 3:
            if self.digitmap[i][j + 2] == 2:
                self.digitmap[i][j + 2] = 0
                self.image[j + 2 + i * (len(self.digitmap[0] + 1))] = pg.image.load("images\\none.png").convert_alpha()
            if self.digitmap[i][j - 2] == 2:
                self.digitmap[i][j - 2] = 0
                self.image[j - 2 + i * (len(self.digitmap[0] + 1))] = pg.image.load("images\\none.png").convert_alpha()
            if self.digitmap[i + 1][j - 2] == 2:
                self.digitmap[i + 1][j - 2] = 0
                self.image[j - 2 + (i + 1) * (len(self.digitmap[0] + 1))] = pg.image.load("images\\none.png").convert_alpha()
            if self.digitmap[i + 1][j + 2] == 2:
                self.digitmap[i + 1][j + 2] = 0
                self.image[j + 2 + (i + 1) * (len(self.digitmap[0] + 1))] = pg.image.load("images\\none.png").convert_alpha()
        if self.digitmap[i][j + 1] == 2:
            self.digitmap[i][j + 1] = 0
            self.image[j + 1 + i * (len(self.digitmap[0] + 1))] = pg.image.load("images\\none.png").convert_alpha()
        elif pos == 4:
            if self.digitmap[i + 2][j] == 2:
                self.digitmap[i + 2][j] = 0
                self.image[j + (i + 2) * (len(self.digitmap[0] + 1))] = pg.image.load("images\\none.png").convert_alpha()
            if self.digitmap[i - 2][j] == 2:
                self.digitmap[i - 2][j] = 0
                self.image[j + (i - 2) * (len(self.digitmap[0] + 1))] = pg.image.load("images\\none.png").convert_alpha()
            if self.digitmap[i + 2][j - 1] == 2:
                self.digitmap[i + 2][j - 1] = 0
                self.image[j - 1 + (i + 2) * (len(self.digitmap[0] + 1))] = pg.image.load("images\\none.png").convert_alpha()
            if self.digitmap[i - 2][j - 1] == 2:
                self.digitmap[i - 2][j - 1] = 0
                self.image[j - 1 + (i - 2) * (len(self.digitmap[0] + 1))] = pg.image.load("images\\none.png").convert_alpha()
        if self.digitmap[i][j - 1] == 2:
            self.digitmap[i][j - 1] = 0
            self.image[j - 1 + i * (len(self.digitmap[0] + 1))] = pg.image.load("images\\none.png").convert_alpha()
        elif pos == 2:
            if self.digitmap[i + 2][j] == 2:
                self.digitmap[i + 2][j] = 0
                self.image[j + (i + 2) * (len(self.digitmap[0] + 1))] = pg.image.load("images\\none.png").convert_alpha()
            if self.digitmap[i - 2][j] == 2:
                self.digitmap[i - 2][j] = 0
                self.image[j + (i - 2) * (len(self.digitmap[0] + 1))] = pg.image.load("images\\none.png").convert_alpha()
            if self.digitmap[i + 2][j + 1] == 2:
                self.digitmap[i + 2][j + 1] = 0
                self.image[j + 1 + (i + 2) * (len(self.digitmap[0] + 1))] = pg.image.load("images\\none.png").convert_alpha()
            if self.digitmap[i - 2][j + 1] == 2:
                self.digitmap[i - 2][j + 1] = 0
                self.image[j + 1 + (i - 2) * (len(self.digitmap[0] + 1))] = pg.image.load("images\\none.png").convert_alpha()

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

    def bfs(self, start, finish):
        j_s = int(start[0] / 16)
        i_s = int(start[1] / 16)
        j_f = int(finish[0] / 16)
        i_f = int(finish[1] / 16)
        q = []
        q.append([(i_s, j_s), (-1, -1)])
        v = []
        visited = []
        visited.append(q[0])
        prev = []
        count = 0
        f = True
        while q and f:
            curr = q[0][0]
            curr_prev = q[0][1]
            q.pop(0)
            v.append(curr)
            prev.append(curr_prev)
            if v[len(v) - 1][0] == i_f and v[len(v) - 1][1] == j_f:
                f = False
            if f and visited.count((curr[0] + 1, curr[1])) == 0 and self.check((curr[0] + 1, curr[1])):
                q.append([(curr[0] + 1, curr[1]), curr])
                visited.append((curr[0] + 1, curr[1]))
            if f and visited.count((curr[0], curr[1] + 1)) == 0 and self.check((curr[0], curr[1] + 1)):
                q.append([(curr[0], curr[1] + 1), curr])
                visited.append((curr[0], curr[1] + 1))
            if f and visited.count((curr[0] - 1, curr[1])) == 0 and self.check((curr[0] - 1, curr[1])):
                q.append([(curr[0] - 1, curr[1]), curr])
                visited.append((curr[0] - 1, curr[1]))
            if f and visited.count((curr[0], curr[1] - 1)) == 0 and self.check((curr[0], curr[1] - 1)):
                q.append([(curr[0], curr[1] - 1), curr])
                visited.append((curr[0], curr[1] - 1))
        path = []
        path.append((i_f, j_f))
        p = (prev[len(v) - 1][0], prev[len(v) - 1][1])
        f = True
        while f:
            i = v.index(p)
            path.append(p)
            p = (prev[i][0], prev[i][1])
            if p == (-1, -1):
                f = False
        if len(q) == 0:
            path.clear()
        return path

    def dfs(self, start, finish):
        j_s = int(start[0] / 16)
        i_s = int(start[1] / 16)
        j_f = int(finish[0] / 16)
        i_f = int(finish[1] / 16)
        path = []
        curr_path = []
        path_length = -1
        f = [True]
        self.dfs_tick((i_s, j_s), (i_f, j_f), path, f)
        if path[len(path) - 1] != (i_f, j_f):
            path.clear()
        return path

    def dfs_tick(self, curr, finish, c_p, f):
        c_p.append(curr)
        if curr == finish:
            f = False
            return
        else:
            if c_p.count((curr[0] + 1, curr[1])) == 0 and self.check((curr[0] + 1, curr[1])):
                self.dfs_tick((curr[0] + 1, curr[1]), finish, c_p, f)
                if c_p[len(c_p) - 1] == finish:
                    return
            if c_p.count((curr[0], curr[1] + 1)) == 0 and self.check((curr[0], curr[1] + 1)):
                self.dfs_tick((curr[0], curr[1] + 1), finish, c_p, f)
                if c_p[len(c_p) - 1] == finish:
                    return
            if c_p.count((curr[0] - 1, curr[1])) == 0 and self.check((curr[0] - 1, curr[1])):
                self.dfs_tick((curr[0] - 1, curr[1]), finish, c_p, f)
                if c_p[len(c_p) - 1] == finish:
                    return
            if c_p.count((curr[0], curr[1] - 1)) == 0 and self.check((curr[0], curr[1] - 1)):
                self.dfs_tick((curr[0], curr[1] - 1), finish, c_p, f)
                if c_p[len(c_p) - 1] == finish:
                    return

    def ucs(self, start, finish):
        j_s = int(start[0] / 16)
        i_s = int(start[1] / 16)
        j_f = int(finish[0] / 16)
        i_f = int(finish[1] / 16)
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
        return True

    def update_smallmap(self):
        for i in range(len(self.small_digitmap)):
            for j in range(len(self.small_digitmap[i])):
                if self.small_digitmap[i][j] == 2:
                    if self.digitmap[i*2][j*2] == 0 and self.digitmap[i*2 + 1][j*2] == 0 and self.digitmap[i*2][j*2 + 1] == 0 and self.digitmap[i*2 + 1][j*2 + 1] == 0:
                        self.small_digitmap[i][j] = 0