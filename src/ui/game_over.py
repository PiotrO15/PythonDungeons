import pygame

from src import utils
from .menu import Button

class TextInputBox(pygame.sprite.Sprite):
    def __init__(self, game, x, y, width, fontsize):
        super().__init__()
        self.game = game
        self.text_color = (255, 255, 255)
        self.backcolor = (0, 0, 30)
        self.pos = (x, y)
        self.width = width
        self.font = pygame.font.Font(utils.font, fontsize)
        self.text = ""
        self.char_limit = 12
        self.active = False
        self.render_text()

    def render_text(self):
        text_surf = self.font.render(self.text, True, self.text_color)

        self.box_surf = pygame.Surface((self.width, text_surf.get_height() + 20), pygame.SRCALPHA)
        if self.active and self.backcolor:
            self.box_surf.fill(self.backcolor)
        self.box_surf.blit(text_surf, (10, 10))

        pygame.draw.rect(self.box_surf, self.text_color, self.box_surf.get_rect().inflate(-2, -2), 2)
        self.rect = self.box_surf.get_rect(topleft=self.pos)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)

        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_RETURN:
                self.active = False
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif len(self.text) < self.char_limit:
                self.text += event.unicode

    def update(self):
        self.render_text()

    def draw(self, surface):
        surface.blit(self.box_surf, self.pos)
class SaveButton(Button):
    def __init__(self, menu, x, y):
        super().__init__(menu, x, y, 'SAVE', 60)

    def detect_action(self, pos):
        if self.text_rect.collidepoint(pos) and pygame.mouse.get_pressed()[0] == 1:
            name = self.menu.input_box.text
            print(name)
            ... # TODO
class ExitButton(Button):
    def __init__(self, menu, x, y):
        super().__init__(menu, x, y, 'EXIT', 60)

    def detect_action(self, pos):
        if self.text_rect.collidepoint(pos) and pygame.mouse.get_pressed()[0] == 1:
            self.menu.game.running = False
            self.menu.running = False

class GameOver:
    def __init__(self, game):
        self.game = game
        self.running = True

        self.save_button = SaveButton(self, 300, 300)
        self.exit_button = ExitButton(self, 300, 450)
        self.input_box = TextInputBox(self.game, 700, 90, 250, 24)


    def input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            self.input_box.handle_event(event)

    def update(self):
        if self.game.player.dead:
            self.input()
            self.input_box.update()

            self.save_button.update()
            self.exit_button.update()

    def draw_message(self):
        text_surface = pygame.font.Font(utils.font, 60).render('GAME OVER', True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=utils.SCREEN_CENTER)
        self.game.screen.blit(text_surface, text_rect)

    def draw_input_box(self):
        surf = self.game.screen
        self.input_box.draw(surf)
        self.save_button.draw(surf)
        self.exit_button.draw(surf)
    def draw(self):
        if self.game.player.dead:
            # darken background
            s = pygame.Surface(utils.SCREEN_SIZE)
            s.set_alpha(128)
            s.fill((0, 0, 0))
            self.game.screen.blit(s, (0, 0))

            self.draw_message()
            self.draw_input_box()

    def show(self):
        while self.running:
            self.input()
            self.update()
            self.draw()

            self.game.display.blit(self.game.screen, (0, 0))
            pygame.display.flip()
