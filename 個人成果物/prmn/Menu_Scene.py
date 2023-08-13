import pygame
import sys
import global_value as g


class Menu_Scene():
    def __init__(self):
        self.font = pygame.font.SysFont("MS Gothic", 50)
        self.rule_str = ["矢印キー : 押した矢印の方向に移動する",
                         "スペースキー : 弾を発射する。決定",
                         "コントロールキー : 減速する。押しているとき",
                         "　　　　　　　　   発射される弾の軌道が変わる",
                         "ｘキー : ゲームを中断する、戻る",
                         "エスケープキー : ゲームを終了させる"]
        self.choice = 0
        self.choice_change_time = 0
            
    def db_save_highscore(self):
        if g.user_name in g.HighScore["user_name"].values:
            g.db.update((g.user_name, g.high_score, g.date))
        else:
            g.db.insert((g.user_name, g.high_score, g.date))

    def quit(self, screen):
        quit_start = g.counter
        end = self.font.render("ゲームを終了します", True, (255, 255, 255))
        while True:
            screen.blit(end, (g.width / 2 - end.get_width() / 2, g.height / 2 - end.get_height() / 2))
            g.counter += 1
            pygame.display.update()
            if g.counter - quit_start > 5000:
                break
        self.db_save_highscore()
        pygame.quit()
        sys.exit()

    def menu(self, screen):
        start = self.font.render("始める", True, (255, 255, 255))
        rule = self.font.render("操作方法", True, (255, 255, 255))
        highscore = self.font.render("High Score", True, (255, 255, 255))
        ranking = self.font.render("ハイスコアランキング", True, (255, 255, 255))
        end = self.font.render("終了", True, (255, 255, 255))
        menu_strs = [start, rule, highscore, ranking, end]
        pygame.draw.polygon(screen, (255, 241, 0), [[g.width / 2 - menu_strs[3].get_width() / 2 - 10, g.height / 2 - menu_strs[self.choice].get_height() / 2 + (self.choice - 2) * 100 + 25],
                                                    [g.width / 2 - menu_strs[3].get_width() / 2 - 35, g.height / 2 - menu_strs[self.choice].get_height() / 2 + (self.choice - 2) * 100 + 37.5],
                                                    [g.width / 2 - menu_strs[3].get_width() / 2 - 35, g.height / 2 - menu_strs[self.choice].get_height() / 2 + (self.choice - 2) * 100 + 12.5]])
        for i, str in enumerate(menu_strs):
            i -= 2
            screen.blit(str, (g.width / 2 - str.get_width() / 2, g.height / 2 - str.get_height() / 2 + i * 100))

    def highscore(self, screen):
        date = self.font.render("更新された日 : " + g.date, True, (255, 255, 255))
        user_name = self.font.render(g.user_name + "のHigh Score", True, (255, 255, 255))
        high_score =self.font.render(str(g.high_score), True, (255, 255, 255))
        screen.blit(user_name, (g.width / 2 - user_name.get_width() / 2, g.height / 2 - user_name.get_height() / 2 - 60))
        screen.blit(high_score, (g.width / 2 - high_score.get_width() / 2, g.height / 2 - high_score.get_height() / 2))
        screen.blit(date, (g.width / 2 - date.get_width() / 2, g.height / 2 - date.get_height() / 2 + 60))

    def ranking(self, screen):
        self.db_save_highscore()
        g.HighScore = g.db.sort_load()
        font = pygame.font.SysFont("MS Gothic", 25)
        columns = font.render("順位" + " " + "ユーザー名" + " " + "ハイスコア" + " " + "更新日", True, (255, 255, 255))
        screen.blit(columns, (g.width / 2 - columns.get_width() / 2, g.height / 2 - columns.get_height() - 200))
        font = pygame.font.SysFont("MS Gothic", 30)
        for rank, data in enumerate(g.HighScore.values):
            rank += 1
            if rank == 11:
                break
            user_name, high_score, date = data
            date = "".join(date)
            order = font.render(str(rank) + " " + user_name + " " + str(high_score) + " " + date, True, (255, 255, 255))
            screen.blit(order, (g.width / 2 - order.get_width() / 2, g.height / 2 - order.get_height() / 2 + (rank - 5) * 40))

    def rule(self, screen):
        for i, text in enumerate(self.rule_str):
            font = pygame.font.SysFont("MS Gothic", 25)
            rule_text = font.render(text, True, (255, 255, 255))
            screen.blit(rule_text, (30, 30 + i * 55))
    
    def select(self, key, switch, pouse_time):
        if switch == 0:
            if key[pygame.K_UP] and g.counter - self.choice_change_time > 10:
                self.choice = (self.choice + 4) % 5
                self.choice_change_time = g.counter
            elif key[pygame.K_DOWN] and g.counter - self.choice_change_time > 10:
                self.choice = (self.choice + 1) % 5
                self.choice_change_time = g.counter
            
            if (key[pygame.K_SPACE] or key[pygame.K_RETURN]) and g.counter - pouse_time > 20:
                if self.choice == 0:
                    self.choice_change_time = 0
                    return 5
                else:
                    return self.choice
        else:
            if key[pygame.K_x]:
                return 0
            
        return switch