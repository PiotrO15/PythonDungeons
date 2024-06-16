import random

from src.items.chest import Chest
from src.utils import ROOM_DIMENSIONS, TILE_SIZE, SCREEN_SIZE

class ItemManager:
    def __init__(self, game):
        self.game = game

    def draw_items(self):
        for item in self.game.current_room.item_list:
            item.draw()

    def update_items(self):
        for item in self.game.current_room.item_list:
            item.update()

    def add_items(self):
        for row in self.game.dungeon:
            for room in row:

                room_size_px = (room.size[0] * ROOM_DIMENSIONS[0] * TILE_SIZE,
                                room.size[1] * ROOM_DIMENSIONS[1] * TILE_SIZE)
                top_left_corner = [(a - b) / 2 for a, b in zip(SCREEN_SIZE, room_size_px)]

                if room.end:
                    ... # TODO spawn ladder

                #spawn chests
                num_of_chests = random.randint(0, 1 + room.size[0] * room.size[1])
                for _ in range(num_of_chests):
                    x = top_left_corner[0] + random.randint(TILE_SIZE, room_size_px[0] - TILE_SIZE)
                    y = top_left_corner[1] + random.randint(TILE_SIZE, room_size_px[1] - TILE_SIZE)

                    chest = Chest(self.game, (x, y))
                    room.item_list.append(chest)
