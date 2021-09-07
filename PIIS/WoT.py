from numpy import positive, true_divide
import pygame as pg
import pygame.display as dp
from my_tank import my_tank
from map import map
import random

def is_there_tank(my_tank, enemies, point):
    if ((point[0] - my_tank.rect.center[0]) ** 2 + (point[1] - my_tank.rect.center[1]) ** 2) ** 0.5 <= 37:
        return True
    for e in enemies:
        if not e.is_destroyed and ((point[0] - e.rect.center[0]) ** 2 + (point[1] - e.rect.center[1]) ** 2) ** 0.5 <= 37:
            return True
    return False

pg.init()
sc = dp.set_mode((448, 480))
dp.set_caption("Battle City")
dp.set_icon(pg.image.load("images\\my_tank.png"))

menu = True
selected = 0
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
select_image = pg.image.load("images\\selected.png").convert_alpha()
clock = pg.time.Clock()
FPS = 60
fin = 0


my_map = map(56, 56)
tank1 = None 
enemies = []
enemy_count = 16
enemy_on_map = 0
spawn = 2
spawn_point = [(32, 32),(224, 32), (32, 224), (416, 224), (416, 32)]

pg.mixer.music.load("sounds\\Horse Steppin.mp3")
pg.mixer.music.play(-1)
while True:
    if menu:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                exit()
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    exit()
                elif event.key == pg.K_DOWN:
                    if selected == 2:
                        selected = 0
                    else:
                        selected += 1
                elif event.key == pg.K_UP:
                    if selected == 0:
                        selected = 2
                    else:
                        selected -= 1
                elif event.key == pg.K_SPACE:
                    menu = False
                    spawn = 2
                    enemy_on_map = 0
                    enemy_count = 16
                    fin = 0
                    my_map.select_map(selected + 1)
                    tank1 = my_tank(224, 368, 1, "images\my_tank.png")
                    if selected == 0:
                        pg.mixer.music.load("sounds\\Knock Knock.mp3")
                        pg.mixer.music.play(-1)
                    elif selected == 1:
                        pg.mixer.music.load("sounds\\Hydrogen.mp3")
                        pg.mixer.music.play(-1)
                    else:
                        pg.mixer.music.load("sounds\\Hotline.mp3")
                        pg.mixer.music.play(-1)


        sc.fill((0, 0, 0))
        if fin == -1:
            sc.blit(lose_text, lose_rect)
        elif fin == 1:
            sc.blit(win_text, win_rect)
        for i in range(3):
            sc.blit(text[i], text_pos[i])
        sc.blit(select_image, select_image.get_rect(center = (180, 180 + selected * 48)))
        dp.update()
        clock.tick(FPS)
    else:
        if tank1.is_destroyed == True:
            menu = True
            enemies.clear()
            selected = 0
            enemy_count = 16
            fin = -1
        if enemy_count <= 13:
            spawn = 3
            if enemy_count <= 8:
                spawn = 4
                if enemy_count <= 2:
                    spawn = 5
            if enemy_count <= spawn:
                spawn = enemy_count
            if enemy_count == 0:
                fin = 1
                menu = True
        for i in range(spawn - enemy_on_map):
            f = True
            while f:
                r = random.randint(0,4)
                if not is_there_tank(tank1, enemies, spawn_point[r]):
                    f = False
                    enemies.append(my_tank(spawn_point[r][0], spawn_point[r][1], 1, "images\enemy_tank.png"))
                    enemy_on_map += 1
        
        for event in pg.event.get():
            if event.type == pg.QUIT:
                exit()
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    if not tank1.is_fire:
                        tank1.Fire("images\\fire.png")
                elif event.key == pg.K_ESCAPE:
                    menu = True
                    enemies.clear()
                    selected = 0
                    enemy_count = 16
                    pg.mixer.music.load("sounds\\Horse Steppin.mp3")
                    pg.mixer.music.play(-1)

        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            tank1.image = pg.transform.rotate(pg.image.load("images\my_tank.png").convert_alpha(), 90)
            tank1.position = 4
            f = True
            for e in enemies:
                if not e.is_destroyed and tank1.rect.left - 1 == e.rect.right and ((tank1.rect.top >= e.rect.top and tank1.rect.top <= e.rect.bottom) or (tank1.rect.bottom <= e.rect.bottom and tank1.rect.bottom >= e.rect.top)):
                    f = False
            if f and my_map.is_path_free(tank1.rect.left - 1, tank1.rect.topleft[1]) and my_map.is_path_free(tank1.rect.left - 1, tank1.rect.bottomleft[1]) and my_map.is_path_free(tank1.rect.left - 1, tank1.rect.midleft[1]) and my_map.is_path_free(tank1.rect.left - 1, tank1.rect.midleft[1] - 7) and my_map.is_path_free(tank1.rect.left - 1, tank1.rect.midleft[1] + 7):
                tank1.rect.x -= tank1.speed
        elif keys[pg.K_UP] or keys[pg.K_w]:
            tank1.image = pg.transform.rotate(pg.image.load("images\my_tank.png").convert_alpha(), 0)
            tank1.position = 1
            f = True
            for e in enemies:
                if not e.is_destroyed and tank1.rect.top - 1 == e.rect.bottom and ((tank1.rect.left >= e.rect.left and tank1.rect.left <= e.rect.right) or (tank1.rect.right <= e.rect.right and tank1.rect.right >= e.rect.left)):
                    f = False
            if f and my_map.is_path_free(tank1.rect.topleft[0], tank1.rect.topleft[1] - 1) and my_map.is_path_free(tank1.rect.topright[0], tank1.rect.topright[1] - 1) and my_map.is_path_free(tank1.rect.midtop[0], tank1.rect.midtop[1] - 1) and my_map.is_path_free(tank1.rect.midtop[0] + 7, tank1.rect.midtop[1] - 1) and my_map.is_path_free(tank1.rect.midtop[0] - 7, tank1.rect.midtop[1] - 1):
                tank1.rect.y -= tank1.speed
        elif keys[pg.K_RIGHT] or keys[pg.K_d]:
            tank1.image = pg.transform.rotate(pg.image.load("images\my_tank.png").convert_alpha(), 270)
            tank1.position = 2
            f = True
            for e in enemies:
                if not e.is_destroyed and tank1.rect.right + 1 == e.rect.left and ((tank1.rect.top >= e.rect.top and tank1.rect.top <= e.rect.bottom) or (tank1.rect.bottom <= e.rect.bottom and tank1.rect.bottom >= e.rect.top)):
                    f = False
            if f and my_map.is_path_free(tank1.rect.topright[0] + 1, tank1.rect.topright[1]) and my_map.is_path_free(tank1.rect.bottomright[0] + 1, tank1.rect.bottomright[1]) and my_map.is_path_free(tank1.rect.midright[0] + 1, tank1.rect.midright[1]) and my_map.is_path_free(tank1.rect.midright[0] + 1, tank1.rect.midright[1] + 7) and my_map.is_path_free(tank1.rect.midright[0] + 1, tank1.rect.midright[1] - 7):
                tank1.rect.x += tank1.speed
        elif keys[pg.K_DOWN] or keys[pg.K_s]:
            tank1.image = pg.transform.rotate(pg.image.load("images\my_tank.png").convert_alpha(), 180)
            tank1.position = 3
            f = True
            for e in enemies:
                if not e.is_destroyed and tank1.rect.bottom + 1 == e.rect.top and ((tank1.rect.left >= e.rect.left and tank1.rect.left <= e.rect.right) or (tank1.rect.right <= e.rect.right and tank1.rect.right >= e.rect.left)):
                    f = False
            if f and my_map.is_path_free(tank1.rect.bottomleft[0], tank1.rect.bottomleft[1] + 1) and my_map.is_path_free(tank1.rect.bottomright[0], tank1.rect.bottomright[1] + 1) and my_map.is_path_free(tank1.rect.midbottom[0], tank1.rect.midbottom[1] + 1) and my_map.is_path_free(tank1.rect.midbottom[0] - 7, tank1.rect.midbottom[1] + 1) and my_map.is_path_free(tank1.rect.midbottom[0] + 7, tank1.rect.midbottom[1] + 1):
                tank1.rect.y += tank1.speed

        for e in enemies:
            if not e.is_destroyed:
                if random.randint(1, 100) <= 3:
                    e.move = random.randint(1, 4)
                    e.move_times = random.randint(1, 10) * 8
                if not e.is_fire and random.randint(1, 100) <= 5:
                    e.Fire("images\\enemy_fire.png")

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
                        if q.move_times > 0:
                            q.rect.x -= q.speed
                            q.move_times -= 1
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
                        if q.move_times > 0:
                            q.rect.y -= q.speed
                            q.move_times -= 1
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
                        if q.move_times > 0:
                            q.rect.x += q.speed
                            q.move_times -= 1
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
                        if q.move_times > 0:
                            q.rect.y += q.speed
                            q.move_times -= 1

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
                        enemy_count -= 1
                        my_map.enemy_count[enemy_count] = False
                        enemy_on_map -= 1
                if f and my_map.is_path_free(tank1.fire.rect.topleft[0], tank1.fire.rect.topleft[1] - 1, 1) and my_map.is_path_free(tank1.fire.rect.topright[0], tank1.fire.rect.topright[1] - 1, 1) and my_map.is_path_free(tank1.fire.rect.midtop[0], tank1.fire.rect.midtop[1] - 1, 1):
                    tank1.fire.rect.y -= tank1.fire.speed
                else:
                    tank1.is_fire = False
            elif tank1.fire.position == 2:
                f = True
                for e in enemies:
                    if not e.is_destroyed and (tank1.fire.rect.right < e.rect.left or (tank1.fire.rect.right >= e.rect.left and tank1.fire.rect.right < e.rect.right)) and tank1.fire.rect.right + tank1.fire.speed >= e.rect.left and ((tank1.fire.rect.top >= e.rect.top and tank1.fire.rect.top <= e.rect.bottom) or (tank1.fire.rect.bottom <= e.rect.bottom and tank1.fire.rect.bottom >= e.rect.top)):
                        f = False
                        e.is_destroyed = True
                        enemy_count -= 1
                        my_map.enemy_count[enemy_count] = False
                        enemy_on_map -= 1
                if f and my_map.is_path_free(tank1.fire.rect.topright[0] + 1, tank1.fire.rect.topright[1], 1) and my_map.is_path_free(tank1.fire.rect.bottomright[0] + 1, tank1.fire.rect.bottomright[1], 1) and my_map.is_path_free(tank1.fire.rect.midright[0] + 1, tank1.fire.rect.midright[1], 1):
                    tank1.fire.rect.x += tank1.fire.speed
                else:
                    tank1.is_fire = False
            elif tank1.fire.position == 3:
                f = True
                for e in enemies:
                    if not e.is_destroyed and (tank1.fire.rect.bottom < e.rect.top or (tank1.fire.rect.bottom >= e.rect.top and tank1.fire.rect.bottom < e.rect.bottom)) and tank1.fire.rect.bottom + tank1.fire.speed >= e.rect.top and ((tank1.fire.rect.left >= e.rect.left and tank1.fire.rect.left <= e.rect.right) or (tank1.fire.rect.right <= e.rect.right and tank1.fire.rect.right >= e.rect.left)):
                        f = False
                        e.is_destroyed = True
                        enemy_count -= 1
                        my_map.enemy_count[enemy_count] = False
                        enemy_on_map -= 1
                if f and my_map.is_path_free(tank1.fire.rect.bottomleft[0], tank1.fire.rect.bottomleft[1] + 1, 1) and my_map.is_path_free(tank1.fire.rect.bottomright[0], tank1.fire.rect.bottomright[1] + 1, 1) and my_map.is_path_free(tank1.fire.rect.midbottom[0], tank1.fire.rect.midbottom[1] + 1, 1):
                    tank1.fire.rect.y += tank1.fire.speed
                else:
                    tank1.is_fire = False
            else:
                f = True
                for e in enemies:
                    if not e.is_destroyed and (tank1.fire.rect.left > e.rect.right or (tank1.fire.rect.left <= e.rect.right and tank1.fire.rect.left > e.rect.left)) and tank1.fire.rect.left - tank1.fire.speed <= e.rect.right and ((tank1.fire.rect.top >= e.rect.top and tank1.fire.rect.top <= e.rect.bottom) or (tank1.fire.rect.bottom <= e.rect.bottom and tank1.fire.rect.bottom >= e.rect.top)):
                        f = False
                        e.is_destroyed = True
                        enemy_count -= 1
                        my_map.enemy_count[enemy_count] = False
                        enemy_on_map -= 1
                if f and my_map.is_path_free(tank1.fire.rect.topleft[0] - 1, tank1.fire.rect.topleft[1], 1) and my_map.is_path_free(tank1.fire.rect.bottomleft[0] - 1, tank1.fire.rect.bottomleft[1], 1) and my_map.is_path_free(tank1.fire.rect.midleft[0] - 1, tank1.fire.rect.midleft[1], 1):
                    tank1.fire.rect.x -= tank1.fire.speed
                else:
                    tank1.is_fire = False
            if tank1.is_fire:
                sc.blit(tank1.fire.image, tank1.fire.rect)

        sc.blit(tank1.image, tank1.rect)

        for e in enemies:
            if not e.is_destroyed:
                sc.blit(e.image, e.rect)
        for e in enemies:
            if not e.is_destroyed and e.is_fire:
                if e.fire.position == 1:
                    f = True
                    if not tank1.is_destroyed and (e.fire.rect.top > tank1.rect.bottom or (e.fire.rect.top <= tank1.rect.bottom and e.fire.rect.top > tank1.rect.top)) and e.fire.rect.top - e.fire.speed <= tank1.rect.bottom and ((e.fire.rect.left >= tank1.rect.left and e.fire.rect.left <= tank1.rect.right) or (e.fire.rect.right <= tank1.rect.right and e.fire.rect.right >= tank1.rect.left)):
                        f = False
                        tank1.is_destroyed = True
                    if f and my_map.is_path_free(e.fire.rect.topleft[0], e.fire.rect.topleft[1] - 1, 1) and my_map.is_path_free(e.fire.rect.topright[0], e.fire.rect.topright[1] - 1, 1) and my_map.is_path_free(e.fire.rect.midtop[0], e.fire.rect.midtop[1] - 1, 1):
                        e.fire.rect.y -= e.fire.speed
                    else:
                        e.is_fire = False
                elif e.fire.position == 2:
                    f = True
                    if not tank1.is_destroyed and (e.fire.rect.right < tank1.rect.left or (e.fire.rect.right >= tank1.rect.left and e.fire.rect.right < tank1.rect.right)) and e.fire.rect.right + e.fire.speed >= tank1.rect.left and ((e.fire.rect.top >= tank1.rect.top and e.fire.rect.top <= tank1.rect.bottom) or (e.fire.rect.bottom <= tank1.rect.bottom and e.fire.rect.bottom >= tank1.rect.top)):
                        f = False
                        tank1.is_destroyed = True
                    if f and my_map.is_path_free(e.fire.rect.topright[0] + 1, e.fire.rect.topright[1], 1) and my_map.is_path_free(e.fire.rect.bottomright[0] + 1, e.fire.rect.bottomright[1], 1) and my_map.is_path_free(e.fire.rect.midright[0] + 1, e.fire.rect.midright[1], 1):
                        e.fire.rect.x += e.fire.speed
                    else:
                        e.is_fire = False
                elif e.fire.position == 3:
                    f = True
                    if not tank1.is_destroyed and (e.fire.rect.bottom < tank1.rect.top or (e.fire.rect.bottom >= tank1.rect.top and e.fire.rect.bottom < tank1.rect.bottom)) and e.fire.rect.bottom + e.fire.speed >= tank1.rect.top and ((e.fire.rect.left >= tank1.rect.left and e.fire.rect.left <= tank1.rect.right) or (e.fire.rect.right <= tank1.rect.right and e.fire.rect.right >= tank1.rect.left)):
                        f = False
                        tank1.is_destroyed = True
                    if f and my_map.is_path_free(e.fire.rect.bottomleft[0], e.fire.rect.bottomleft[1] + 1, 1) and my_map.is_path_free(e.fire.rect.bottomright[0], e.fire.rect.bottomright[1] + 1, 1) and my_map.is_path_free(e.fire.rect.midbottom[0], e.fire.rect.midbottom[1] + 1, 1):
                        e.fire.rect.y += e.fire.speed
                    else:
                        e.is_fire = False
                else:
                    f = True
                    if not tank1.is_destroyed and (e.fire.rect.left > tank1.rect.right or (e.fire.rect.left <= tank1.rect.right and e.fire.rect.left > tank1.rect.left)) and e.fire.rect.left - e.fire.speed <= tank1.rect.right and ((e.fire.rect.top >= tank1.rect.top and e.fire.rect.top <= tank1.rect.bottom) or (e.fire.rect.bottom <= tank1.rect.bottom and e.fire.rect.bottom >= tank1.rect.top)):
                        f = False
                        tank1.is_destroyed = True
                    if f and my_map.is_path_free(e.fire.rect.topleft[0] - 1, e.fire.rect.topleft[1], 1) and my_map.is_path_free(e.fire.rect.bottomleft[0] - 1, e.fire.rect.bottomleft[1], 1) and my_map.is_path_free(e.fire.rect.midleft[0] - 1, e.fire.rect.midleft[1], 1):
                        e.fire.rect.x -= e.fire.speed
                    else:
                        e.is_fire = False
                if e.is_fire:
                    sc.blit(e.fire.image, e.fire.rect)
            for i in range(len(my_map.image)):
                if my_map.digitmap[i // len(my_map.digitmap[0])][i % len(my_map.digitmap[0])] == 4:
                    sc.blit(my_map.image[i], my_map.rect[i])
            
        for i in range(len(my_map.enemy_count)):
            if my_map.enemy_count[i]:
                sc.blit(my_map.menu_image[i], my_map.menu_rect[i])

    dp.update()
    clock.tick(FPS)
