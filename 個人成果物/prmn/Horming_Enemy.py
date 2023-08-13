import random
import numpy as np
import pygame
from Enemy import Enemy
import global_value as g

class Horming_Enemy(Enemy):
    def __init__(self, player_pos):
        x, y = random.randint(0, g.width), random.randint(0, g.height)
        while abs(player_pos[0] - x) < 200:
            x = random.randint(0, g.width)
        while abs(player_pos[1] - y) < 200:
            y = random.randint(0, g.height)
        self.pos = np.array([x, y])
        self.pos_change = 3
        self.repop_time = 0
        self.score = 100
        self.hp = 1

    def repop(self, player_pos):
        if self.repop_time == 0:
            self.repop_time = g.counter
            self.pos = np.array([10000, 10000])
            g.score += self.score
        elif g.counter - self.repop_time > 180:
            x, y = random.randint(0, g.width), random.randint(0, g.height)
            while abs(player_pos[0] - x) < 200:
                x = random.randint(0, g.width)
            while abs(player_pos[1] - y) < 200:
                y = random.randint(0, g.height)
            self.pos = np.array([x, y])
            self.pos_change = 3
            self.repop_time = 0
            self.hp = 1
        else:
            self.pos = np.array([10000, 10000])

    def blit(self, screen):
        enemy = pygame.Rect(self.pos[0] - 12.5, self.pos[1] - 12.5, 25, 25)
        screen.fill((0, 0, 255), enemy)
    
    def move(self, screen, player_pos):
        theta = np.arctan2(player_pos[1] - self.pos[1], player_pos[0]- self.pos[0])
        self.pos[0] += self.pos_change * np.cos(theta)
        self.pos[1] += self.pos_change * np.sin(theta)