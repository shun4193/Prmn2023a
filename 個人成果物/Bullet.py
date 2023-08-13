import pygame
import numpy as np
import global_value as g

class Bullet:
    def __init__(self):
        self.pos = np.array([10000, 10000], dtype=np.float64) # 画面内に表示されないように
        self.pos_change = np.array([0, 0], dtype=np.float64)
        self.change = 7 # 進行速度７
        self.theta = 0 # 進行方向
        self.count = 0 # ホーミングした時間
        self.state = 0 # 最初は発射されていない状態の0

    def isright(self, player_pos):
        return np.cross(self.pos_change, player_pos - self.pos)
        # return self.pos_change[0] * (player_pos[1] - self.pos[1]) - self.pos_change[1] * (player_pos[0] - self.pos[0])
    
    def shot(self, screen, enemy_pos, player_pos, count, deff_angle):
        if self.state == 0 and g.counter % 60 == 0 and count > 0: # 発射する準備
            self.state = 1 # 発射されている状態を表す１にする。
            self.pos[0], self.pos[1] = enemy_pos[0], enemy_pos[1] # 最初の位置
            angle = player_pos - enemy_pos # playerの方向を出すための傾き
            self.theta = np.arctan2(angle[1], angle[0]) + deff_angle # 弾を打ち出すための角度を求める。
            self.pos_change = np.array([self.change * np.cos(self.theta), self.change * np.sin(self.theta)], dtype=np.float64)
            count -= 1
            deff_angle -= np.deg2rad(40)
        else:
            self.pos += self.pos_change
            if self.pos[0] < 0 or self.pos[0] > g.width or self.pos[1] < 0 or self.pos[1] > g.height: # 画面外に出たら
                self.pos = np.array([10000, 10000], dtype=np.float64) # 元の場所に戻す
            pygame.draw.circle(screen, (255, 255, 255), (self.pos[0], self.pos[1]), 10) # 丸で弾を表示する。
        return count, deff_angle

    def horming_shot(self, screen, enemy_pos, player_pos, count, deff_angle):
        if g.counter % 60 == 0 and self.state == 0 and count > 0: # 発射する準備
            self.state = 1
            self.pos[0], self.pos[1] = enemy_pos[0], enemy_pos[1]
            angle = player_pos - self.pos
            self.theta = np.arctan2(angle[1], angle[0]) + deff_angle
            self.pos_change = np.array([self.change * np.cos(self.theta), self.change * np.sin(self.theta)])
            count -= 1
            deff_angle -= np.deg2rad(40)
        else:
            rotate_angle = 0
            if self.isright(player_pos) > 0 and self.count < 45: # 右回り、左回りの判定
                rotate_angle = 1.5 * np.pi / 180 # 回転する角度
            elif self.isright(player_pos) < 0 and self.count < 45: # ０．７５秒間ホーミングする。
                rotate_angle = -1.5 * np.pi / 180
            rotate = np.array([[np.cos(rotate_angle), -np.sin(rotate_angle)], # 回転行列の作成
                               [np.sin(rotate_angle), np.cos(rotate_angle)]], dtype=np.float64)
            self.pos_change = np.dot(rotate, self.pos_change) # 進行方向の回転
            self.pos += self.pos_change
            if self.pos[0] < 0 or self.pos[0] > g.width or self.pos[1] < 0 or self.pos[1] > g.height: # 画面外に出たら
                self.pos = np.array([10000, 10000], dtype=np.float64) # 元の場所に戻す
            self.count += 1
            pygame.draw.circle(screen, (255, 255, 255), (self.pos[0], self.pos[1]), 10) # 丸で弾を表示する。
        return count, deff_angle
    
    def player_shot(self, screen, player_pos, theta, ok):
        if self.state == 0 and ok:
            self.state = 1
            self.pos[0], self.pos[1] = player_pos[0], player_pos[1]
            self.theta = theta
            ok = False
            self.pos_change = np.array([self.change * np.cos(self.theta), self.change * np.sin(self.theta)])
        else:
            self.pos += self.pos_change
            if self.pos[0] < 0 or self.pos[0] > g.width or self.pos[1] < 0 or self.pos[1] > g.height: # 画面外に出たら
                self.pos = np.array([10000, 10000], dtype=np.float64)
            pygame.draw.circle(screen, (0, 255, 0), (self.pos[0], self.pos[1]), 10) # 丸で弾を表示する。
        return ok
    
    def reload(self):
        self.state = 0
        self.count = 0

    def size(self):
        return 5