import pygame

import pygame_test_map
# from .entities.enemy_manager import EnemyManager
from src.entities.player import Player
# from .menu import MainMenu
# from .mini_map import MiniMap
# from .hud import Hud
# from .map.world_manager import WorldManager
# from .objects.object_manager import ObjectManager
# from .game_over import GameOver
import time
pygame.init()
pygame.mixer.init()

world_size = (21 * 64, 14 * 64)

class Game:
    def __init__(self):
        self.display = pygame.display.set_mode(world_size)
        self.screen = pygame.Surface(world_size).convert()
        self.clock = pygame.time.Clock()
        # self.enemy_manager = EnemyManager(self)
        # self.world_manager = WorldManager(self)

        self.dungeon_layout = pygame_test_map.create_room(21, 14)

        # self.object_manager = ObjectManager(self)
        self.player = Player(self)
        # self.hud = Hud(self)
        self.running = True
        # self.menu = MainMenu(self)
        # self.mini_map = MiniMap(self)
        self.game_time = None
        self.fps = 60
        # self.game_over = GameOver(self)
        pygame.mixer.init()
        self.dt = 0
        self.screen_position = (0, 0)



    def refresh(self):
        self.__init__()
        pygame.display.flip()
        self.run_game()

    def update_groups(self):
        # self.enemy_manager.update_enemies()
        # self.object_manager.update()
        self.player.update()
        # self.world_manager.update()
        # self.mini_map.update()

    def draw_groups(self):
        # self.world_manager.draw_map(self.screen)
        pygame_test_map.draw_map(self.dungeon_layout, self.screen)
        if self.player:
            self.player.draw(self.screen)
        #self.enemy_manager.draw_enemies(self.screen)
        #self.object_manager.draw()
        #self.mini_map.draw(self.screen)
        #self.hud.draw()

    def input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        self.player.input()
        pressed = pygame.key.get_pressed()

        if pressed[pygame.K_ESCAPE]:
            pass
            # TODO menu + pause

    def run_game(self):
        # self.enemy_manager.add_enemies()
        prev_time = time.time()
        while self.running:
            self.clock.tick(self.fps)
            now = time.time()
            self.dt = now - prev_time
            prev_time = now
            # self.menu.show()
            self.screen.fill((0, 0, 0))

            self.input()
            self.update_groups()
            self.draw_groups()
            self.game_time = pygame.time.get_ticks()
            self.display.blit(self.screen, self.screen_position)

            if self.running:
                pygame.display.flip()

        pygame.quit()