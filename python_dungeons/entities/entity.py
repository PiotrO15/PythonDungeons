import pygame
import python_dungeons.utils as utils
from python_dungeons.utils import get_mask_rect
import math


class Entity:
    max_hp = 1000
    def_speed = 100
    speed = 0

    def __init__(self, game, name, frames=1):
        self.hp = self.max_hp
        self.game = game
        self.name = name
        self.path = f'assets\\entities\\{self.name}'
        self.image = []
        for frame in range(frames):
            self.image.append(pygame.transform.scale(pygame.image.load(f'{self.path}\\idle_{frame + 1}.png'),
                                                     utils.basic_entity_size).convert_alpha())
        self.rect = self.image[0].get_rect()
        self.hitbox = get_mask_rect(self.image[0], *self.rect.topleft)
        self.velocity = [0, 0]
        self.hurt = False
        self.dead = False
        # self.direction = 'right'
        self.can_move = True
        self.can_get_hurt = True

    def __repr__(self):
        return self.name

    def __str__(self):
        return f'{id(self)}, {self.name}'

    def update_hitbox(self):
        self.hitbox = get_mask_rect(self.image[0], *self.rect.topleft)
        self.hitbox.midbottom = self.rect.midbottom

    def moving(self):
        return self.velocity[0] != 0 or self.velocity[1] != 0

    def set_velocity(self, new_velocity):
        self.velocity = new_velocity

    def drop_items(self):
        pass

    def detect_death(self):
        if self.hp <= 0 and self.dead is False:
            self.dead = True
            self.can_move = False
            self.velocity = [0, 0]

            self.drop_items()

    def basic_update(self):
        self.detect_death()
        self.rect.move_ip(self.velocity)
        self.hitbox.move_ip(self.velocity)
        self.update_hitbox()
        self.check_collisions()

    def check_collisions(self):
        new_pos_rect = self.hitbox.move(*self.velocity)  # Position after moving

        room = self.game.current_room
        room_size_px = (room.size[0] * utils.ROOM_DIMENSIONS[0] * utils.TILE_SIZE,
                        room.size[1] * utils.ROOM_DIMENSIONS[1] * utils.TILE_SIZE)
        top_left_corner = [(a - b) / 2 for a, b in zip(utils.SCREEN_SIZE, room_size_px)]

        # Allow movement if the player touches a door
        for door in room.doors:
            if door.rect.colliderect(new_pos_rect):
                try:
                    self.use_door(door)
                except:
                    pass

        for item in room.item_list:
            # if item.rect.colliderect(new_pos_rect):
            #     self.velocity = [0, 0]
            if item.solid:
                collide_points = (
                new_pos_rect.midbottom, new_pos_rect.bottomleft, new_pos_rect.bottomright, new_pos_rect.midleft,
                new_pos_rect.midright, new_pos_rect.center)
                if any(item.hitbox.collidepoint(point) for point in collide_points):
                    self.velocity = [0, 0]

        if (new_pos_rect.left < top_left_corner[0] + utils.TILE_SIZE
                or new_pos_rect.right > top_left_corner[0] + room.size[0] * utils.ROOM_DIMENSIONS[
                    0] * utils.TILE_SIZE - utils.TILE_SIZE
                or new_pos_rect.top < top_left_corner[1] + utils.TILE_SIZE
                or new_pos_rect.bottom > top_left_corner[1] + room.size[1] * utils.ROOM_DIMENSIONS[
                    1] * utils.TILE_SIZE - utils.TILE_SIZE):
            self.velocity = [0, 0]

    def draw(self):
        if self.dead:
            return
        frames = len(self.image)
        # Divide 1000 ticks into frames
        frame = math.floor((pygame.time.get_ticks() % 1000) / (1000 / frames))
        image = self.image[frame]
        self.game.screen.blit(image, self.rect)
