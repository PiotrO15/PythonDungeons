import pygame

import generator
from src import utils
from src.map import display_map
from src.entities.enemy_manager import EnemyManager
from src.entities.player import Player
# from .menu import MainMenu
# from .mini_map import MiniMap
from .hud import Hud
# from .objects.object_manager import ObjectManager
# from .game_over import GameOver
import time

pygame.init()
pygame.mixer.init()


class Game:
    def __init__(self):
        self.dungeon = None
        self.current_room = None
        self.display = pygame.display.set_mode(utils.SCREEN_SIZE)
        self.screen = pygame.Surface(utils.SCREEN_SIZE).convert()
        self.clock = pygame.time.Clock()
        self.enemy_manager = EnemyManager(self)
        self.dungeon_size = 5
        self.room_count = 10
        self.level = 0

        self.next_level()

        # self.object_manager = ObjectManager(self)
        self.player = Player(self)
        self.hud = Hud(self)
        self.running = True
        # self.menu = MainMenu(self)
        # self.mini_map = MiniMap(self)
        self.game_time = None
        self.fps = 60
        # self.game_over = GameOver(self)
        pygame.mixer.init()
        self.dt = 0
        self.screen_position = (0, 0)

    def next_level(self):
        self.level += 1
        self.dungeon = generator.generate_dungeon(self.dungeon_size, self.room_count)

        start_x = int(self.dungeon_size / 2)
        start_y = self.dungeon_size - 1
        self.current_room = self.dungeon[start_x, start_y]
        while self.current_room.master: self.current_room = self.dungeon[self.current_room.master]

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
        #self.mini_map.draw(self.screen)
        self.hud.draw()

    def input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        self.player.input()
        pressed = pygame.key.get_pressed()

        if pressed[pygame.K_ESCAPE]:
            pass
            # TODO menu + pause

    def debug(self):
        if pygame.mouse.get_pressed()[2]: # spawn enemies under cursor
            x, y = pygame.mouse.get_pos()
            from src.entities.enemy import EnemyT1
            self.current_room.enemy_list.append(EnemyT1(self, 200, self.current_room))
            #print('spawned enemy')
            self.current_room.enemy_list[-1].rect.topleft = (x, y)
        if pygame.mouse.get_pressed()[0]: # hurt enemies in the room
            x, y = pygame.mouse.get_pos()
            for enemy in self.current_room.enemy_list:
                #print('hurt enemies')
                enemy.hp -= 4

    def run_game(self):
        self.enemy_manager.add_enemies()
        prev_time = time.time()
        while self.running:
            self.clock.tick(self.fps)
            now = time.time()
            self.dt = now - prev_time
            prev_time = now
            # self.menu.show()

            self.debug()

            self.input()
            self.update_groups()
            self.draw_groups()
            self.game_time = pygame.time.get_ticks()
            self.display.blit(self.screen, self.screen_position)

            if self.running:
                pygame.display.flip()

        pygame.quit()
