from os import kill
from numpy import positive, true_divide
import pygame.display as dp
from my_tank import my_tank
from csv import writer
import pygame as pg
from map import map
import random
import time as t

def is_there_tank(my_tank, enemies, point):
    if ((point[0] - my_tank.rect.center[0]) ** 2 + (point[1] - my_tank.rect.center[1]) ** 2) ** 0.5 <= 70:
        return True
    for e in enemies:
        if not e.is_destroyed and ((point[0] - e.rect.center[0]) ** 2 + (point[1] - e.rect.center[1]) ** 2) ** 0.5 <= 70:
            return True
    return False

def save_result(result, file = "result.csv"):
    with open(file, 'a+', newline = '') as write_obj: 
        csv_writer = writer(write_obj) 
        csv_writer.writerow(result)

def count_score(killed, hp, time):
    return killed * 30 - (3 - hp) * 50 - time // 1 * 2

pg.init()
sc = dp.set_mode((480, 498))
dp.set_caption("Battle City")
dp.set_icon(pg.image.load("images\\my_tank.png"))

menu = True
selected = 0
search = 1
f = pg.font.SysFont("arial", 20)
f1 = pg.font.SysFont("arial", 40)
text = []
text_pos = []
win_text = f1.render("You win!", (255, 0, 0), (0, 255, 0))
win_rect = win_text.get_rect(center = (224, 100))
lose_text = f1.render("You lose(", (255, 0, 0), (255, 0, 0))
lose_rect = lose_text.get_rect(center = (224, 100))
for i in range(3):
    text.append(f.render("Level " + str(i + 1), (255, 0, 0), (255, 255, 255)))
    text_pos.append(text[i].get_rect(center = (224, 180 + i * 48)))
text.append(f.render("Random Level", (255, 0, 0), (255, 255, 255)))
text_pos.append(text[3].get_rect(center = (224, 180 + 144)))
select_image = pg.image.load("images\\selected.png").convert_alpha()
clock = pg.time.Clock()
FPS = 60
fin = 0
frames = 0
round_time = 0
algh = 1
deep = 4

start_dumb_count = 0
my_map = map(60, 64)
tank1 = None 
enemies = []
enemy_count = 10
enemy_on_map = 0
spawn = 1
dumb_count = start_dumb_count
spawn_point = [(48, 48), (240, 48), (48, 240), (432, 240), (432, 48)]

