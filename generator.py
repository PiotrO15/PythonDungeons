import numpy as np
import random
from enum import Enum


# Enum for all the directions
class Direction(Enum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3


class Room:
    def __init__(self):
        self.end = False
        self.neighbors = []


def generate_dungeon(dungeon_size, room_count):
    grid = np.zeros((dungeon_size, dungeon_size), dtype=Room)
    rooms = 0
    x = int(dungeon_size / 2)
    y = dungeon_size - 1

    direction_map = {Direction.UP: (0, 1), Direction.RIGHT: (1, 0), Direction.DOWN: (0, -1), Direction.LEFT: (-1, 0)}

    while rooms < room_count:
        if grid[x, y] == 0:
            grid[x, y] = Room()
            rooms += 1

            if rooms == room_count:
                grid[x, y].end = True

        direction = random.choice(list(direction_map.values()))
        new_x, new_y = x + direction[0], y + direction[1]

        if 0 <= new_x < dungeon_size and 0 <= new_y < dungeon_size and rooms < room_count:
            if not grid[new_x, new_y]:
                if direction == (0, 1):  # Up
                    grid[x, y].neighbors.append(Direction.UP)
                elif direction == (1, 0):  # Right
                    grid[x, y].neighbors.append(Direction.RIGHT)
                elif direction == (0, -1):  # Down
                    grid[x, y].neighbors.append(Direction.DOWN)
                elif direction == (-1, 0):  # Left
                    grid[x, y].neighbors.append(Direction.LEFT)

                x, y = new_x, new_y
            else:
                free = False
                for direction in list(direction_map.values()):
                    new_x, new_y = x + direction[0], y + direction[1]
                    if 0 <= new_x < dungeon_size and 0 <= new_y < dungeon_size:
                        if not grid[new_x, new_y]:
                            free = True
                            break
                if not free:
                    grid = np.zeros((dungeon_size, dungeon_size), dtype=Room)
                    rooms = 0
                    x = int(dungeon_size / 2)
                    y = dungeon_size - 1

    return grid
