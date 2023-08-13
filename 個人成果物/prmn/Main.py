import pygame
import sys
import datetime
from Menu_Scene import Menu_Scene
from Game_Scene import Game_Scene
from DB import DB
from Input_Text import Input_Text
import global_value as g

def db_save_highscore():
    if g.user_name in g.HighScore["user_name"].values:
        g.db.update((g.user_name, g.high_score, g.date))
    else:
        g.db.insert((g.user_name, g.high_score, g.date))

pygame.init()
screen = pygame.display.set_mode((g.width, g.height))
g.scene.append(Input_Text())
g.fps = 60
switch = 0
pouse_time = 0
first_time = True
first_write = True
g.clock = pygame.time.Clock()
g.db = DB()
g.HighScore = g.db.load()

while True:
    screen.fill((0, 0, 0))

    if g.user_name != "" and first_write:
        if g.user_name in g.HighScore["user_name"].values:
            g.high_score = int(g.HighScore[g.HighScore["user_name"] == g.user_name]["high_score"].values)
            g.date = "".join(g.HighScore[g.HighScore["user_name"] == g.user_name]["date"].values)
        else:
            g.high_score = 0
            g.date = str(datetime.date.today())
        first_write = False
    if g.high_score < g.score:
        g.high_score = g.score
        g.date = str(datetime.date.today())
    now_scene = g.scene[-1]
    key = pygame.key.get_pressed()
    for event in pygame.event.get():
        if key[pygame.K_ESCAPE] or event.type == pygame.QUIT:
            db_save_highscore()
            pygame.quit()
            sys.exit()    
        if event.type == pygame.VIDEORESIZE:
                screen.fill((0, 0, 0))
                g.width, g.height = screen.get_width(), screen.get_height()    

    if isinstance(now_scene, Game_Scene):
        if first_time:
            now_scene.countdown(screen)
            first_time = False
            now_scene.player_shot_time = g.counter 
        gameover, pouse_select = now_scene.game(screen, key)
        if pouse_select == -1:
            pass
        elif pouse_select == 0:
            now_scene.switch = 0
        elif pouse_select == 1:
            g.scene.pop()
            pouse_time = g.counter
        if gameover == True:
            pouse_time = g.counter
            g.scene.pop()
            db_save_highscore()
    
    elif isinstance(now_scene, Input_Text):
        pygame.key.start_text_input()
        now_scene.draw_text(screen, "".join(now_scene.text))
        now_scene.event_loop(screen)
        g.scene.append(Menu_Scene())

    elif isinstance(now_scene, Menu_Scene):
        if switch == 0:
            now_scene.menu(screen)
            switch = now_scene.select(key, switch, pouse_time)
            first_time = True
            g.score = 0
        elif switch == 1:
            now_scene.rule(screen)
            switch = now_scene.select(key, switch, pouse_time)
        elif switch == 2:
            now_scene.highscore(screen)
            switch = now_scene.select(key, switch, pouse_time)
        elif switch == 3:
            now_scene.ranking(screen)
            switch = now_scene.select(key, switch, pouse_time)
        elif switch == 4:
            now_scene.quit(screen)
            switch = now_scene.select(key, switch, pouse_time)
        elif switch == 5:
            g.scene.append(Game_Scene())
            switch = 0

    pygame.display.update()
    g.clock.tick(g.fps) 
    g.counter += 1