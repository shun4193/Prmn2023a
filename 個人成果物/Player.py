import numpy as np
import pygame
from Bullet import Bullet
import global_value as g

class Player:
    def __init__(self):
        self.pos = np.array([g.width / 2,  g.height / 2])
        self.pos_change = np.array([0, 0], dtype=float)
        self.angle = 0
        self.hp = 3
        self.bullets = []
        for i in range(5):
            self.bullets.append(Bullet())

    def move(self, key, screen):
        if key[pygame.K_LEFT]: # 左が押されていたら
            self.pos_change[0] = -5    
        if key[pygame.K_RIGHT]: # 右が押されていたら
            self.pos_change[0] = 5
        if key[pygame.K_UP]: # 上が押されていたら
            self.pos_change[1] = -5 
        if key[pygame.K_DOWN]: # 下が押されていたら
            self.pos_change[1] = 5
        if sum(self.pos_change ** 2) != 0: # 変化させる量がゼロでなければ
            self.angle = np.arctan2(self.pos_change[1], self.pos_change[0]) # playerの進行方向
            if key[pygame.K_RCTRL] or key[pygame.K_LCTRL]: # コントロールが押されていれば、低速移動
                self.pos_change = self.pos_change / 2 # 0.5倍速        
            if key[pygame.K_c]:
                self.pos_change = self.pos_change * 0
        if self.pos_change[0] != 0 and self.pos_change[1] != 0: # 斜め移動しているならば
            self.pos_change /= np.sqrt(2) # 斜め移動のほうがはやくなるので、その調整
        self.pos += self.pos_change # 移動させる。
        self.pos_change *= 0 # 変化量をもとに戻す
                
        if self.pos[0] < 12.5: 
            self.pos[0] = 12.5
        if self.pos[0] > 625.5:
            self.pos[0] = 625.5
        if self.pos[1] < 12.5: 
            self.pos[1] = 12.5
        if self.pos[1] > 465.5: 
            self.pos[1] = 465.5

        self.blit(screen)
        for bullet in self.bullets:
            bullet.player_shot(screen, self.pos, self.angle, False)

    def blit(self, screen):
        # playerを表示させる。
        player = pygame.Rect(self.pos[0] - 12.5, self.pos[1] - 12.5, 25, 25)
        screen.fill((0, 255, 0), player)

    def shot(self, screen):
        self.reload()
        ok = True
        for bullet in self.bullets:
            ok = bullet.player_shot(screen, self.pos, self.angle, ok)

    def reload(self):
        empty = True
        for bullet in self.bullets:
            if bullet.state == 0:
                empty = False
            else:
                if bullet.pos[0] >= 0 and bullet.pos[0] <= g.width and bullet.pos[1] >= 0 and bullet.pos[1] <= g.height:
                    empty = False
        if empty:
            for bullet in self.bullets:
                bullet.reload()

    def size(self):
        return 12.5