while True:
    if menu:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                exit()
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    exit()
                elif event.key == pg.K_DOWN:
                    if selected == 3:
                        selected = 0
                    else:
                        selected += 1
                elif event.key == pg.K_UP:
                    if selected == 0:
                        selected = 3
                    else:
                        selected -= 1
                elif event.key == pg.K_SPACE:
                    menu = False
                    spawn = 1
                    enemy_on_map = 0
                    enemy_count = 10
                    dumb_count = start_dumb_count
                    fin = 0
                    my_map.select_map(selected + 1)
                    tank1 = my_tank(240, 384, 1, 3, "images\my_tank.png")
                    round_time = t.time()

        sc.fill((0, 0, 0))
        if fin == -1:
            sc.blit(lose_text, lose_rect)
        elif fin == 1:
            sc.blit(win_text, win_rect)
        for i in range(4):
            sc.blit(text[i], text_pos[i])
        if selected < 3:
            sc.blit(select_image, select_image.get_rect(center = (180, 180 + selected * 48)))
        else:
            sc.blit(select_image, select_image.get_rect(center = (148, 180 + selected * 48)))
        dp.update()
        clock.tick(FPS)
    else:
        if tank1.hp == 0:
            time = t.time() - round_time
            save_result([0, tank1.hp, 10 - enemy_count, selected + 1, str(time)[:6], count_score(10 - enemy_count, tank1.hp, time), algh])
            menu = True
            enemies.clear()
            selected = 0
            enemy_count = 10
            fin = -1
            search = 1
        if enemy_count <= 8:
            spawn = 2
            if enemy_count <= 5:
                spawn = 3
            if enemy_count <= spawn:
                spawn = enemy_count
            if enemy_count == 0:
                time = t.time() - round_time
                save_result([1, tank1.hp, 10 - enemy_count, selected + 1, str(time)[:6], count_score(10 - enemy_count, tank1.hp, time), algh])
                fin = 1
                menu = True
        for i in range(spawn - enemy_on_map):
            f = True
            while f:
                r = random.randint(0,4)
                if not is_there_tank(tank1, enemies, spawn_point[r]):
                    f = False
                    if random.randint(1, enemy_count) <= dumb_count:
                        enemies.append(my_tank(spawn_point[r][0], spawn_point[r][1], 1, 1, "images\enemy_tank.png", 0))
                        dumb_count -= 1
                    else:
                        enemies.append(my_tank(spawn_point[r][0], spawn_point[r][1], 1, 1, "images\enemy_tank.png"))
                    enemy_on_map += 1
        
        for event in pg.event.get():
            if event.type == pg.QUIT:
                exit()
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    menu = True
                    enemies.clear()
                    selected = 0
                    enemy_count = 10
                    search = 1

        if tank1.move_times == 0 or tank1.algh_time == 0:
            step = 0
            if algh:
                step = my_map.mini_max(1, (-35695, 35695), my_map, tank1, enemies, deep)[0]
            else:
                step = my_map.expectimax(1, my_map, tank1, enemies)[0]
            if step < 5:
                tank1.move = step
                tank1.move_times = tank1.how_many_steps()
                tank1.algh_time = 16
            else:
                tank1.ready_aim_fire = True
                tank1.move = step - 4
                tank1.move_times = tank1.how_many_steps()
                tank1.algh_time = 16

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
                tank1.ready_aim_fire = False
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
                tank1.ready_aim_fire = False
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
                tank1.ready_aim_fire = False
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
                tank1.ready_aim_fire = False
        tank1.algh_time -= 1

        for i in range(len(enemies)):
            if enemies[i].smart:
                if not enemies[i].is_destroyed and (enemies[i].move_times == 0 or enemies[i].algh_time == 0):
                    enemies[i].path = my_map.A_star(enemies[i].rect.center, tank1.rect.center)
                    if enemies[i].path:
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
                        enemies[i].algh_time = 16
                        enemies[i].move_times = enemies[i].how_many_steps()
            else:
                if random.randint(0, 100) < 4:
                    enemies[i].move = random.randint(1, 4)
                    enemies[i].move_times = random.randint(10, 20)
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
                if not q.is_fire and (not q.smart or my_map.distance(q.rect.center, tank1.rect.center) < 150) and q.can_i_shoot(tank1, my_map) and q.cd == 0:
                    q.Fire("images\enemy_fire.png")
            q.algh_time -= 1
            if q.cd > 0:
                q.cd -= 1

        sc.fill((100, 100, 100))
        for i in range(len(my_map.image)):
            sc.blit(my_map.image[i], my_map.rect[i])     
        if tank1.is_fire:
            if tank1.fire.position == 1:
                f = True
                for e in enemies:
                    if not e.is_destroyed and (tank1.fire.rect.top > e.rect.bottom or (tank1.fire.rect.top <= e.rect.bottom and tank1.fire.rect.top > e.rect.top)) and tank1.fire.rect.top - tank1.fire.speed <= e.rect.bottom and ((tank1.fire.rect.left >= e.rect.left and tank1.fire.rect.left <= e.rect.right) or (tank1.fire.rect.right <= e.rect.right and tank1.fire.rect.right >= e.rect.left)):
                        f = False
                        e.is_destroyed = True
                        enemies.pop(enemies.index(e))
                        enemy_count -= 1
                        my_map.enemy_count[enemy_count] = False
                        enemy_on_map -= 1
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
                        enemies.pop(enemies.index(e))#
                        enemy_count -= 1
                        my_map.enemy_count[enemy_count] = False
                        enemy_on_map -= 1
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
                        enemies.pop(enemies.index(e))#
                        enemy_count -= 1
                        my_map.enemy_count[enemy_count] = False
                        enemy_on_map -= 1
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
                        enemies.pop(enemies.index(e))#
                        enemy_count -= 1
                        my_map.enemy_count[enemy_count] = False
                        enemy_on_map -= 1
                if f and my_map.is_path_free(tank1.fire.rect.topleft[0] - 1, tank1.fire.rect.topleft[1], 1, 4) and my_map.is_path_free(tank1.fire.rect.bottomleft[0] - 1, tank1.fire.rect.bottomleft[1], 1, 4) and my_map.is_path_free(tank1.fire.rect.midleft[0] - 1, tank1.fire.rect.midleft[1], 1, 4):
                    tank1.fire.rect.x -= tank1.fire.speed
                else:
                    tank1.is_fire = False
            if tank1.is_fire:
                sc.blit(tank1.fire.image, tank1.fire.rect)
        sc.blit(tank1.image, tank1.rect)
        for e in enemies:
            if not e.is_destroyed:
                sc.blit(e.image, e.rect)
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
                        e.cd = 16
                elif e.fire.position == 2:
                    f = True
                    if not tank1.is_destroyed and (e.fire.rect.right < tank1.rect.left or (e.fire.rect.right >= tank1.rect.left and e.fire.rect.right < tank1.rect.right)) and e.fire.rect.right + e.fire.speed >= tank1.rect.left and ((e.fire.rect.top >= tank1.rect.top and e.fire.rect.top <= tank1.rect.bottom) or (e.fire.rect.bottom <= tank1.rect.bottom and e.fire.rect.bottom >= tank1.rect.top)):
                        f = False
                        tank1.hp -= 1
                    if f and my_map.is_path_free(e.fire.rect.topright[0] + 1, e.fire.rect.topright[1], 1, 2) and my_map.is_path_free(e.fire.rect.bottomright[0] + 1, e.fire.rect.bottomright[1], 1, 2) and my_map.is_path_free(e.fire.rect.midright[0] + 1, e.fire.rect.midright[1], 1, 2):
                        e.fire.rect.x += e.fire.speed
                    else:
                        e.is_fire = False
                        e.cd = 16
                elif e.fire.position == 3:
                    f = True
                    if not tank1.is_destroyed and (e.fire.rect.bottom < tank1.rect.top or (e.fire.rect.bottom >= tank1.rect.top and e.fire.rect.bottom < tank1.rect.bottom)) and e.fire.rect.bottom + e.fire.speed >= tank1.rect.top and ((e.fire.rect.left >= tank1.rect.left and e.fire.rect.left <= tank1.rect.right) or (e.fire.rect.right <= tank1.rect.right and e.fire.rect.right >= tank1.rect.left)):
                        f = False
                        tank1.hp -= 1
                    if f and my_map.is_path_free(e.fire.rect.bottomleft[0], e.fire.rect.bottomleft[1] + 1, 1, 3) and my_map.is_path_free(e.fire.rect.bottomright[0], e.fire.rect.bottomright[1] + 1, 1, 3) and my_map.is_path_free(e.fire.rect.midbottom[0], e.fire.rect.midbottom[1] + 1, 1, 3):
                        e.fire.rect.y += e.fire.speed
                    else:
                        e.is_fire = False
                        e.cd = 16
                else:
                    f = True
                    if not tank1.is_destroyed and (e.fire.rect.left > tank1.rect.right or (e.fire.rect.left <= tank1.rect.right and e.fire.rect.left > tank1.rect.left)) and e.fire.rect.left - e.fire.speed <= tank1.rect.right and ((e.fire.rect.top >= tank1.rect.top and e.fire.rect.top <= tank1.rect.bottom) or (e.fire.rect.bottom <= tank1.rect.bottom and e.fire.rect.bottom >= tank1.rect.top)):
                        f = False
                        tank1.hp -= 1
                    if f and my_map.is_path_free(e.fire.rect.topleft[0] - 1, e.fire.rect.topleft[1], 1, 4) and my_map.is_path_free(e.fire.rect.bottomleft[0] - 1, e.fire.rect.bottomleft[1], 1, 4) and my_map.is_path_free(e.fire.rect.midleft[0] - 1, e.fire.rect.midleft[1], 1, 4):
                        e.fire.rect.x -= e.fire.speed
                    else:
                        e.is_fire = False
                        e.cd = 16
                if e.is_fire:
                    sc.blit(e.fire.image, e.fire.rect)
            for i in range(len(my_map.image)):
                if my_map.digitmap[i // len(my_map.digitmap[0])][i % len(my_map.digitmap[0])] == 4:
                    sc.blit(my_map.image[i], my_map.rect[i])  
        
        for i in range(len(my_map.enemy_count)):
            if my_map.enemy_count[i]:
                sc.blit(my_map.menu_image[i], my_map.menu_rect[i])
        for i in range(tank1.hp):
            sc.blit(my_map.hp[i], my_map.hp_rect[i])

    dp.update()
    clock.tick(FPS)