import pygame
import sys
from DB import DB
import numpy as np
import global_value as g
from Player import Player
from Hiscore_Enemy import Hiscore_Enemy
from Horming_Enemy import Horming_Enemy
from Bullet_Enemy import Bullet_Enemy

class Game_Scene:
    def __init__(self):
        self.player = Player()
        self.player_shot_time = 0
        self.enemys = []
        self.enemys.append(Hiscore_Enemy(self.player.pos))
        self.enemys.append(Horming_Enemy(self.player.pos))
        self.enemys.append(Bullet_Enemy(self.player.pos))
        self.switch = 0
        self.choice = 0
        self.choice_change_time = 0
        self.gameover_time = 0

    def db_save_highscore(self):
        if g.user_name in g.HighScore["user_name"].values:
            g.db.update((g.user_name, g.high_score, g.date))
        else:
            g.db.insert((g.user_name, g.high_score, g.date))

    def countdown(self, screen):
        running = True
        while running:
            font = pygame.font.SysFont("MS Gothic", 50)
            start = font.render("Press Start", True, (255, 255, 255))
            screen.blit(start, (g.width / 2 - start.get_width() / 2, g.height / 2 - start.get_height() / 2))
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key ==  pygame.K_ESCAPE:
                        self.db_save_highscore()
                        pygame.quit()
                        sys.exit()
                    else:
                        running = False
                if event.type ==  pygame.QUIT:
                    self.db_save_highscore()
                    pygame.quit()
                    sys.exit()
        g.counter = 0
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.db_save_highscore()
                    pygame.quit()
                    sys.exit()
            text = ""
            screen.fill((0, 0, 0))
            if g.counter <= g.fps:
                text = "3"
            elif g.counter <= g.fps * 2:
                text = "2"
            elif g.counter <= g.fps * 3:
                text = "1"
            elif g.counter <= g.fps * 4:
                break
            for enemy in self.enemys:
                enemy.blit(screen)
                if isinstance(enemy, Bullet_Enemy):
                    for bullet in enemy.bullets:
                        pygame.draw.circle(screen, (255, 255, 255), (bullet.pos[0], bullet.pos[1]), 10)
            self.player.blit(screen)
            for bullet in self.player.bullets:
                pygame.draw.circle(screen, (255, 255, 255), (bullet.pos[0], bullet.pos[1]), 10)
            
            count = font.render(text, True, (255, 255, 255))
            screen.blit(count, (g.width / 2 - count.get_width() / 2, g.height / 2 - count.get_height() / 2))
            pygame.display.update()
            g.clock.tick(g.fps)
            g.counter += 1
        g.counter = self.player_shot_time

    def pouse(self, screen, key):
        font = pygame.font.SysFont("MS Gothic", 50)
        continue_ = font.render("続ける", True, (255, 255, 255))
        end = font.render("辞める", True, (255, 255, 255))
        strs = [continue_, end]
        for i, str in enumerate(strs):
            screen.blit(str, (g.width / 2 - str.get_width() / 2, g.height / 2 - str.get_height() / 2 + (i - 0.5) * 120))
        select = self.select(screen, key)
        pygame.draw.polygon(screen, (255, 241, 0), [[g.width / 2 - strs[1].get_width() / 2 - 10, g.height / 2 - strs[self.choice].get_height() / 2 + (self.choice - 0.5) * 120 + 25],
                                                    [g.width / 2 - strs[1].get_width() / 2 - 35, g.height / 2 - strs[self.choice].get_height() / 2 + (self.choice - 0.5) * 120 + 12.5],
                                                    [g.width / 2 - strs[1].get_width() / 2 - 35, g.height / 2 - strs[self.choice].get_height() / 2 + (self.choice - 0.5) * 120 + 37.5]])
        return select
            
    def select(self, screen, key):
        self.player_shot_time = g.counter
        if key[pygame.K_UP] and g.counter - self.choice_change_time > 10:
            self.choice = (self.choice + 1) % 2
            self.choice_change_time = g.counter
        elif key[pygame.K_DOWN] and g.counter - self.choice_change_time > 10:
            self.choice = (self.choice + 1) % 2
            self.choice_change_time = g.counter
        if key[pygame.K_SPACE] or key[pygame.K_ESCAPE]:
                self.choice_change_time = 0
                if self.choice == 0:
                    screen.fill((0, 0, 0))
                    self.countdown(screen)
                    return 0
                elif self.choice == 1:
                    return 1
        else:
            return -1
        
    def gameover(self, screen):
        self.gameover_time = g.counter
        running = True
        while running:
            font = pygame.font.SysFont("MS Gothic", 50)
            gameover = font.render("Game Over", True, (255, 255, 255))
            score = font.render("score : " + str(g.score), True, (255, 255, 255))
            screen.blit(gameover, (g.width / 2 - gameover.get_width() / 2, g.height / 2 - gameover.get_height() / 2 - 60))
            screen.blit(score, (g.width / 2 - gameover.get_width() / 2, g.height / 2 - gameover.get_height() / 2 + 60))
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and g.counter - self.gameover_time > 5:
                    if event.key ==  pygame.K_ESCAPE:
                        self.db_save_highscore()
                        pygame.quit()
                        sys.exit()
                    else:
                        running = False
                if event.type ==  pygame.QUIT:
                    self.db_save_highscore()
                    pygame.quit()
                    sys.exit()
            g.clock.tick(g.fps)
            g.counter += 1
        return True, 0

    def game(self, screen, key):
        screen.fill((0, 0, 0))

        if g.high_score < g.score:
            g.high_score = g.score
        font = pygame.font.SysFont(None, 30)
        score = font.render("score : " + str(g.score), True, (255, 255, 255))
        high_score = font.render("High Score : " + str(g.high_score), True, (255, 255, 255))
        screen.blit(score, (0 + 15, 0 + 15))
        screen.blit(high_score, (0 + 15, 0 + 35))

        if key[pygame.K_SPACE] and g.counter - self.player_shot_time > 10:
            self.player.shot(screen)
            self.player_shot_time = g.counter
        elif key[pygame.K_RSHIFT or pygame.K_LSHIFT]:
            self.switch = 1

        if self.switch == 1:
            self.player_shot_time = g.counter
            return False, self.pouse(screen, key)

        self.player.move(key, screen) 

        for enemy in self.enemys:
            enemy.move(screen, self.player.pos)
            distance = abs(self.player.pos - enemy.pos)
            if distance[0] <= self.player.size() + enemy.size() and distance[1] <= self.player.size() + enemy.size():
                self.player.hp -= 1
                enemy.hp -= 10
                if enemy.hp <= 0:
                    enemy.repop(self.player.pos)
                if self.player.hp == 0:
                    screen.fill((0, 0, 0))
                    return self.gameover(screen)
            for bullet in self.player.bullets:
                distance = abs(enemy.pos - bullet.pos)
                if distance[0] <= enemy.size() + bullet.size() and distance[1] <= enemy.size() + bullet.size():
                    enemy.hp -= 1
                    if enemy.hp <= 0:
                        enemy.repop(self.player.pos)
                    bullet.pos = np.array([10000, 10000], dtype=np.float64)

        for enemy in self.enemys:
            if isinstance(enemy, Bullet_Enemy):
                for enemy_bullet in enemy.bullets:
                    distance = abs(self.player.pos - enemy_bullet.pos)
                    if distance[0] <= self.player.size() + enemy_bullet.size() and distance[1] <= self.player.size() + enemy_bullet.size():
                        enemy_bullet.pos = np.array([10000, 10000], dtype=np.float64)
                        self.player.hp -= 1
                        if self.player.hp == 0:
                            screen.fill((0, 0, 0))
                            return self.gameover(screen)
                    for player_bullet in self.player.bullets:
                        distance = abs(player_bullet.pos - enemy_bullet.pos)
                        if distance[0] <= player_bullet.size() + enemy_bullet.size() and distance[1] <= player_bullet.size() + enemy_bullet.size():
                            enemy_bullet.pos = np.array([10000, 10000], dtype=np.float64)
                            player_bullet.pos = np.array([10000, 10000], dtype=np.float64)
                            

        for enemy in self.enemys:
            if enemy.repop_time != 0:
                enemy.repop(self.player.pos)
            enemy.blit(screen)

        return False, 0