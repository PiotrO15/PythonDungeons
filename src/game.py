import pygame

from src.map import display_map, generator
# from .objects.object_manager import ObjectManager
from src.entities.enemy_manager import EnemyManager
from src.entities.enemy import EnemyT1 # for debug
from src.entities.player import Player
from src.ui.menu import MainMenu
# from .mini_map import MiniMap
from src.ui.hud import Hud
from src.ui.game_over import GameOver
from src import utils

import time

pygame.init()
pygame.mixer.init()

class Game:
    dungeon_size = 5
    room_count = 10
    level = 0
    def __init__(self):
        self.display = pygame.display.set_mode(utils.SCREEN_SIZE)
        self.screen = pygame.Surface(utils.SCREEN_SIZE).convert()

        self.dungeon = None
        self.current_room = None
        # self.mini_map = MiniMap(self)

        self.player = Player(self)
        self.enemy_manager = EnemyManager(self)
        # self.object_manager = ObjectManager(self)

        self.next_level()

        self.running = True
        self.paused = True

        self.hud = Hud(self)
        self.menu = MainMenu(self)
        self.game_over = GameOver(self)

        self.clock = pygame.time.Clock()
        self.fps = 60
        self.dt = 0

    def next_level(self):
        self.level += 1
        self.dungeon = generator.generate_dungeon(self.dungeon_size, self.room_count)

        self.enemy_manager.add_enemies()

        start_x = int(self.dungeon_size / 2)
        start_y = self.dungeon_size - 1
        self.current_room = self.dungeon[start_x, start_y]
        while self.current_room.master: self.current_room = self.dungeon[self.current_room.master]

        self.current_room.enemy_list.clear()

    def refresh(self):
        self.__init__()
        pygame.display.flip()
        self.run_game()

    def update_groups(self):
        self.enemy_manager.update_enemies()
        # self.object_manager.update()
        self.player.update()
        # self.mini_map.update()

    def draw_groups(self):
        display_map.draw_room(self.current_room, self.screen)

        if self.player:
            self.player.draw(self.screen)

        self.enemy_manager.draw_enemies(self.screen)
        #self.object_manager.draw_objects()

        # self.mini_map.draw(self.screen)
        self.hud.draw()
        self.game_over.draw()

    def input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        if not self.paused:
            self.player.input()
            pressed = pygame.key.get_pressed()

            if pressed[pygame.K_ESCAPE]:
                self.menu.running = True
                self.paused = True

    def debug(self):
        # Spawn enemies under cursor
        if pygame.mouse.get_pressed()[2]:
            x, y = pygame.mouse.get_pos()

            self.current_room.enemy_list.append(EnemyT1(self, 150, self.current_room))
            self.current_room.enemy_list[-1].rect.topleft = (x, y)

        # Hurt enemies in the room
        if pygame.mouse.get_pressed()[0]:
            x, y = pygame.mouse.get_pos()
            for enemy in self.current_room.enemy_list:
                enemy.hp -= 4

    def run_game(self):
        prev_time = time.time()

        while self.running:
            self.input()

            self.clock.tick(self.fps)
            now = time.time()
            self.dt = now - prev_time
            prev_time = now

            if self.player.dead:
                self.game_over.show()
            elif not self.paused:
                self.debug()

                self.update_groups()
                self.draw_groups()

                self.display.blit(self.screen, (0,0))
            else:
                self.menu.show()
            pygame.display.flip()

        # game_time = pygame.time.get_ticks()
        pygame.quit()
