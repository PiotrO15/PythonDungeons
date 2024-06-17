import random

import pygame

from src.items.item import Item
from src.utils import TILE_SIZE


class Chest(Item):
    def __init__(self, game, position=None):
        Item.__init__(self, game, 'chest', (TILE_SIZE, TILE_SIZE), position=position)
        self.open = False
        self.solid = True

    def interact(self):
        if not self.open:
            self.open_chest()

    def open_chest(self):
        self.open = True
        self.interaction = False

        self.game.player.gold += random.randint(2 * self.game.level, 5 * self.game.level)

        self.image = pygame.transform.scale(pygame.image.load('../assets/objects/chest_empty.png').convert_alpha(),
                                            self.size)
