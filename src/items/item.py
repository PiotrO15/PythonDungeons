import random

import pygame

from src.utils import get_mask_rect
from src.utils import TILE_SIZE

class Item:
    def __init__(self, game, name, size=None, position=None):
        self.game = game
        self.name = name
        self.size = size
        self.image = None
        self.path = f'..\\assets\\objects\\{self.name}.png'
        self.load_image()
        self.rect = self.image.get_rect()
        self.update_hitbox()
        if position:
            self.rect.x, self.rect.y = position
        self.interaction = False

    def __repr__(self):
        return self.name

    def __str__(self):
        return f'{id(self)}, {self.name}'

    def load_image(self):
        size = self.size if self.size else (TILE_SIZE, TILE_SIZE)
        self.image = pygame.transform.scale(pygame.image.load(self.path).convert_alpha(), self.size)

    def update_hitbox(self):
        self.hitbox = get_mask_rect(self.image, *self.rect.topleft)
        self.hitbox.midbottom = self.rect.midbottom

    def detect_collision(self):
        if self.game.player.hitbox.colliderect(self.rect) and self.game.player.interaction:
            self.interaction = True
        else:
            self.interaction = False

    def update(self):
        pass

    def interact(self):
        pass

    def draw(self):
        surface = self.game.screen
        surface.blit(self.image, (self.rect.x, self.rect.y))
