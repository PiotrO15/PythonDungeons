import pygame

from src import utils
from menu import Button

class SaveButton(Button):
    def __init__(self, menu, y):
        super().__init__(menu, utils.SCREEN_CENTER[0], y, 'SAVE', 60)

    def detect_action(self, pos):
        if self.text_rect.collidepoint(pos) and pygame.mouse.get_pressed()[0] == 1:
            ...


class ExitButton(Button):
    def __init__(self, menu, y):
        super().__init__(menu, utils.SCREEN_CENTER[0], y, 'EXIT', 60)

    def detect_action(self, pos):
        if self.text_rect.collidepoint(pos) and pygame.mouse.get_pressed()[0] == 1:
            self.menu.game.running = False
            self.menu.running = False

class GameOver:
    def __init__(self, game):
        self.game = game
        self.position = utils.SCREEN_CENTER

    @staticmethod
    def input():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

    def update(self):
        if self.game.player.dead:
            self.input()

    def draw_message(self):
        text_surface = pygame.font.Font(utils.font, 60).render('GAME OVER', True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=utils.SCREEN_CENTER)
        self.game.screen.blit(text_surface, text_rect)

    def draw(self):
        if self.game.player.dead:
            # darken background
            s = pygame.Surface(utils.SCREEN_SIZE)
            s.set_alpha(128)
            s.fill((0, 0, 0))
            self.game.screen.blit(s, (0, 0))

            self.draw_message()
