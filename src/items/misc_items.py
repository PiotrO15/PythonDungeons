import random

import pygame

from src.items.item import Item
from src.utils import TILE_SIZE


class Shield(Item):
    def __init__(self, game, position=None):
        Item.__init__(self, game, 'shield', (TILE_SIZE, TILE_SIZE), position=position)
        self.open = False
        self.solid = True

    def interact(self):
        self.game.player.shield += 1
        self.game.current_room.item_list.remove(self)


class PotionHPSmall(Item):
    name = 'hp_potion_s'
    def __init__(self, game, position=None):
        Item.__init__(self, game, self.name, (TILE_SIZE, TILE_SIZE), position=position)
        self.open = False
        self.solid = True

    def interact(self):
        self.game.player.hp = min(self.game.player.hp + 10, self.game.player.max_hp)
        self.game.current_room.item_list.remove(self)


class PotionHPLarge(Item):
    name = 'hp_potion_l'

    def __init__(self, game, position=None):
        Item.__init__(self, game, self.name, (TILE_SIZE, TILE_SIZE), position=position)
        self.open = False
        self.solid = True

    def interact(self):
        self.game.player.hp = min(self.game.player.hp + 30, self.game.player.max_hp)
        self.game.current_room.item_list.remove(self)

