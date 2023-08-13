from Enemy import Enemy
import random
import numpy as np
import global_value as g

class Hiscore_Enemy(Enemy):
    def move(self, screen, player_pos):
        if g.counter % random.randint(10, 40) == 0:
            if player_pos[0] > g.width / 2:
                self.pos_change[0] = random.uniform(-2.5, 2)
            else:
                self.pos_change[0] = random.uniform(-2, 2.5)
            if player_pos[1] > g.height / 2:
                self.pos_change[1] = random.uniform(-2.5, 2)
            else:
                self.pos_change[1] = random.uniform(-2, 2.5)
        if random.uniform(0, 100) < 1:
            self.pos_change *= 2
        self.pos += self.pos_change
        if self.pos[0] < 12.5:
            self.pos[0] = 12.5
        if self.pos[0] > 615:
            self.pos[0] = 615
        if self.pos[1] < 12.5:
            self.pos[1] = 12.5
        if self.pos[1] > 455:
            self.pos[1] = 455