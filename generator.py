from typing import Tuple

import numpy as np
import random
from enum import Enum
import typing


# Enum for all the directions
class Direction(Enum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3


# Dictionary for all the directions
direction_dict = {
    Direction.UP: (0, -1),
    Direction.RIGHT: (1, 0),
    Direction.DOWN: (0, 1),
    Direction.LEFT: (-1, 0)
}

valid_sizes = [(1, 2), (2, 1), (1, 3), (3, 1), (2, 2)]


def make_empty_room(size):
    default_dimensions = (11, 15)
    dimensions = [a * b for a, b in zip(size, default_dimensions)]
    room_layout = np.ones(dimensions)
    room_layout[1:-1, 1:-1] = 0

    return room_layout

class Room:
    position: Tuple[int, int]
    size: tuple[int, int]
    end: bool
    neighbors: list[Direction]
    master: typing.Optional[Tuple[int, int]]
    merged_with: list
    layout: []

    def __init__(self, x, y):
        self.position = (x, y)
        self.size = (1, 1)

        self.end = False
        self.neighbors = []
        self.master = None
        self.merged_with = []
        self.layout = make_empty_room(self.size)

    def add_doors(self):
        if Direction.UP in self.neighbors: self.layout[0][int(len(self.layout[0]) / 2)] = 11
        if Direction.DOWN in self.neighbors: self.layout[-1][int(len(self.layout[0]) / 2)] = 12
        if Direction.LEFT in self.neighbors: self.layout[int(len(self.layout) / 2)][0] = 13
        if Direction.RIGHT in self.neighbors: self.layout[int(len(self.layout) / 2)][-1] = 14

def find_missing_neighbors(grid, dungeon_size, x, y):
    missing_neighbors = []

    for direction in list(direction_dict.values()):
        new_x, new_y = x + direction[0], y + direction[1]
        if 0 <= new_x < dungeon_size and 0 <= new_y < dungeon_size:
            if not grid[new_x, new_y]:
                missing_neighbors.append((x, y, direction))

    return missing_neighbors


def connect_rooms(first_room, second_room, direction):
    if direction == (0, -1):  # Up
        first_room.neighbors.append(Direction.UP)
        second_room.neighbors.append(Direction.DOWN)
    elif direction == (1, 0):  # Right
        first_room.neighbors.append(Direction.RIGHT)
        second_room.neighbors.append(Direction.LEFT)
    elif direction == (0, 1):  # Down
        first_room.neighbors.append(Direction.DOWN)
        second_room.neighbors.append(Direction.UP)
    elif direction == (-1, 0):  # Left
        first_room.neighbors.append(Direction.LEFT)
        second_room.neighbors.append(Direction.RIGHT)


def generate_main_path(dungeon_size, length):
    start_x = int(dungeon_size / 2)
    start_y = dungeon_size - 1

    while True:
        grid = np.zeros((dungeon_size, dungeon_size), np.dtype(Room))
        x = start_x
        y = start_y

        room = grid[x, y] = Room(x, y)
        rooms = 1

        # Checks if the room is within the bounds of the dungeon
        def is_within_bounds(room_x, room_y):
            return 0 <= room_x < dungeon_size and 0 <= room_y < dungeon_size

        # Generate the main path of the dungeon
        while rooms < length:
            # Select a random direction to go to
            direction = random.choice(list(direction_dict.values()))
            next_x, next_y = x + direction[0], y + direction[1]

            if is_within_bounds(next_x, next_y):
                # Create a new room if there is no room in the next position
                if not grid[next_x, next_y]:
                    next_room = grid[next_x, next_y] = Room(next_x, next_y)
                    rooms += 1

                    # Apply room modifiers
                    if rooms == length:
                        next_room.end = True

                    # Create a door between the rooms
                    connect_rooms(room, next_room, direction)

                    # Move to the next room
                    x, y = next_x, next_y
                    room = next_room

                    if rooms == length:
                        return grid

                else:
                    # Find any possible connections to the next room
                    possible_connections = False
                    for direction in list(direction_dict.values()):
                        next_x, next_y = x + direction[0], y + direction[1]
                        if is_within_bounds(next_x, next_y) and not grid[next_x, next_y]:
                            possible_connections = True
                            break

                    # If there are no possible connections, reset the grid
                    if not possible_connections:
                        break


def add_missing_rooms(grid, dungeon_size):
    # Go through all the rooms and find missing neighbors
    to_visit = [(int(dungeon_size / 2), dungeon_size - 1)]
    missing_neighbors = []
    previous_room = None

    while not grid[to_visit[0][0], to_visit[0][1]].end:
        x, y = to_visit.pop(0)
        room = grid[x, y]
        for direction in list(direction_dict.values()):
            new_x, new_y = x + direction[0], y + direction[1]
            if 0 <= new_x < dungeon_size and 0 <= new_y < dungeon_size:
                if not grid[new_x, new_y]:
                    missing_neighbors.append((x, y, direction))

        # Select the direction vector that doesn't point to the previous room
        for direc in list(room.neighbors):
            if previous_room is None or (x + direction_dict.get(direc)[0], y + direction_dict.get(direc)[1]) != previous_room.position:
                direction_vector = direction_dict.get(direc)
                break

        to_visit.append((x + direction_vector[0], y + direction_vector[1]))

        previous_room = room

    while missing_neighbors:
        for x, y, direction in missing_neighbors:
            new_x, new_y = x + direction[0], y + direction[1]
            if not grid[new_x, new_y]:
                grid[new_x, new_y] = Room(new_x, new_y)
                connect_rooms(grid[x, y], grid[new_x, new_y], direction)

                missing_neighbors += find_missing_neighbors(grid, dungeon_size, new_x, new_y)

            missing_neighbors.remove((x, y, direction))


def generate_dungeon(dungeon_size, room_count):
    # Generate the main path
    grid = generate_main_path(dungeon_size, room_count)

    # Add missing rooms
    add_missing_rooms(grid, dungeon_size)

    # Merge rooms
    max_merges = 10
    merges = 0

    while merges < max_merges:
        room = grid[random.randint(0, dungeon_size - 1), random.randint(0, dungeon_size - 1)]
        while room.master is not None:
            room = grid[room.master[0], room.master[1]]

        if not room.end:
            if len(room.neighbors) >= 1:
                direction = random.choice(room.neighbors)
                direction_vector = direction_dict.get(direction)
                new_x, new_y = room.position[0] + direction_vector[0], room.position[1] + direction_vector[1]
                if 0 <= new_x < dungeon_size and 0 <= new_y < dungeon_size:
                    new_room = grid[new_x, new_y]
                    while new_room.master is not None:
                        new_room = grid[new_room.master[0], new_room.master[1]]
                    if room.position[0] > new_x or room.position[1] > new_y:
                        room, new_room = new_room, room
                        new_x, new_y = new_room.position

                    if new_room.master is None and new_room.merged_with == [] and not new_room.end:
                        # Calculate new size considering positions and sizes of both rooms
                        if (room.position[0] == new_room.position[0] and room.size[0] == new_room.size[0]) or (room.position[1] == new_room.position[1] and room.size[1] == new_room.size[1]):
                            if room.position[0] == new_room.position[0]:
                                new_size = (room.size[0], room.size[1] + new_room.size[1])
                            else:
                                new_size = (room.size[0] + new_room.size[0], room.size[1])
                            if new_size in valid_sizes:
                                new_room.master = room.position
                                room.merged_with.append(grid[new_x, new_y])
                                merges += 1
                                room.size = new_size
                                new_room.size = new_size
    #
    #                             print(f"Merged room {room.position} with room {new_room.position} to size {room.size}")
    #                             #print(f"Room position: {room.position}, size: {room.size}, neighbors: {room.neighbors}, master: {room.master}, merged_with: {room.merged_with}")
    #                             #print(f"New room position: {new_room.position}, size: {new_room.size}, neighbors: {new_room.neighbors}, master: {new_room.master}, merged_with: {new_room.merged_with}")

    return grid
