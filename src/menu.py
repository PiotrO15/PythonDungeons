import pygame

from src import utils


class Button:

    def __init__(self, menu, y: int, text: str):
        self.menu = menu
        self.text = text
        font = pygame.font.Font(utils.font, 60)
        self.text_surface = font.render(self.text, True, (255, 255, 255))
        self.text_rect = self.text_surface.get_rect(midtop=(utils.SCREEN_CENTER[0], y))

    def detect_action(self, pos):
        pass

    def update(self):
        mouse = pygame.mouse.get_pos()
        # change button color on hover?
        # if self.text_rect.collidepoint(mouse):
        #     self.text_rect.color = (200, 200, 200)
        # else:
        #     self.text_rect.color = (255, 255, 255)
        self.detect_action(mouse)

    def draw(self, surface):
        surface.blit(self.text_surface, self.text_rect)


class PlayButton(Button):
    def __init__(self, menu, y):
        super().__init__(menu, y, 'play')

    def detect_action(self, pos):
        if self.text_rect.collidepoint(pos) and pygame.mouse.get_pressed()[0] == 1:
            self.menu.running = False
            self.menu.game.running = True


class ExitButton(Button):
    def __init__(self, menu, y):
        super().__init__(menu, y, 'exit')

    def detect_action(self, pos):
        if self.text_rect.collidepoint(pos) and pygame.mouse.get_pressed()[0] == 1:
            self.menu.game.running = False
            self.menu.running = False


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

    def input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_ESCAPE]:
            self.game.running = False

    def update(self):
        self.play_button.update()
        self.exit_button.update()

    def draw(self):
        # Darken background
        s = pygame.Surface(utils.SCREEN_SIZE)
        s.set_alpha(128)
        s.fill((0, 0, 0))
        self.game.screen.blit(s, (0, 0))

        # Draw buttons
        self.play_button.draw(self.game.screen)
        self.exit_button.draw(self.game.screen)

    def show(self):
        while self.running:
            self.input()
            self.update()
            self.draw()
            self.play_button.detect_action(pygame.mouse.get_pos())
            self.game.clock.tick(self.game.fps)
            self.game.display.blit(self.game.screen, (0, 0))
            pygame.display.flip()
