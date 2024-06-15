import pygame
import random
from .entity import Entity
from src.utils import time_passed
from .. import utils


def draw_health_bar(surface, pos, size, hp_percentage):
    border_c = (1, 0, 0)
    back_c = (98, 35, 47)

    # color based on hp percentage
    bar_c = (117, 178, 56)
    if hp_percentage < 0.5 :
        bar_c = (217, 178, 56)
        if hp_percentage < 0.25:
            bar_c = (217, 78, 56)

    pygame.draw.rect(surface, back_c, (*pos, *size))
    pygame.draw.rect(surface, border_c, (*pos, *size), 1)
    inner_pos = (pos[0] + 1, pos[1] + 1)
    inner_size = ((size[0] - 2) * hp_percentage, size[1] - 2)
    rect = (round(inner_pos[0]), round(inner_pos[1]), round(inner_size[0]), round(inner_size[1]))
    pygame.draw.rect(surface, bar_c, rect)


class Enemy(Entity):
    def __init__(self, game, max_hp, room, name):
        Entity.__init__(self, game, name)
        self.max_hp = max_hp
        self.hp = self.max_hp
        self.room = room
        self.move_time = 0
        self.attack_cooldown = 0

        self.destination_position = None

    def generate_drops(self):
        pass
        # for _ in range(random.randint(5, 10)):
        #     #self.items.append(Coin())
        # if random.randint(1, 100) == 1:  # 1/100 chance
        #     #self.items.append(Item())

    def drop_items(self):
        self.game.player.gold += random.randint(5, 10)
        # self.generate_drops()

    def spawn(self):
        room_size_px = (self.room.size[0] * utils.ROOM_DIMENSIONS[0] * utils.TILE_SIZE,
                        self.room.size[1] * utils.ROOM_DIMENSIONS[1] * utils.TILE_SIZE)
        top_left_corner = [(a - b) / 2 for a, b in zip(utils.SCREEN_SIZE, room_size_px)]

        self.rect.x = top_left_corner[0] + random.randint(100,  room_size_px[0] - 100)
        self.rect.y = top_left_corner[1] + random.randint(100,  room_size_px[1] - 100)

    def can_attack(self):
        if time_passed(self.attack_cooldown, 1000):
            self.attack_cooldown = pygame.time.get_ticks()
            return True

    def attack_player(self, player):
        if self.hitbox.colliderect(player.hitbox) and self.can_attack():
            player.calculate_collision(self)

    def update(self):
        self.basic_update()
        if not self.dead:
            self.change_speed()
            self.wall_collision()
            self.move()
            self.attack_player(self.game.player)

    def change_speed(self):  # changes speed every 1.5s
        if time_passed(self.move_time, 100):
            self.move_time = pygame.time.get_ticks()
            self.speed = random.randint(100, 200)
            return True

    def move(self):
        if not self.dead and self.hp > 0 and self.can_move and not self.game.player.dead:
            if self.hp < self.max_hp / 10:
                self.move_away_from_player(radius=100)
            else:
                self.move_towards_player()
        else:
            self.velocity = [0, 0]

    def move_towards_player(self):
        dt = self.game.dt
        dir_vector = pygame.math.Vector2(self.game.player.hitbox.x - self.hitbox.x,
                                         self.game.player.hitbox.y - self.hitbox.y)
        if dir_vector.length != 0:
            dir_vector.normalize_ip()
            dir_vector.scale_to_length(self.speed * dt)
        self.set_velocity(dir_vector)

    def move_away_from_player(self, radius):
        dt = self.game.dt
        distance_to_player = pygame.math.Vector2(self.game.player.hitbox.x - self.hitbox.x,
                                                 self.game.player.hitbox.y - self.hitbox.y).length()
        if self.destination_position:
            vector = pygame.math.Vector2(self.game.player.hitbox.x - self.destination_position[0],
                                         self.game.player.hitbox.y - self.destination_position[1]).length()
            if vector < radius:
                self.pick_random_spot()
        if distance_to_player < radius:
            if not self.destination_position:
                self.pick_random_spot()
            dir_vector = pygame.math.Vector2(self.destination_position[0] - self.hitbox.x,
                                             self.destination_position[1] - self.hitbox.y)
            if dir_vector.length_squared() > 0:
                dir_vector.normalize_ip()
                dir_vector.scale_to_length(self.speed * dt)
                self.set_velocity(dir_vector)
            else:
                self.pick_random_spot()
        else:
            self.set_velocity([0, 0])

    def pick_random_spot(self):
        room_size_px = (self.room.size[0] * utils.ROOM_DIMENSIONS[0] * utils.TILE_SIZE,
                        self.room.size[1] * utils.ROOM_DIMENSIONS[1] * utils.TILE_SIZE)
        top_left_corner = [(a - b) / 2 for a, b in zip(utils.SCREEN_SIZE, room_size_px)]

        vector = pygame.math.Vector2(0, 0)

        while vector.length() < 100:
            pick = [top_left_corner[0] + random.randint(100, room_size_px[0] - 100),
                    top_left_corner[1] + random.randint(100, room_size_px[1] - 100)]

            vector = pygame.math.Vector2(self.game.player.hitbox.x - pick[0],
                                         self.game.player.hitbox.y - pick[1])

            self.destination_position = pick


    def draw_health(self, surf):
        if self.hp < self.max_hp:
            health_rect = pygame.Rect(0, 0, 30, 8)
            health_rect.midbottom = self.rect.centerx, self.rect.top
            health_rect.midbottom = self.rect.centerx, self.rect.top

            draw_health_bar(surf, health_rect.topleft, health_rect.size, self.hp/self.max_hp)

    def draw(self):
        if self.dead:
            return
        self.game.screen.blit(self.image, self.rect)
        self.draw_health(self.game.screen)


class EnemyT1(Enemy):
    name = 'e1'
    damage = 13
    speed = 300

    def __init__(self, game, max_hp, room):
        Enemy.__init__(self, game, max_hp, room, self.name)
