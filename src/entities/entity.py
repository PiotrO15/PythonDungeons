
import pygame
import src.utils as utils
from src.utils import get_mask_rect

class Entity:
    max_hp = 1000
    def __init__(self, game, name):
        self.hp = self.max_hp/2
        self.game = game
        self.name = name
        self.path = f'..\\assets\\entities\\{self.name}'
        self.image = pygame.transform.scale(pygame.image.load(f'{self.path}\\idle.png'),
                                            utils.basic_entity_size).convert_alpha()
        self.rect = self.image.get_rect()
        self.hitbox = get_mask_rect(self.image, *self.rect.topleft)
        self.velocity = [0, 0]
        self.hurt = False
        self.dead = False
        #self.direction = 'right'
        self.can_move = True
        self.time = 0
        self.can_get_hurt = True

    def __repr__(self):
        return self.name

    def __str__(self):
        return f'{id(self)}, {self.name}'

    def set_velocity(self, new_velocity):
        self.velocity = new_velocity

    def drop_items(self):
        pass

    def detect_death(self):
        if self.hp <= 0 and self.dead is False:
            self.dead = True
            self.can_move = False
            self.velocity = [0, 0]

            # self.drop_items()

    def basic_update(self):
        self.detect_death()
        self.update_hitbox()
        self.rect.move_ip(self.velocity)
        self.hitbox.move_ip(self.velocity)

    def wall_collision(self):
        new_pos_rect = self.hitbox.move(*self.velocity)  # Position after moving, change name later

        room = self.game.current_room
        room_size_px = (room.size[0] * utils.ROOM_DIMENSIONS[0] * utils.TILE_SIZE, room.size[1] * utils.ROOM_DIMENSIONS[1] * utils.TILE_SIZE)
        top_left_corner = [(a - b)/2 for a, b in zip(utils.SCREEN_SIZE, room_size_px)]

        # Allow movement if the player touches a door
        for door in room.doors_rect:
            if door['rect'].colliderect(new_pos_rect):
                return

        if (new_pos_rect.left < top_left_corner[0] + utils.TILE_SIZE
                or new_pos_rect.right > top_left_corner[0] + room.size[0] * utils.ROOM_DIMENSIONS[0] * utils.TILE_SIZE - utils.TILE_SIZE
                or new_pos_rect.top < top_left_corner[1] + utils.TILE_SIZE
                or new_pos_rect.bottom > top_left_corner[1] + room.size[1] * utils.ROOM_DIMENSIONS[1] * utils.TILE_SIZE - utils.TILE_SIZE):
            self.velocity = [0, 0]

    def update_hitbox(self):
        self.hitbox = get_mask_rect(self.image, *self.rect.topleft)
        self.hitbox.midbottom = self.rect.midbottom

    def moving(self):
        return self.velocity[0] != 0 or self.velocity[1] != 0
