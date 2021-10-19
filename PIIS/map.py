import pygame as pg
import pygame.surface
import numpy as np
import random
from my_tank import my_tank
from fire import fire
import trans
import copy

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

    def check_for_expec(self, point, move):
        j = int(point.rect.center[0] / 32)
        i = int(point.rect.center[1] / 32)
        if (point.rect.center[0] - 13) // 32 != j:
            j = j * 2
        elif (point.rect.center[0] + 13) // 32 != j:
            j = j * 2 + 2
        else:
            j = j * 2 + 1
        if (point.rect.center[1] - 13) // 32 != i:
            i = i * 2
        elif (point.rect.center[1] + 13) // 32 != i:
            i = i * 2 + 2
        else:
            i = i * 2 + 1
        if move == 1:
            return(self.check([i - 1, j]))
        elif move == 2:
            return(self.check([i, j + 1]))
        elif move == 3:
            return(self.check([i + 1, j]))
        elif move == 4:
            return(self.check([i, j - 1]))


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

    def mini_max(self, who, alpha_beta, map, me, enemy, limit, move = 0, deep = 0):
        curr_deep = deep + 1
        result = [0, -123456]
        if curr_deep <= limit:
            if who:
                j = int(me.rect.center[0] / 32)
                i = int(me.rect.center[1] / 32)
                if (me.rect.center[0] - 13) // 32 != j:
                    j = j * 2
                elif (me.rect.center[0] + 13) // 32 != j:
                    j = j * 2 + 2
                else:
                    j = j * 2 + 1
                if (me.rect.center[1] - 13) // 32 != i:
                    i = i * 2
                elif (me.rect.center[1] + 13) // 32 != i:
                    i = i * 2 + 2
                else:
                    i = i * 2 + 1

                curr_var = [0, -123456]
                if map.check((i - 1, j)):
                    curr_var = self.mini_max(0, alpha_beta, map, me, enemy, limit, move = 1, deep = curr_deep)
                    if curr_var[1] >= alpha_beta[1]:
                        return result
                    elif curr_var[1] > result[1]:
                        result[0] = curr_var[0]
                        result[1] = curr_var[1]
                if map.check((i, j + 1)):
                    curr_var = self.mini_max(0, alpha_beta, map, me, enemy, limit, move = 2, deep = curr_deep)
                    if curr_var[1] >= alpha_beta[1]:
                        return result
                    elif curr_var[1] > result[1]:
                        result[0] = curr_var[0]
                        result[1] = curr_var[1]
                if map.check((i + 1, j)):
                    curr_var = self.mini_max(0, alpha_beta, map, me, enemy, limit, move = 3, deep = curr_deep)
                    if curr_var[1] >= alpha_beta[1]:
                        return result
                    elif curr_var[1] > result[1]:
                        result[0] = curr_var[0]
                        result[1] = curr_var[1]
                if map.check((i, j - 1)):
                    curr_var = self.mini_max(0, alpha_beta, map, me, enemy, limit, move = 4, deep = curr_deep)
                    if curr_var[1] >= alpha_beta[1]:
                        return result
                    elif curr_var[1] > result[1]:
                        result[0] = curr_var[0]
                        result[1] = curr_var[1]
                if not me.is_fire:
                    curr_var = self.mini_max(0, alpha_beta, map, me, enemy, limit, move = 5, deep = curr_deep)
                    if curr_var[1] >= alpha_beta[1]:
                        return result
                    elif curr_var[1] > result[1]:
                        result[0] = curr_var[0]
                        result[1] = curr_var[1]
                    curr_var = self.mini_max(0, alpha_beta, map, me, enemy, limit, move = 6, deep = curr_deep)
                    if curr_var[1] >= alpha_beta[1]:
                        return result
                    elif curr_var[1] > result[1]:
                        result[0] = curr_var[0]
                        result[1] = curr_var[1]
                    curr_var = self.mini_max(0, alpha_beta, map, me, enemy, limit, move = 7, deep = curr_deep)
                    if curr_var[1] >= alpha_beta[1]:
                        return result
                    elif curr_var[1] > result[1]:
                        result[0] = curr_var[0]
                        result[1] = curr_var[1]
                    curr_var = self.mini_max(0, alpha_beta, map, me, enemy, limit, move = 8, deep = curr_deep)
                    if curr_var[1] >= alpha_beta[1]:
                        return result
                    elif curr_var[1] > result[1]:
                        result[0] = curr_var[0]
                        result[1] = curr_var[1]
                return result
            else:
                my_map = map.copy()
                tank1 = my_tank(me.rect.center[0], me.rect.center[1], me.speed, me.hp, "images\my_tank.png")
                tank1.position = me.position
                tank1.is_fire = me.is_fire
                tank1.fire = fire(me.fire.rect.center[0], me.fire.rect.center[1], 2, "images\\fire.png", me.fire.position)
                enemies = []
                for i in range(len(enemy)):
                    enemies.append(my_tank(enemy[i].rect.center[0], enemy[i].rect.center[1], enemy[i].speed, enemy[i].hp, "images\enemy_tank.png"))
                    enemies[i].position = enemy[i].position
                    enemies[i].is_destroyed = enemy[i].is_destroyed
                if move < 5:
                    tank1.move = move
                    tank1.move_times = 16
                else:
                    tank1.ready_aim_fire = True
                    tank1.move = move - 4
                    tank1.move_times = 16

                for i in range(16):
                    if tank1.move == 4:
                        tank1.image = pg.transform.rotate(pg.image.load("images\\my_tank.png").convert_alpha(), 90)
                        tank1.position = 4
                        f = True
                        for e in enemies:
                            if not e.is_destroyed and tank1.rect.left - 1 == e.rect.right and ((tank1.rect.top >= e.rect.top and tank1.rect.top <= e.rect.bottom) or (tank1.rect.bottom <= e.rect.bottom and tank1.rect.bottom >= e.rect.top)):
                                f = False
                        if f and my_map.is_path_free(tank1.rect.left - 1, tank1.rect.topleft[1]) and my_map.is_path_free(tank1.rect.left - 1, tank1.rect.bottomleft[1]) and my_map.is_path_free(tank1.rect.left - 1, tank1.rect.midleft[1]) and my_map.is_path_free(tank1.rect.left - 1, tank1.rect.midleft[1] - 7) and my_map.is_path_free(tank1.rect.left - 1, tank1.rect.midleft[1] + 7):
                            tank1.rect.x -= tank1.speed
                            tank1.move_times -= 1
                        if not tank1.is_fire and tank1.ready_aim_fire:
                            tank1.Fire("images\\fire.png")
                    elif tank1.move == 1:
                        tank1.image = pg.transform.rotate(pg.image.load("images\my_tank.png").convert_alpha(), 0)
                        tank1.position = 1
                        f = True
                        for e in enemies:
                            if not e.is_destroyed and tank1.rect.top - 1 == e.rect.bottom and ((tank1.rect.left >= e.rect.left and tank1.rect.left <= e.rect.right) or (tank1.rect.right <= e.rect.right and tank1.rect.right >= e.rect.left)):
                                f = False
                        if f and my_map.is_path_free(tank1.rect.topleft[0], tank1.rect.topleft[1] - 1) and my_map.is_path_free(tank1.rect.topright[0], tank1.rect.topright[1] - 1) and my_map.is_path_free(tank1.rect.midtop[0], tank1.rect.midtop[1] - 1) and my_map.is_path_free(tank1.rect.midtop[0] + 7, tank1.rect.midtop[1] - 1) and my_map.is_path_free(tank1.rect.midtop[0] - 7, tank1.rect.midtop[1] - 1):
                            tank1.rect.y -= tank1.speed
                            tank1.move_times -= 1
                        if not tank1.is_fire and tank1.ready_aim_fire:
                            tank1.Fire("images\\fire.png")
                    elif tank1.move == 2:
                        tank1.image = pg.transform.rotate(pg.image.load("images\my_tank.png").convert_alpha(), 270)
                        tank1.position = 2
                        f = True
                        for e in enemies:
                            if not e.is_destroyed and tank1.rect.right + 1 == e.rect.left and ((tank1.rect.top >= e.rect.top and tank1.rect.top <= e.rect.bottom) or (tank1.rect.bottom <= e.rect.bottom and tank1.rect.bottom >= e.rect.top)):
                                f = False
                        if f and my_map.is_path_free(tank1.rect.topright[0] + 1, tank1.rect.topright[1]) and my_map.is_path_free(tank1.rect.bottomright[0] + 1, tank1.rect.bottomright[1]) and my_map.is_path_free(tank1.rect.midright[0] + 1, tank1.rect.midright[1]) and my_map.is_path_free(tank1.rect.midright[0] + 1, tank1.rect.midright[1] + 7) and my_map.is_path_free(tank1.rect.midright[0] + 1, tank1.rect.midright[1] - 7):
                            tank1.rect.x += tank1.speed
                            tank1.move_times -= 1
                        if not tank1.is_fire and tank1.ready_aim_fire:
                            tank1.Fire("images\\fire.png")
                    elif tank1.move == 3:
                        tank1.image = pg.transform.rotate(pg.image.load("images\my_tank.png").convert_alpha(), 180)
                        tank1.position = 3
                        f = True
                        for e in enemies:
                            if not e.is_destroyed and tank1.rect.bottom + 1 == e.rect.top and ((tank1.rect.left >= e.rect.left and tank1.rect.left <= e.rect.right) or (tank1.rect.right <= e.rect.right and tank1.rect.right >= e.rect.left)):
                                f = False
                        if f and my_map.is_path_free(tank1.rect.bottomleft[0], tank1.rect.bottomleft[1] + 1) and my_map.is_path_free(tank1.rect.bottomright[0], tank1.rect.bottomright[1] + 1) and my_map.is_path_free(tank1.rect.midbottom[0], tank1.rect.midbottom[1] + 1) and my_map.is_path_free(tank1.rect.midbottom[0] - 7, tank1.rect.midbottom[1] + 1) and my_map.is_path_free(tank1.rect.midbottom[0] + 7, tank1.rect.midbottom[1] + 1):
                            tank1.rect.y += tank1.speed
                            tank1.move_times -= 1
                        if not tank1.is_fire and tank1.ready_aim_fire:
                            tank1.Fire("images\\fire.png")
                    for i in range(len(enemies)):
                        if not enemies[i].is_destroyed and enemies[i].move_times == 0:
                            enemies[i].path = my_map.A_star(enemies[i].rect.center, tank1.rect.center)
                            if enemies[i].path:
                                enemies[i].move_times = 16
                                point1 = enemies[i].path[len(enemies[i].path) - 1]
                                point2 = enemies[i].path[len(enemies[i].path) - 2]
                                if point2[0] < point1[0]:
                                    enemies[i].move = 1
                                elif point2[0] > point1[0]:
                                    enemies[i].move = 3
                                elif point2[1] > point1[1]:
                                    enemies[i].move = 2
                                else:
                                    enemies[i].move = 4
                    for q in enemies:
                        if not q.is_destroyed:
                            if q.move == 4:
                                q.image = pg.transform.rotate(pg.image.load("images\enemy_tank.png").convert_alpha(), 90)
                                q.position = 4
                                f = True
                                if not tank1.is_destroyed and q.rect.left - 1 == tank1.rect.right and ((q.rect.top >= tank1.rect.top and q.rect.top <= tank1.rect.bottom) or (q.rect.bottom <= tank1.rect.bottom and q.rect.bottom >= tank1.rect.top)):
                                    f = False
                                for e in enemies:
                                    if e != q:
                                        if not e.is_destroyed and q.rect.left - 1 == e.rect.right and ((q.rect.top >= e.rect.top and q.rect.top <= e.rect.bottom) or (q.rect.bottom <= e.rect.bottom and q.rect.bottom >= e.rect.top)):
                                            f = False
                                if f and my_map.is_path_free(q.rect.left - 1, q.rect.topleft[1]) and my_map.is_path_free(q.rect.left - 1, q.rect.bottomleft[1]) and my_map.is_path_free(q.rect.left - 1, q.rect.midleft[1]) and my_map.is_path_free(q.rect.left - 1, q.rect.midleft[1] - 7) and my_map.is_path_free(q.rect.left - 1, q.rect.midleft[1] + 7):
                                    q.rect.x -= q.speed
                                    q.move_times -=1
                            elif q.move == 1:
                                q.image = pg.transform.rotate(pg.image.load("images\enemy_tank.png").convert_alpha(), 0)
                                q.position = 1
                                f = True
                                if not tank1.is_destroyed and q.rect.top - 1 == tank1.rect.bottom and ((q.rect.left >= tank1.rect.left and q.rect.left <= tank1.rect.right) or (q.rect.right <= tank1.rect.right and q.rect.right >= tank1.rect.left)):
                                    f = False
                                for e in enemies:
                                    if e != q:
                                        if not e.is_destroyed and q.rect.top - 1 == e.rect.bottom and ((q.rect.left >= e.rect.left and q.rect.left <= e.rect.right) or (q.rect.right <= e.rect.right and q.rect.right >= e.rect.left)):
                                            f = False
                                if f and my_map.is_path_free(q.rect.topleft[0], q.rect.topleft[1] - 1) and my_map.is_path_free(q.rect.topright[0], q.rect.topright[1] - 1) and my_map.is_path_free(q.rect.midtop[0], q.rect.midtop[1] - 1) and my_map.is_path_free(q.rect.midtop[0] + 7, q.rect.midtop[1] - 1) and my_map.is_path_free(q.rect.midtop[0] - 7, q.rect.midtop[1] - 1):
                                    q.rect.y -= q.speed
                                    q.move_times -=1
                            elif q.move == 2:
                                q.image = pg.transform.rotate(pg.image.load("images\enemy_tank.png").convert_alpha(), 270)
                                q.position = 2
                                f = True
                                if not tank1.is_destroyed and q.rect.right + 1 == tank1.rect.left and ((q.rect.top >= tank1.rect.top and q.rect.top <= tank1.rect.bottom) or (q.rect.bottom <= tank1.rect.bottom and q.rect.bottom >= tank1.rect.top)):
                                    f = False
                                for e in enemies:
                                    if e != q:
                                        if not e.is_destroyed and q.rect.right + 1 == e.rect.left and ((q.rect.top >= e.rect.top and q.rect.top <= e.rect.bottom) or (q.rect.bottom <= e.rect.bottom and q.rect.bottom >= e.rect.top)):
                                            f = False
                                if f and my_map.is_path_free(q.rect.topright[0] + 1, q.rect.topright[1]) and my_map.is_path_free(q.rect.bottomright[0] + 1, q.rect.bottomright[1]) and my_map.is_path_free(q.rect.midright[0] + 1, q.rect.midright[1]) and my_map.is_path_free(q.rect.midright[0] + 1, q.rect.midright[1] + 7) and my_map.is_path_free(q.rect.midright[0] + 1, q.rect.midright[1] - 7):
                                    q.rect.x += q.speed
                                    q.move_times -=1
                            elif q.move == 3:
                                q.image = pg.transform.rotate(pg.image.load("images\enemy_tank.png").convert_alpha(), 180)
                                q.position = 3
                                f = True
                                if not tank1.is_destroyed and q.rect.bottom + 1 == tank1.rect.top and ((q.rect.left >= tank1.rect.left and q.rect.left <= tank1.rect.right) or (q.rect.right <= tank1.rect.right and q.rect.right >= tank1.rect.left)):
                                    f = False
                                for e in enemies:
                                    if e != q:
                                        if not e.is_destroyed and q.rect.bottom + 1 == e.rect.top and ((q.rect.left >= e.rect.left and q.rect.left <= e.rect.right) or (q.rect.right <= e.rect.right and q.rect.right >= e.rect.left)):
                                            f = False
                                if f and my_map.is_path_free(q.rect.bottomleft[0], q.rect.bottomleft[1] + 1) and my_map.is_path_free(q.rect.bottomright[0], q.rect.bottomright[1] + 1) and my_map.is_path_free(q.rect.midbottom[0], q.rect.midbottom[1] + 1) and my_map.is_path_free(q.rect.midbottom[0] - 7, q.rect.midbottom[1] + 1) and my_map.is_path_free(q.rect.midbottom[0] + 7, q.rect.midbottom[1] + 1):
                                    q.rect.y += q.speed
                                    q.move_times -=1
                            if not q.is_fire and my_map.distance(q.rect.center, tank1.rect.center) < 150 and q.can_i_shoot(tank1, my_map):
                                q.Fire("images\enemy_fire.png")

                    if tank1.is_fire:
                        if tank1.fire.position == 1:
                            f = True
                            for e in enemies:
                                if not e.is_destroyed and (tank1.fire.rect.top > e.rect.bottom or (tank1.fire.rect.top <= e.rect.bottom and tank1.fire.rect.top > e.rect.top)) and tank1.fire.rect.top - tank1.fire.speed <= e.rect.bottom and ((tank1.fire.rect.left >= e.rect.left and tank1.fire.rect.left <= e.rect.right) or (tank1.fire.rect.right <= e.rect.right and tank1.fire.rect.right >= e.rect.left)):
                                    f = False
                                    e.is_destroyed = True
                            if f and my_map.is_path_free(tank1.fire.rect.topleft[0], tank1.fire.rect.topleft[1] - 1, 1, 1) and my_map.is_path_free(tank1.fire.rect.topright[0], tank1.fire.rect.topright[1] - 1, 1, 1) and my_map.is_path_free(tank1.fire.rect.midtop[0], tank1.fire.rect.midtop[1] - 1, 1, 1):
                                tank1.fire.rect.y -= tank1.fire.speed
                            else:
                                tank1.is_fire = False
                        elif tank1.fire.position == 2:
                            f = True
                            for e in enemies:
                                if not e.is_destroyed and (tank1.fire.rect.right < e.rect.left or (tank1.fire.rect.right >= e.rect.left and tank1.fire.rect.right < e.rect.right)) and tank1.fire.rect.right + tank1.fire.speed >= e.rect.left and ((tank1.fire.rect.top >= e.rect.top and tank1.fire.rect.top <= e.rect.bottom) or (tank1.fire.rect.bottom <= e.rect.bottom and tank1.fire.rect.bottom >= e.rect.top)):
                                    f = False
                                    e.is_destroyed = True
                            if f and my_map.is_path_free(tank1.fire.rect.topright[0] + 1, tank1.fire.rect.topright[1], 1, 2) and my_map.is_path_free(tank1.fire.rect.bottomright[0] + 1, tank1.fire.rect.bottomright[1], 1, 2) and my_map.is_path_free(tank1.fire.rect.midright[0] + 1, tank1.fire.rect.midright[1], 1, 2):
                                tank1.fire.rect.x += tank1.fire.speed
                            else:
                                tank1.is_fire = False
                        elif tank1.fire.position == 3:
                            f = True
                            for e in enemies:
                                if not e.is_destroyed and (tank1.fire.rect.bottom < e.rect.top or (tank1.fire.rect.bottom >= e.rect.top and tank1.fire.rect.bottom < e.rect.bottom)) and tank1.fire.rect.bottom + tank1.fire.speed >= e.rect.top and ((tank1.fire.rect.left >= e.rect.left and tank1.fire.rect.left <= e.rect.right) or (tank1.fire.rect.right <= e.rect.right and tank1.fire.rect.right >= e.rect.left)):
                                    f = False
                                    e.is_destroyed = True
                            if f and my_map.is_path_free(tank1.fire.rect.bottomleft[0], tank1.fire.rect.bottomleft[1] + 1, 1, 3) and my_map.is_path_free(tank1.fire.rect.bottomright[0], tank1.fire.rect.bottomright[1] + 1, 1, 3) and my_map.is_path_free(tank1.fire.rect.midbottom[0], tank1.fire.rect.midbottom[1] + 1, 1, 3):
                                tank1.fire.rect.y += tank1.fire.speed
                            else:
                                tank1.is_fire = False
                        else:
                            f = True
                            for e in enemies:
                                if not e.is_destroyed and (tank1.fire.rect.left > e.rect.right or (tank1.fire.rect.left <= e.rect.right and tank1.fire.rect.left > e.rect.left)) and tank1.fire.rect.left - tank1.fire.speed <= e.rect.right and ((tank1.fire.rect.top >= e.rect.top and tank1.fire.rect.top <= e.rect.bottom) or (tank1.fire.rect.bottom <= e.rect.bottom and tank1.fire.rect.bottom >= e.rect.top)):
                                    f = False
                                    e.is_destroyed = True
                            if f and my_map.is_path_free(tank1.fire.rect.topleft[0] - 1, tank1.fire.rect.topleft[1], 1, 4) and my_map.is_path_free(tank1.fire.rect.bottomleft[0] - 1, tank1.fire.rect.bottomleft[1], 1, 4) and my_map.is_path_free(tank1.fire.rect.midleft[0] - 1, tank1.fire.rect.midleft[1], 1, 4):
                                tank1.fire.rect.x -= tank1.fire.speed
                            else:
                                tank1.is_fire = False
                    for e in enemies:
                        if not e.is_destroyed and e.is_fire:
                            if e.fire.position == 1:
                                f = True
                                if not tank1.is_destroyed and (e.fire.rect.top > tank1.rect.bottom or (e.fire.rect.top <= tank1.rect.bottom and e.fire.rect.top > tank1.rect.top)) and e.fire.rect.top - e.fire.speed <= tank1.rect.bottom and ((e.fire.rect.left >= tank1.rect.left and e.fire.rect.left <= tank1.rect.right) or (e.fire.rect.right <= tank1.rect.right and e.fire.rect.right >= tank1.rect.left)):
                                    f = False
                                    tank1.hp -= 1
                                if f and my_map.is_path_free(e.fire.rect.topleft[0], e.fire.rect.topleft[1] - 1, 1, 1) and my_map.is_path_free(e.fire.rect.topright[0], e.fire.rect.topright[1] - 1, 1, 1) and my_map.is_path_free(e.fire.rect.midtop[0], e.fire.rect.midtop[1] - 1, 1, 1):
                                    e.fire.rect.y -= e.fire.speed
                                else:
                                    e.is_fire = False
                            elif e.fire.position == 2:
                                f = True
                                if not tank1.is_destroyed and (e.fire.rect.right < tank1.rect.left or (e.fire.rect.right >= tank1.rect.left and e.fire.rect.right < tank1.rect.right)) and e.fire.rect.right + e.fire.speed >= tank1.rect.left and ((e.fire.rect.top >= tank1.rect.top and e.fire.rect.top <= tank1.rect.bottom) or (e.fire.rect.bottom <= tank1.rect.bottom and e.fire.rect.bottom >= tank1.rect.top)):
                                    f = False
                                    tank1.hp -= 1
                                if f and my_map.is_path_free(e.fire.rect.topright[0] + 1, e.fire.rect.topright[1], 1, 2) and my_map.is_path_free(e.fire.rect.bottomright[0] + 1, e.fire.rect.bottomright[1], 1, 2) and my_map.is_path_free(e.fire.rect.midright[0] + 1, e.fire.rect.midright[1], 1, 2):
                                    e.fire.rect.x += e.fire.speed
                                else:
                                    e.is_fire = False
                            elif e.fire.position == 3:
                                f = True
                                if not tank1.is_destroyed and (e.fire.rect.bottom < tank1.rect.top or (e.fire.rect.bottom >= tank1.rect.top and e.fire.rect.bottom < tank1.rect.bottom)) and e.fire.rect.bottom + e.fire.speed >= tank1.rect.top and ((e.fire.rect.left >= tank1.rect.left and e.fire.rect.left <= tank1.rect.right) or (e.fire.rect.right <= tank1.rect.right and e.fire.rect.right >= tank1.rect.left)):
                                    f = False
                                    tank1.hp -= 1
                                if f and my_map.is_path_free(e.fire.rect.bottomleft[0], e.fire.rect.bottomleft[1] + 1, 1, 3) and my_map.is_path_free(e.fire.rect.bottomright[0], e.fire.rect.bottomright[1] + 1, 1, 3) and my_map.is_path_free(e.fire.rect.midbottom[0], e.fire.rect.midbottom[1] + 1, 1, 3):
                                    e.fire.rect.y += e.fire.speed
                                else:
                                    e.is_fire = False
                            else:
                                f = True
                                if not tank1.is_destroyed and (e.fire.rect.left > tank1.rect.right or (e.fire.rect.left <= tank1.rect.right and e.fire.rect.left > tank1.rect.left)) and e.fire.rect.left - e.fire.speed <= tank1.rect.right and ((e.fire.rect.top >= tank1.rect.top and e.fire.rect.top <= tank1.rect.bottom) or (e.fire.rect.bottom <= tank1.rect.bottom and e.fire.rect.bottom >= tank1.rect.top)):
                                    f = False
                                    tank1.hp -= 1
                                if f and my_map.is_path_free(e.fire.rect.topleft[0] - 1, e.fire.rect.topleft[1], 1, 4) and my_map.is_path_free(e.fire.rect.bottomleft[0] - 1, e.fire.rect.bottomleft[1], 1, 4) and my_map.is_path_free(e.fire.rect.midleft[0] - 1, e.fire.rect.midleft[1], 1, 4):
                                    e.fire.rect.x -= e.fire.speed
                                else:
                                    e.is_fire = False

                return (move, self.mini_max(0, alpha_beta, my_map, tank1, enemies, limit, deep = curr_deep, move = move)[1])
        else:
            return [move, self.evaluate(map, me, enemy, move)]

    def expectimax(self, who, map, me, enemy, limit = 2, move = 0, deep = 0):
        curr_deep = deep + 1
        result = [0, -123456]
        if curr_deep <= limit:
            if who:
                j = int(me.rect.center[0] / 32)
                i = int(me.rect.center[1] / 32)
                if (me.rect.center[0] - 13) // 32 != j:
                    j = j * 2
                elif (me.rect.center[0] + 13) // 32 != j:
                    j = j * 2 + 2
                else:
                    j = j * 2 + 1
                if (me.rect.center[1] - 13) // 32 != i:
                    i = i * 2
                elif (me.rect.center[1] + 13) // 32 != i:
                    i = i * 2 + 2
                else:
                    i = i * 2 + 1

                curr_var = [0, -123456]
                if map.check((i - 1, j)):
                    curr_var = self.expectimax(0, map, me, enemy, limit, move = 1, deep = curr_deep)
                    if curr_var[1] > result[1]:
                        result[0] = curr_var[0]
                        result[1] = curr_var[1]
                if map.check((i, j + 1)):
                    curr_var = self.expectimax(0, map, me, enemy, limit, move = 2, deep = curr_deep)
                    if curr_var[1] > result[1]:
                        result[0] = curr_var[0]
                        result[1] = curr_var[1]
                if map.check((i + 1, j)):
                    curr_var = self.expectimax(0, map, me, enemy, limit, move = 3, deep = curr_deep)
                    if curr_var[1] > result[1]:
                        result[0] = curr_var[0]
                        result[1] = curr_var[1]
                if map.check((i, j - 1)):
                    curr_var = self.expectimax(0, map, me, enemy, limit, move = 4, deep = curr_deep)
                    if curr_var[1] > result[1]:
                        result[0] = curr_var[0]
                        result[1] = curr_var[1]
                if not me.is_fire:
                    curr_var = self.expectimax(0, map, me, enemy, limit, move = 5, deep = curr_deep)
                    if curr_var[1] > result[1]:
                        result[0] = curr_var[0]
                        result[1] = curr_var[1]
                    curr_var = self.expectimax(0, map, me, enemy, limit, move = 6, deep = curr_deep)
                    if curr_var[1] > result[1]:
                        result[0] = curr_var[0]
                        result[1] = curr_var[1]
                    curr_var = self.expectimax(0, map, me, enemy, limit, move = 7, deep = curr_deep)
                    if curr_var[1] > result[1]:
                        result[0] = curr_var[0]
                        result[1] = curr_var[1]
                    curr_var = self.expectimax(0, map, me, enemy, limit, move = 8, deep = curr_deep)
                    if curr_var[1] > result[1]:
                        result[0] = curr_var[0]
                        result[1] = curr_var[1]
                return result
            else:
                res = 0
                for p in range(len(enemy)):
                    if not enemy[p].is_destroyed:
                        count = 0
                        sum = 0
                        for z in range(1,5):
                            if map.check_for_expec(enemy[p], z):
                                count += 1
                                my_map = map.copy()
                                tank1 = my_tank(me.rect.center[0], me.rect.center[1], me.speed, me.hp, "images\my_tank.png")
                                tank1.position = me.position
                                tank1.is_fire = me.is_fire
                                tank1.fire = fire(me.fire.rect.center[0], me.fire.rect.center[1], 2, "images\\fire.png", me.fire.position)
                                enemies = []
                                for i in range(len(enemy)):
                                    enemies.append(my_tank(enemy[i].rect.center[0], enemy[i].rect.center[1], enemy[i].speed, enemy[i].hp, "images\enemy_tank.png"))
                                    enemies[i].position = enemy[i].position
                                    enemies[i].is_destroyed = enemy[i].is_destroyed
                                enemies[p].move = z
                                enemies[p].move_times = 16
                                if move < 5:
                                    tank1.move = move
                                    tank1.move_times = 16
                                else:
                                    tank1.ready_aim_fire = True
                                    tank1.move = move - 4
                                    tank1.move_times = 16
                                for i in range(16):
                                    if tank1.move == 4:
                                        tank1.image = pg.transform.rotate(pg.image.load("images\\my_tank.png").convert_alpha(), 90)
                                        tank1.position = 4
                                        f = True
                                        for e in enemies:
                                            if not e.is_destroyed and tank1.rect.left - 1 == e.rect.right and ((tank1.rect.top >= e.rect.top and tank1.rect.top <= e.rect.bottom) or (tank1.rect.bottom <= e.rect.bottom and tank1.rect.bottom >= e.rect.top)):
                                                f = False
                                        if f and my_map.is_path_free(tank1.rect.left - 1, tank1.rect.topleft[1]) and my_map.is_path_free(tank1.rect.left - 1, tank1.rect.bottomleft[1]) and my_map.is_path_free(tank1.rect.left - 1, tank1.rect.midleft[1]) and my_map.is_path_free(tank1.rect.left - 1, tank1.rect.midleft[1] - 7) and my_map.is_path_free(tank1.rect.left - 1, tank1.rect.midleft[1] + 7):
                                            tank1.rect.x -= tank1.speed
                                            tank1.move_times -= 1
                                        if not tank1.is_fire and tank1.ready_aim_fire:
                                            tank1.Fire("images\\fire.png")
                                    elif tank1.move == 1:
                                        tank1.image = pg.transform.rotate(pg.image.load("images\my_tank.png").convert_alpha(), 0)
                                        tank1.position = 1
                                        f = True
                                        for e in enemies:
                                            if not e.is_destroyed and tank1.rect.top - 1 == e.rect.bottom and ((tank1.rect.left >= e.rect.left and tank1.rect.left <= e.rect.right) or (tank1.rect.right <= e.rect.right and tank1.rect.right >= e.rect.left)):
                                                f = False
                                        if f and my_map.is_path_free(tank1.rect.topleft[0], tank1.rect.topleft[1] - 1) and my_map.is_path_free(tank1.rect.topright[0], tank1.rect.topright[1] - 1) and my_map.is_path_free(tank1.rect.midtop[0], tank1.rect.midtop[1] - 1) and my_map.is_path_free(tank1.rect.midtop[0] + 7, tank1.rect.midtop[1] - 1) and my_map.is_path_free(tank1.rect.midtop[0] - 7, tank1.rect.midtop[1] - 1):
                                            tank1.rect.y -= tank1.speed
                                            tank1.move_times -= 1
                                        if not tank1.is_fire and tank1.ready_aim_fire:
                                            tank1.Fire("images\\fire.png")
                                    elif tank1.move == 2:
                                        tank1.image = pg.transform.rotate(pg.image.load("images\my_tank.png").convert_alpha(), 270)
                                        tank1.position = 2
                                        f = True
                                        for e in enemies:
                                            if not e.is_destroyed and tank1.rect.right + 1 == e.rect.left and ((tank1.rect.top >= e.rect.top and tank1.rect.top <= e.rect.bottom) or (tank1.rect.bottom <= e.rect.bottom and tank1.rect.bottom >= e.rect.top)):
                                                f = False
                                        if f and my_map.is_path_free(tank1.rect.topright[0] + 1, tank1.rect.topright[1]) and my_map.is_path_free(tank1.rect.bottomright[0] + 1, tank1.rect.bottomright[1]) and my_map.is_path_free(tank1.rect.midright[0] + 1, tank1.rect.midright[1]) and my_map.is_path_free(tank1.rect.midright[0] + 1, tank1.rect.midright[1] + 7) and my_map.is_path_free(tank1.rect.midright[0] + 1, tank1.rect.midright[1] - 7):
                                            tank1.rect.x += tank1.speed
                                            tank1.move_times -= 1
                                        if not tank1.is_fire and tank1.ready_aim_fire:
                                            tank1.Fire("images\\fire.png")
                                    elif tank1.move == 3:
                                        tank1.image = pg.transform.rotate(pg.image.load("images\my_tank.png").convert_alpha(), 180)
                                        tank1.position = 3
                                        f = True
                                        for e in enemies:
                                            if not e.is_destroyed and tank1.rect.bottom + 1 == e.rect.top and ((tank1.rect.left >= e.rect.left and tank1.rect.left <= e.rect.right) or (tank1.rect.right <= e.rect.right and tank1.rect.right >= e.rect.left)):
                                                f = False
                                        if f and my_map.is_path_free(tank1.rect.bottomleft[0], tank1.rect.bottomleft[1] + 1) and my_map.is_path_free(tank1.rect.bottomright[0], tank1.rect.bottomright[1] + 1) and my_map.is_path_free(tank1.rect.midbottom[0], tank1.rect.midbottom[1] + 1) and my_map.is_path_free(tank1.rect.midbottom[0] - 7, tank1.rect.midbottom[1] + 1) and my_map.is_path_free(tank1.rect.midbottom[0] + 7, tank1.rect.midbottom[1] + 1):
                                            tank1.rect.y += tank1.speed
                                            tank1.move_times -= 1
                                        if not tank1.is_fire and tank1.ready_aim_fire:
                                            tank1.Fire("images\\fire.png")
                                    q = enemies[p]
                                    if q.move == 4:
                                        q.image = pg.transform.rotate(pg.image.load("images\enemy_tank.png").convert_alpha(), 90)
                                        q.position = 4
                                        f = True
                                        if not tank1.is_destroyed and q.rect.left - 1 == tank1.rect.right and ((q.rect.top >= tank1.rect.top and q.rect.top <= tank1.rect.bottom) or (q.rect.bottom <= tank1.rect.bottom and q.rect.bottom >= tank1.rect.top)):
                                            f = False
                                        for e in enemies:
                                            if e != q:
                                                if not e.is_destroyed and q.rect.left - 1 == e.rect.right and ((q.rect.top >= e.rect.top and q.rect.top <= e.rect.bottom) or (q.rect.bottom <= e.rect.bottom and q.rect.bottom >= e.rect.top)):
                                                    f = False
                                        if f and my_map.is_path_free(q.rect.left - 1, q.rect.topleft[1]) and my_map.is_path_free(q.rect.left - 1, q.rect.bottomleft[1]) and my_map.is_path_free(q.rect.left - 1, q.rect.midleft[1]) and my_map.is_path_free(q.rect.left - 1, q.rect.midleft[1] - 7) and my_map.is_path_free(q.rect.left - 1, q.rect.midleft[1] + 7):
                                            q.rect.x -= q.speed
                                            q.move_times -=1
                                    elif q.move == 1:
                                        q.image = pg.transform.rotate(pg.image.load("images\enemy_tank.png").convert_alpha(), 0)
                                        q.position = 1
                                        f = True
                                        if not tank1.is_destroyed and q.rect.top - 1 == tank1.rect.bottom and ((q.rect.left >= tank1.rect.left and q.rect.left <= tank1.rect.right) or (q.rect.right <= tank1.rect.right and q.rect.right >= tank1.rect.left)):
                                            f = False
                                        for e in enemies:
                                            if e != q:
                                                if not e.is_destroyed and q.rect.top - 1 == e.rect.bottom and ((q.rect.left >= e.rect.left and q.rect.left <= e.rect.right) or (q.rect.right <= e.rect.right and q.rect.right >= e.rect.left)):
                                                    f = False
                                        if f and my_map.is_path_free(q.rect.topleft[0], q.rect.topleft[1] - 1) and my_map.is_path_free(q.rect.topright[0], q.rect.topright[1] - 1) and my_map.is_path_free(q.rect.midtop[0], q.rect.midtop[1] - 1) and my_map.is_path_free(q.rect.midtop[0] + 7, q.rect.midtop[1] - 1) and my_map.is_path_free(q.rect.midtop[0] - 7, q.rect.midtop[1] - 1):
                                            q.rect.y -= q.speed
                                            q.move_times -=1
                                    elif q.move == 2:
                                        q.image = pg.transform.rotate(pg.image.load("images\enemy_tank.png").convert_alpha(), 270)
                                        q.position = 2
                                        f = True
                                        if not tank1.is_destroyed and q.rect.right + 1 == tank1.rect.left and ((q.rect.top >= tank1.rect.top and q.rect.top <= tank1.rect.bottom) or (q.rect.bottom <= tank1.rect.bottom and q.rect.bottom >= tank1.rect.top)):
                                            f = False
                                        for e in enemies:
                                            if e != q:
                                                if not e.is_destroyed and q.rect.right + 1 == e.rect.left and ((q.rect.top >= e.rect.top and q.rect.top <= e.rect.bottom) or (q.rect.bottom <= e.rect.bottom and q.rect.bottom >= e.rect.top)):
                                                    f = False
                                        if f and my_map.is_path_free(q.rect.topright[0] + 1, q.rect.topright[1]) and my_map.is_path_free(q.rect.bottomright[0] + 1, q.rect.bottomright[1]) and my_map.is_path_free(q.rect.midright[0] + 1, q.rect.midright[1]) and my_map.is_path_free(q.rect.midright[0] + 1, q.rect.midright[1] + 7) and my_map.is_path_free(q.rect.midright[0] + 1, q.rect.midright[1] - 7):
                                            q.rect.x += q.speed
                                            q.move_times -=1
                                    elif q.move == 3:
                                        q.image = pg.transform.rotate(pg.image.load("images\enemy_tank.png").convert_alpha(), 180)
                                        q.position = 3
                                        f = True
                                        if not tank1.is_destroyed and q.rect.bottom + 1 == tank1.rect.top and ((q.rect.left >= tank1.rect.left and q.rect.left <= tank1.rect.right) or (q.rect.right <= tank1.rect.right and q.rect.right >= tank1.rect.left)):
                                            f = False
                                        for e in enemies:
                                            if e != q:
                                                if not e.is_destroyed and q.rect.bottom + 1 == e.rect.top and ((q.rect.left >= e.rect.left and q.rect.left <= e.rect.right) or (q.rect.right <= e.rect.right and q.rect.right >= e.rect.left)):
                                                    f = False
                                        if f and my_map.is_path_free(q.rect.bottomleft[0], q.rect.bottomleft[1] + 1) and my_map.is_path_free(q.rect.bottomright[0], q.rect.bottomright[1] + 1) and my_map.is_path_free(q.rect.midbottom[0], q.rect.midbottom[1] + 1) and my_map.is_path_free(q.rect.midbottom[0] - 7, q.rect.midbottom[1] + 1) and my_map.is_path_free(q.rect.midbottom[0] + 7, q.rect.midbottom[1] + 1):
                                            q.rect.y += q.speed
                                            q.move_times -=1
                                    if not q.is_fire and my_map.distance(q.rect.center, tank1.rect.center) < 150 and q.can_i_shoot(tank1, my_map):
                                        q.Fire("images\enemy_fire.png")

                                    if tank1.is_fire:
                                        if tank1.fire.position == 1:
                                            f = True
                                            for e in enemies:
                                                if not e.is_destroyed and (tank1.fire.rect.top > e.rect.bottom or (tank1.fire.rect.top <= e.rect.bottom and tank1.fire.rect.top > e.rect.top)) and tank1.fire.rect.top - tank1.fire.speed <= e.rect.bottom and ((tank1.fire.rect.left >= e.rect.left and tank1.fire.rect.left <= e.rect.right) or (tank1.fire.rect.right <= e.rect.right and tank1.fire.rect.right >= e.rect.left)):
                                                    f = False
                                                    e.is_destroyed = True
                                            if f and my_map.is_path_free(tank1.fire.rect.topleft[0], tank1.fire.rect.topleft[1] - 1, 1, 1) and my_map.is_path_free(tank1.fire.rect.topright[0], tank1.fire.rect.topright[1] - 1, 1, 1) and my_map.is_path_free(tank1.fire.rect.midtop[0], tank1.fire.rect.midtop[1] - 1, 1, 1):
                                                tank1.fire.rect.y -= tank1.fire.speed
                                            else:
                                                tank1.is_fire = False
                                        elif tank1.fire.position == 2:
                                            f = True
                                            for e in enemies:
                                                if not e.is_destroyed and (tank1.fire.rect.right < e.rect.left or (tank1.fire.rect.right >= e.rect.left and tank1.fire.rect.right < e.rect.right)) and tank1.fire.rect.right + tank1.fire.speed >= e.rect.left and ((tank1.fire.rect.top >= e.rect.top and tank1.fire.rect.top <= e.rect.bottom) or (tank1.fire.rect.bottom <= e.rect.bottom and tank1.fire.rect.bottom >= e.rect.top)):
                                                    f = False
                                                    e.is_destroyed = True
                                            if f and my_map.is_path_free(tank1.fire.rect.topright[0] + 1, tank1.fire.rect.topright[1], 1, 2) and my_map.is_path_free(tank1.fire.rect.bottomright[0] + 1, tank1.fire.rect.bottomright[1], 1, 2) and my_map.is_path_free(tank1.fire.rect.midright[0] + 1, tank1.fire.rect.midright[1], 1, 2):
                                                tank1.fire.rect.x += tank1.fire.speed
                                            else:
                                                tank1.is_fire = False
                                        elif tank1.fire.position == 3:
                                            f = True
                                            for e in enemies:
                                                if not e.is_destroyed and (tank1.fire.rect.bottom < e.rect.top or (tank1.fire.rect.bottom >= e.rect.top and tank1.fire.rect.bottom < e.rect.bottom)) and tank1.fire.rect.bottom + tank1.fire.speed >= e.rect.top and ((tank1.fire.rect.left >= e.rect.left and tank1.fire.rect.left <= e.rect.right) or (tank1.fire.rect.right <= e.rect.right and tank1.fire.rect.right >= e.rect.left)):
                                                    f = False
                                                    e.is_destroyed = True
                                            if f and my_map.is_path_free(tank1.fire.rect.bottomleft[0], tank1.fire.rect.bottomleft[1] + 1, 1, 3) and my_map.is_path_free(tank1.fire.rect.bottomright[0], tank1.fire.rect.bottomright[1] + 1, 1, 3) and my_map.is_path_free(tank1.fire.rect.midbottom[0], tank1.fire.rect.midbottom[1] + 1, 1, 3):
                                                tank1.fire.rect.y += tank1.fire.speed
                                            else:
                                                tank1.is_fire = False
                                        else:
                                            f = True
                                            for e in enemies:
                                                if not e.is_destroyed and (tank1.fire.rect.left > e.rect.right or (tank1.fire.rect.left <= e.rect.right and tank1.fire.rect.left > e.rect.left)) and tank1.fire.rect.left - tank1.fire.speed <= e.rect.right and ((tank1.fire.rect.top >= e.rect.top and tank1.fire.rect.top <= e.rect.bottom) or (tank1.fire.rect.bottom <= e.rect.bottom and tank1.fire.rect.bottom >= e.rect.top)):
                                                    f = False
                                                    e.is_destroyed = True
                                            if f and my_map.is_path_free(tank1.fire.rect.topleft[0] - 1, tank1.fire.rect.topleft[1], 1, 4) and my_map.is_path_free(tank1.fire.rect.bottomleft[0] - 1, tank1.fire.rect.bottomleft[1], 1, 4) and my_map.is_path_free(tank1.fire.rect.midleft[0] - 1, tank1.fire.rect.midleft[1], 1, 4):
                                                tank1.fire.rect.x -= tank1.fire.speed
                                            else:
                                                tank1.is_fire = False
                                    for e in enemies:
                                        if not e.is_destroyed and e.is_fire:
                                            if e.fire.position == 1:
                                                f = True
                                                if not tank1.is_destroyed and (e.fire.rect.top > tank1.rect.bottom or (e.fire.rect.top <= tank1.rect.bottom and e.fire.rect.top > tank1.rect.top)) and e.fire.rect.top - e.fire.speed <= tank1.rect.bottom and ((e.fire.rect.left >= tank1.rect.left and e.fire.rect.left <= tank1.rect.right) or (e.fire.rect.right <= tank1.rect.right and e.fire.rect.right >= tank1.rect.left)):
                                                    f = False
                                                    tank1.hp -= 1
                                                if f and my_map.is_path_free(e.fire.rect.topleft[0], e.fire.rect.topleft[1] - 1, 1, 1) and my_map.is_path_free(e.fire.rect.topright[0], e.fire.rect.topright[1] - 1, 1, 1) and my_map.is_path_free(e.fire.rect.midtop[0], e.fire.rect.midtop[1] - 1, 1, 1):
                                                    e.fire.rect.y -= e.fire.speed
                                                else:
                                                    e.is_fire = False
                                            elif e.fire.position == 2:
                                                f = True
                                                if not tank1.is_destroyed and (e.fire.rect.right < tank1.rect.left or (e.fire.rect.right >= tank1.rect.left and e.fire.rect.right < tank1.rect.right)) and e.fire.rect.right + e.fire.speed >= tank1.rect.left and ((e.fire.rect.top >= tank1.rect.top and e.fire.rect.top <= tank1.rect.bottom) or (e.fire.rect.bottom <= tank1.rect.bottom and e.fire.rect.bottom >= tank1.rect.top)):
                                                    f = False
                                                    tank1.hp -= 1
                                                if f and my_map.is_path_free(e.fire.rect.topright[0] + 1, e.fire.rect.topright[1], 1, 2) and my_map.is_path_free(e.fire.rect.bottomright[0] + 1, e.fire.rect.bottomright[1], 1, 2) and my_map.is_path_free(e.fire.rect.midright[0] + 1, e.fire.rect.midright[1], 1, 2):
                                                    e.fire.rect.x += e.fire.speed
                                                else:
                                                    e.is_fire = False
                                            elif e.fire.position == 3:
                                                f = True
                                                if not tank1.is_destroyed and (e.fire.rect.bottom < tank1.rect.top or (e.fire.rect.bottom >= tank1.rect.top and e.fire.rect.bottom < tank1.rect.bottom)) and e.fire.rect.bottom + e.fire.speed >= tank1.rect.top and ((e.fire.rect.left >= tank1.rect.left and e.fire.rect.left <= tank1.rect.right) or (e.fire.rect.right <= tank1.rect.right and e.fire.rect.right >= tank1.rect.left)):
                                                    f = False
                                                    tank1.hp -= 1
                                                if f and my_map.is_path_free(e.fire.rect.bottomleft[0], e.fire.rect.bottomleft[1] + 1, 1, 3) and my_map.is_path_free(e.fire.rect.bottomright[0], e.fire.rect.bottomright[1] + 1, 1, 3) and my_map.is_path_free(e.fire.rect.midbottom[0], e.fire.rect.midbottom[1] + 1, 1, 3):
                                                    e.fire.rect.y += e.fire.speed
                                                else:
                                                    e.is_fire = False
                                            else:
                                                f = True
                                                if not tank1.is_destroyed and (e.fire.rect.left > tank1.rect.right or (e.fire.rect.left <= tank1.rect.right and e.fire.rect.left > tank1.rect.left)) and e.fire.rect.left - e.fire.speed <= tank1.rect.right and ((e.fire.rect.top >= tank1.rect.top and e.fire.rect.top <= tank1.rect.bottom) or (e.fire.rect.bottom <= tank1.rect.bottom and e.fire.rect.bottom >= tank1.rect.top)):
                                                    f = False
                                                    tank1.hp -= 1
                                                if f and my_map.is_path_free(e.fire.rect.topleft[0] - 1, e.fire.rect.topleft[1], 1, 4) and my_map.is_path_free(e.fire.rect.bottomleft[0] - 1, e.fire.rect.bottomleft[1], 1, 4) and my_map.is_path_free(e.fire.rect.midleft[0] - 1, e.fire.rect.midleft[1], 1, 4):
                                                    e.fire.rect.x -= e.fire.speed
                                                else:
                                                    e.is_fire = False
                                sum += self.evaluate(my_map, tank1, enemies, move)
                        if count != 0:
                            res += sum // count
                return (move, res)
        else:
            return [move, self.evaluate(map, me, enemy)]

    def evaluate(self, map, me, enemy, move):
        sum = 0
        #hp
        sum -= 5000 * (3 - me.hp)
        #count killed enemy
        for e in enemy:
            if e.is_destroyed:
                sum += 5000 
        #distance to nearest enemy
        value = 3228
        for i in range(len(enemy)):
            if not enemy[i].is_destroyed:
                if enemy[i].path and len(enemy[i].path) > 1:
                    curr = len(map.A_star(enemy[i].rect.center, me.rect.center))
                else:
                    curr = self.distance(me.rect.center, enemy[i].rect.center) * 0.175
                if curr < value:
                    value = curr
        sum += 1000 // value
        #enemy bullets++++
        if me.is_fire:
            for e in enemy:
                if not e.is_destroyed:
                    sum += 3000 // me.fire.where_i_fly(e, map)
        #my bullet+++++
        for e in enemy:
            if not e.is_destroyed and e.is_fire:
                sum -= 5000 // e.fire.where_i_fly(me, map)
        if move < 5:
            return sum + random.randint(1, 3)
        return sum

    def copy(self):
        new_map = map(60, 64)
        new_map.small_digitmap = self.small_digitmap.copy()
        new_map.digitmap = self.digitmap.copy()
        new_map.image = self.image.copy()
        return new_map
