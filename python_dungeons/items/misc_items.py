import random

import pygame

from python_dungeons.items.item import Item
from python_dungeons.utils import TILE_SIZE


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

class PotionStrength(Item):
    name = 'strength_potion'

    def __init__(self, game, position=None):
        Item.__init__(self, game, self.name, (TILE_SIZE, TILE_SIZE), position=position)
        self.open = False
        self.solid = True

    def interact(self):
        self.game.player.strength += 0.1
        self.game.current_room.item_list.remove(self)

