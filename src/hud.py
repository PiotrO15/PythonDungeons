import pygame
import src.utils as utils
from math import ceil

assets_path = '..\\assets\\hud'

starting_position = (15, 10)

class HealthBar:
    hp_per_cell = 10

    cell_height = 20
    cell_width = 10
    margin = 5

    def __init__(self, player, game):
        self.game = game
        self.cell = None
        self.start = None
        self.end = None
        self.path = f'{assets_path}/health_bar'
        self.load_images()
        self.player = player

        self.max_hp_color = (98, 35, 47)
        self.hp_color = (217, 78, 56)

    def load_images(self):
        self.cell = pygame.image.load(f'{self.path}/cell.png').convert_alpha()
        self.start = pygame.image.load(f'{self.path}/start.png').convert_alpha()
        self.end = pygame.image.load(f'{self.path}/end.png').convert_alpha()

    def draw_health_rectangle(self):
        current_hp = self.player.hp
        max_hp = self.player.max_hp

        max_cells = max_hp / self.hp_per_cell

        # draw empty bar
        position = utils.add_tuples((25, 15), starting_position)
        pygame.draw.rect(self.game.screen, self.max_hp_color, (position[0], position[1], max_cells * self.cell_width * (1 + self.margin / self.cell_width), self.cell_height))
        n_of_cells = int(current_hp // self.hp_per_cell)
        end_position = None

        # draw the full cells
        for i in range(n_of_cells):
            position = (25 + i * (self.cell_width + self.margin), 15)
            position = utils.add_tuples(position, starting_position)

            pygame.draw.rect(self.game.screen, self.hp_color,
                             (position[0], position[1], self.cell_width, self.cell_height))
            end_position = (25 + i * (self.cell_width + self.margin) + 15)
        if end_position:
            pygame.draw.rect(self.game.screen, self.hp_color,
                             (end_position, 15, current_hp % self.hp_per_cell, self.cell_height))

    def draw_container(self):
        position = None
        self.game.screen.blit(self.start, starting_position)
        for i in range(self.player.max_hp // self.hp_per_cell):
            position = (i * (self.cell_width + self.margin) + 40, 0)
            position = utils.add_tuples(position, starting_position)
            self.game.screen.blit(self.cell, position)
        self.game.screen.blit(self.end, position)

    def draw_text(self):
        text_hp = f'HP: {self.player.hp}/{self.player.max_hp}'
        text_surface = pygame.font.Font(utils.font, 20).render(text_hp, True, (255, 255, 255))
        position = ((self.player.max_hp // self.hp_per_cell) * (self.cell_width + self.margin) + 60, 15)
        position = utils.add_tuples(position, starting_position)
        self.game.screen.blit(text_surface, position)

    def draw(self):
        self.draw_health_rectangle()
        self.draw_container()
        self.draw_text()


class Stat:
    def __init__(self, player):
        self.image_size = (24, 24)
        self.image_path = f'{assets_path}\\coin.png'
        self.image = None
        self.load_image()
        self.player = player
        self.text = None
        self.image_position = (0, 50)
        self.text_position = (25, 55)

    def load_image(self):
        self.image = pygame.transform.scale(pygame.image.load(self.image_path).convert_alpha(), self.image_size)

    def update(self):
        pass

    def draw(self, surface):
        self.update()
        surface.blit(self.image, utils.add_tuples(self.image_position, starting_position))
        text_surface = pygame.font.Font(utils.font, 24).render(self.text, True, (255, 255, 255))
        surface.blit(text_surface, utils.add_tuples(self.text_position, starting_position))


class PlayerGold(Stat):
    def __init__(self, player):
        super().__init__(player)
        self.image_path = f'{assets_path}\\coin.png'
        self.load_image()
        self.image_position = (0, 50)
        self.text_position = (25, 55)

    def update(self):
        self.text = f' {self.player.gold}'


class PlayerShield(Stat):
    name = 'armor'

    def __init__(self, player):
        super().__init__(player)
        self.image_path = f'{assets_path}\\shield.png'
        self.load_image()
        self.image_position = (0, 80)
        self.text_position = (25, 85)

    def update(self):
        self.text = f' {self.player.shield}'


class PlayerAttack(Stat):
    name = 'attack'

    def __init__(self, player):
        super().__init__(player)
        self.image_path = f'{assets_path}\\attack.png'
        self.load_image()
        self.image_position = (0, 110)
        self.text_position = (25, 115)

    def update(self):
        self.text = f' {round(self.player.strength, 2)}'


class Hud:
    def __init__(self, game):
        self.game = game

        self.player = self.game.player
        self.gold = PlayerGold(self.game.player)
        self.shield = PlayerShield(self.game.player)
        self.attack = PlayerAttack(self.game.player)
        self.health_bar = HealthBar(self.game.player, game)

    def draw_info(self):
        text_level = f'LEVEL: {int(self.game.level)}'
        level_surface = pygame.font.Font(utils.font, 20).render(text_level, True, (255, 255, 255))
        level_rect = level_surface.get_rect(center=(utils.SCREEN_SIZE[0] / 2, 20))
        self.game.screen.blit(level_surface, level_rect)

        self.health_bar.draw()

        self.gold.draw(self.game.screen)
        self.shield.draw(self.game.screen)
        self.attack.draw(self.game.screen)

    def draw(self):
        self.draw_info()
