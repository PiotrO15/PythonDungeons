import numpy as np
import random
from enum import Enum


# Enum for all the directions
class Direction(Enum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3


# Dictionary for all the directions
direction_dict = {
    Direction.UP: (0, 1),
    Direction.RIGHT: (1, 0),
    Direction.DOWN: (0, -1),
    Direction.LEFT: (-1, 0)
}


class Room:
    def __init__(self):
        self.end = False
        self.neighbors = []


def find_missing_neighbors(grid, dungeon_size, x, y):
    missing_neighbors = []

    for direction in list(direction_dict.values()):
        new_x, new_y = x + direction[0], y + direction[1]
        if 0 <= new_x < dungeon_size and 0 <= new_y < dungeon_size:
            if not grid[new_x, new_y]:
                missing_neighbors.append((x, y, direction))

    return missing_neighbors


def find_missing_rooms(grid, dungeon_size, x, y):
    pass


def generate_dungeon(dungeon_size, room_count):
    grid = np.zeros((dungeon_size, dungeon_size), dtype=Room)
    rooms = 0
    x = int(dungeon_size / 2)
    y = dungeon_size - 1

    while rooms < room_count:
        if grid[x, y] == 0:
            grid[x, y] = Room()
            rooms += 1

            if rooms == room_count:
                grid[x, y].end = True

        direction = random.choice(list(direction_dict.values()))
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
                for direction in list(direction_dict.values()):
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

    # Go through all the rooms and find missing neighbors
    to_visit = [(int(dungeon_size / 2), dungeon_size - 1)]
    missing_neighbors = []

    while not grid[to_visit[0][0], to_visit[0][1]].end:
        x, y = to_visit.pop(0)
        room = grid[x, y]
        for direction in list(direction_dict.values()):
            new_x, new_y = x + direction[0], y + direction[1]
            if 0 <= new_x < dungeon_size and 0 <= new_y < dungeon_size:
                if not grid[new_x, new_y]:
                    missing_neighbors.append((x, y, direction))

        direction_vector = direction_dict.get(room.neighbors[0])
        to_visit.append((x + direction_vector[0], y + direction_vector[1]))

    while missing_neighbors:
        for x, y, direction in missing_neighbors:
            new_x, new_y = x + direction[0], y + direction[1]
            if not grid[new_x, new_y]:
                grid[new_x, new_y] = Room()
                grid[x, y].neighbors.append(direction)
                if direction == (0, 1):  # Up
                    grid[x, y].neighbors.append(Direction.UP)
                elif direction == (1, 0):  # Right
                    grid[x, y].neighbors.append(Direction.RIGHT)
                elif direction == (0, -1):  # Down
                    grid[x, y].neighbors.append(Direction.DOWN)
                elif direction == (-1, 0):  # Left
                    grid[x, y].neighbors.append(Direction.LEFT)

                missing_neighbors += find_missing_neighbors(grid, dungeon_size, new_x, new_y)

            missing_neighbors.remove((x, y, direction))


    return grid
