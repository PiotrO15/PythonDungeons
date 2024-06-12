
import pygame
import src.utils as utils
from src.utils import get_mask_rect

class Entity:
    def __init__(self, game, name):
        self.hp = 1000
        self.game = game
        self.name = name
        self.path = f'../assets/entities/{self.name}'
        self.image = pygame.transform.scale(pygame.image.load(f'{self.path}/idle.png'),
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
        test_rect = self.hitbox.move(*self.velocity)  # Position after moving, change name later
        collide_points = (test_rect.midbottom, test_rect.bottomleft, test_rect.bottomright, test_rect.center, test_rect.midleft, test_rect.midright)

        #  if any(wall.hitbox.collidepoint(point) for point in collide_points):
        #         self.velocity = [0, 0]

        screen_surface = self.game.display
        try:
            if any(screen_surface.get_at(point) in [(0,0,0), (30, 50, 50)] for point in collide_points):
                self.velocity = [0, 0]
        except: self.velocity = [0, 0]

    def update_hitbox(self):
        self.hitbox = get_mask_rect(self.image, *self.rect.topleft)
        self.hitbox.midbottom = self.rect.midbottom

    def moving(self):
        return self.velocity[0] != 0 or self.velocity[1] != 0
