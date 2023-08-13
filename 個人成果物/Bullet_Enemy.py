import random
import numpy as np
import pygame
from Enemy import Enemy
from Bullet import Bullet
import global_value as g

class Bullet_Enemy(Enemy):
    def __init__(self, player_pos):
        x, y = random.randint(0, g.width), random.randint(0, g.height)
        while abs(player_pos[0] - x) < 200:
            x = random.randint(0, g.width)
        while abs(player_pos[1] - y) < 200:
            y = random.randint(0, g.height)
        self.pos = np.array([x, y], dtype=np.float64)
        self.pos_change = np.array([0, 0])
        self.bullets = []
        for i in range(10):
            self.bullets.append(Bullet())
        self.repop_time = 0
        self.score = 500
        self.hp = 1

    def repop(self, player_pos):
        if self.repop_time == 0:
            self.repop_time = g.counter
            self.pos = np.array([10000, 10000])
            self.bullets = []
            g.score += self.score
        elif g.counter - self.repop_time > 180:
            x, y = random.randint(0, g.width), random.randint(0, g.height)
            while abs(player_pos[0] - x) < 200:
                x = random.randint(0, g.width)
            while abs(player_pos[1] - y) < 200:
                y = random.randint(0, g.height)
            self.pos = np.array([x, y], dtype=np.float64)
            self.pos_change = np.array([0, 0])
            self.hp = 1
            for i in range(10):
                self.bullets.append(Bullet())
            self.repop_time = 0
        else:
            self.pos = np.array([10000, 10000])

    def blit(self, screen):
        enemy = pygame.Rect(self.pos[0] - 12.5, self.pos[1] - 12.5, 25, 25)
        screen.fill((255, 0, 0), enemy)
    
    def move(self, screen, player_pos):
        if g.counter % random.randint(30, 40) == 0:
            if player_pos[0] < self.pos[0]:
                self.pos_change[0] = random.uniform(-3, 2)
            else:
                self.pos_change[0] = random.uniform(-2, 3)
            if player_pos[1] < self.pos[1]:
                self.pos_change[1] = random.uniform(-3, 2)
            else:
                self.pos_change[1] = random.uniform(-2, 3)
        self.pos += self.pos_change
        if self.pos[0] < 12.5:
            self.pos[0] = 12.5
        if self.pos[0] > 615:
            self.pos[0] = 615
        if self.pos[1] < 12.5:
            self.pos[1] = 12.5
        if self.pos[1] > 455:
            self.pos[1] = 455
        bullet_type = random.uniform(0, 1)
        if bullet_type < 0.25:
            self.shot(screen, player_pos, 1, 0)
        elif bullet_type < 0.5:
            self.horming_shot(screen, player_pos, 1, 0)
        elif bullet_type < 0.75:
            self.shot(screen, player_pos, 3, np.deg2rad(40))
        else:
            self.horming_shot(screen, player_pos, 3, np.deg2rad(40))

    def shot(self, screen, player_pos, count, deff_angle):
        self.reload(count)
        for bullet in self.bullets:
            count, deff_angle = bullet.shot(screen, self.pos, player_pos, count, deff_angle)
                
    def horming_shot(self, screen, player_pos, count, deff_angle):
        self.reload(count)
        for bullet in self.bullets:
            count, deff_angle = bullet.horming_shot(screen, self.pos, player_pos, count, deff_angle)
    
    def reload(self, count):
        cnt = 0
        for bullet in self.bullets:
            if bullet.state == 0:
                cnt += 1
        if cnt < count:
            for bullet in self.bullets:
                bullet.reload()
