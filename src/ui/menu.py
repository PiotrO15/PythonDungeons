import pygame
import pandas as pd

from src import utils
from src.utils import SCREEN_CENTER


class Button:
    color = (255, 255, 255)

    def __init__(self, menu, x, y: int, text: str, fontsize: int):
        self.menu = menu
        self.text = text
        font = pygame.font.Font(utils.font, fontsize)
        self.text_surface = font.render(self.text, True, self.color)
        self.text_rect = self.text_surface.get_rect(midtop=(x, y))

    def detect_action(self):
        pass

    def update(self):
        # change button color on hover?
        # if self.text_rect.collidepoint(mouse):
        #     self.text_rect.color = (200, 200, 200)
        # else:
        #     self.text_rect.color = (255, 255, 255)
        self.detect_action()

    def draw(self, surface):
        surface.blit(self.text_surface, self.text_rect)


class PlayButton(Button):
    def __init__(self, menu, y):
        super().__init__(menu, utils.SCREEN_CENTER[0], y, 'PLAY', 60)

    def detect_action(self):
        pos = pygame.mouse.get_pos()
        if self.text_rect.collidepoint(pos) and pygame.mouse.get_pressed()[0] == 1:
            self.menu.running = False
            self.menu.game.paused = False


class ExitButton(Button):
    def __init__(self, menu, y):
        super().__init__(menu, utils.SCREEN_CENTER[0], y, 'EXIT', 60)

    def detect_action(self):
        pos = pygame.mouse.get_pos()
        if self.text_rect.collidepoint(pos) and pygame.mouse.get_pressed()[0] == 1:
            self.menu.game.running = False
            self.menu.running = False


class StatButton(Button):
    def __init__(self, menu, y):
        super().__init__(menu, utils.SCREEN_CENTER[0], y, 'LEADERBOARD', 60)

    def detect_action(self):
        pos = pygame.mouse.get_pos()
        if self.text_rect.collidepoint(pos) and pygame.mouse.get_pressed()[0] == 1:
            self.menu.leaderboard.visible = True


class LeaderBoard:
    visible = False

    def __init__(self, menu):
        self.game = menu.game
        self.surf = pygame.Surface((800, 600))
        self.surf.fill((35, 15, 25))
        self.rect = pygame.Rect(0, 0, 800, 600)
        self.rect.center = SCREEN_CENTER
        # load and sort the stats
        self.df: pd.DataFrame = self.game.load_stats()
        self.df = self.df.sort_values(by=['points'], na_position='last', ascending=False)

    def update(self):
        self.detect_action()

    def detect_action(self):
        pos = pygame.mouse.get_pos()
        if not self.rect.collidepoint(pos) and pygame.mouse.get_pressed()[0] == 1:
            self.visible = False

    def draw(self, surface):
        if self.visible:
            # add title
            text_surface = pygame.font.Font(utils.font, 40).render('LEADERBOARD', True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=(400, 50))

            self.surf.blit(text_surface, text_rect)

            offset = 150

            # Display leaderboard
            for index, row in self.df.iterrows():
                text_surface = pygame.font.Font(utils.font, 24).render(f'{index}. {row['name']} | {row['points']} points', True, (255, 255, 255))
                text_rect = text_surface.get_rect(midleft=(50, offset))

                self.surf.blit(text_surface, text_rect)
                offset += 60

            self.game.screen.blit(self.surf, self.rect)


class Logo:
    def __init__(self, game):
        self.logo = pygame.image.load('./assets/misc/logo.png').convert_alpha()
        self.logo = pygame.transform.scale(self.logo, (400, 250))
        self.logo_rect = self.logo.get_rect()
        self.logo_rect.midtop = (utils.SCREEN_CENTER[0], 50)

    def draw(self, surface):
        surface.blit(self.logo, self.logo_rect)


class MainMenu:
    def __init__(self, game):
        self.game = game
        self.running = True
        self.play_button = PlayButton(self, 300)
        self.exit_button = ExitButton(self, 450)
        self.stat_button = StatButton(self, 600)
        self.leaderboard = LeaderBoard(self)

    def input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

    def update(self):
        self.play_button.update()
        self.exit_button.update()
        self.stat_button.update()

        self.leaderboard.update()

    def draw(self):
        self.game.screen.fill((20, 5, 15))

        # Draw buttons
        self.play_button.draw(self.game.screen)
        self.exit_button.draw(self.game.screen)
        self.stat_button.draw(self.game.screen)

        self.leaderboard.draw(self.game.screen)

    def show(self):
        while self.running:
            self.input()
            self.update()
            self.draw()
            # self.game.clock.tick(self.game.fps)
            self.game.display.blit(self.game.screen, (0, 0))
            pygame.display.flip()
