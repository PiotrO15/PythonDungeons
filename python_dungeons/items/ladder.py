from python_dungeons.items.item import Item
from python_dungeons.utils import TILE_SIZE


class Ladder(Item):
    def __init__(self, game, position=None):
        Item.__init__(self, game, 'ladder', (TILE_SIZE, TILE_SIZE), position=position)

    def interact(self):
        self.game.next_level()
