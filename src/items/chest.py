import random

import pygame

from src.items.item import Item
from src.utils import TILE_SIZE


class Chest(Item):
    def __init__(self, game, position=None):
        Item.__init__(self, game, 'chest', (TILE_SIZE, TILE_SIZE), position=position)
        self.open = False

    def interact(self):
        if not self.open:
            self.open = True
            self.interaction = False

            self.game.player.gold += random.randint(10, 5 * self.game.level)

    def update(self):
        if self.open:
            self.image = pygame.image.load('./assets/objects/chest_empty.png').convert_alpha()
