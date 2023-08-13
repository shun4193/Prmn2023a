import pygame
import sys
import global_value as g

class Input_Text:
    def __init__(self):
        self.text = ["|"]
        self.editing = []
        self.japanese_editing = False
        self.input_pos = 0
        self.event_trigger = {
            pygame.K_BACKSPACE : self.backspace,
            pygame.K_LEFT : self.move_left,
            pygame.K_RIGHT : self.move_right,
            pygame.K_RETURN : self.enter,
        }
        self.font = pygame.font.SysFont("MS Gothic", 30)
    
    def draw_text(self, screen, text):
        message = self.font.render("使用するユーザー名を入力してください", True, (255, 255, 255))
        text = self.font.render(text, True, (255, 255, 255))
        screen.fill((0, 0, 0))
        center_w = (g.width / 2) - (text.get_width() / 2)
        center_h = (g.height / 2) - (text.get_height() / 2) + 50
        screen.blit(text, (center_w, center_h))
        screen.blit(message, (g.width / 2 - message.get_width() / 2, g.height / 2 - message.get_height() / 2 - 50))
        pygame.display.update()

    def event_loop(self, screen):
        input_text = ""
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.VIDEORESIZE:
                    screen.fill((0, 0, 0))
                    g.width, g.height = screen.get_width(), screen.get_height()
                    self.draw_text(screen, input_text)
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN and not self.japanese_editing:
                    if event.key in self.event_trigger.keys():
                        input_text = self.event_trigger[event.key]()
                    if event.key ==  pygame.K_RETURN:
                        g.user_name = input_text
                        self.draw_text(screen, "".join(self.text))
                        running = False
                        break
                elif event.type == pygame.TEXTEDITING:
                    input_text = self.edit(event.text, event.start)
                elif event.type == pygame.TEXTINPUT:
                    input_text = self.input(event.text)
                if event.type in [pygame.KEYDOWN, pygame.TEXTEDITING, pygame.TEXTINPUT]:
                    self.draw_text(screen, input_text)

    def edit(self, text, editing_input_pos):
        if text:
            self.japanese_editing = True
            for x in text:
                self.editing.append(x)
            self.editing.insert(editing_input_pos, "|")
            disp = "".join(self.editing)
        else:
            self.japanese_editing = False
            disp = "|"
        self.editing = []
        return "".join(self.text)[0 : self.input_pos] + disp + "".join(self.text)[self.input_pos + 1 :]
    
    def input(self, text):
        self.japanese_editing = False
        for x in text:
            self.text.insert(self.input_pos, x)
            self.input_pos += 1
        return "".join(self.text)
    
    def backspace(self):
        if self.input_pos == 0:
            return "".join(self.text)
        self.text.pop(self.input_pos - 1)
        self.input_pos -= 1
        return "".join(self.text)
    
    def enter(self):
        entered = "".join(self.text)[0 : self.input_pos] + "".join(self.text)[self.input_pos + 1 :]
        self.text = ["|"]
        self.input_pos = 0
        return entered
    
    def move_left(self):
        if self.input_pos > 0:
            self.text[self.input_pos], self.text[self.input_pos - 1] = (
                self.text[self.input_pos - 1],
                self.text[self.input_pos],
            )
            self.input_pos -= 1
        return "".join(self.text)
    
    def move_right(self):
        if len(self.text) - 1 > self.input_pos:
            self.text[self.input_pos], self.text[self.input_pos + 1] = (
                self.text[self.input_pos + 1],
                self.text[self.input_pos],
            )
            self.input_pos += 1
        return "".join(self.text)