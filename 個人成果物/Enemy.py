import random
import numpy as np
import pygame
import global_value as g

class Enemy:
    def __init__(self, player_pos):
        x, y = random.randint(0, g.width), random.randint(0, g.height)
        while abs(player_pos[0] - x) < 200:
            x = random.randint(0, g.width)
        while abs(player_pos[1] - y) < 200:
            y = random.randint(0, g.height)
        self.pos = np.array([x, y])
        self.pos_change = np.array([0, 0])
        self.repop_time = 0
        self.score = 1000
        self.hp = 3

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
            self.pos_change = np.array([0, 0])
            self.repop_time = 0
            self.hp = 3
        else:
            self.pos = np.array([10000, 10000])

    def blit(self, screen):
        enemy = pygame.Rect(self.pos[0] - 12.5, self.pos[1] - 12.5, 25, 25)
        screen.fill((255, 255, 255), enemy)
  
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

    def size(self):
        return 12.5