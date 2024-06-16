from typing import Tuple

import numpy as np
import random
from enum import Enum
import typing

import pygame

from src.utils import TILE_SIZE
from src import utils


# Enum for all the directions
class Direction(Enum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3

    def is_vertical(self):
        return self == Direction.UP or self == Direction.DOWN

    def opposite(self):
        return Direction((self.value + 2) % 4)


# Dictionary for all the directions
direction_dict = {
    Direction.UP: (0, -1),
    Direction.RIGHT: (1, 0),
    Direction.DOWN: (0, 1),
    Direction.LEFT: (-1, 0)
}

valid_sizes = [(1, 2), (2, 1), (1, 3), (3, 1), (2, 2)]


class Neighbor:
    position: tuple[int, int]
    direction: Direction

    def __init__(self, position, direction):
        self.position = position
        self.direction = direction

class Door:
    def __init__(self, room, neighbor):
        self.room = room
        self.position = neighbor.position
        self.direction = neighbor.direction
        self.destination = utils.add_tuples(neighbor.position, direction_dict[neighbor.direction])
        self.coords = self.coords_in_room()
        self.rect = self.make_rect()

    def make_rect(self):
        room_size_px = (self.room.size[0] * utils.ROOM_DIMENSIONS[0] * TILE_SIZE, self.room.size[1] * utils.ROOM_DIMENSIONS[1] * TILE_SIZE)
        top_left_corner = [(a - b) / 2 for a, b in zip(utils.SCREEN_SIZE, room_size_px)]

        y, x = self.coords
        rect = pygame.Rect(top_left_corner[0] + x * TILE_SIZE, top_left_corner[1] + y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
        return rect

    def coords_in_room(self):
        door_cords = (0, 0)

        offset_x = self.position[0] - self.room.position[0]
        offset_y = self.position[1] - self.room.position[1]

        if self.direction == Direction.UP:
            door_cords = (0, int((offset_x + 0.5) * utils.ROOM_DIMENSIONS[0]))
        elif self.direction == Direction.DOWN:
            door_cords = (len(self.room.layout) - 1, int((offset_x + 0.5) * utils.ROOM_DIMENSIONS[0]))
        elif self.direction == Direction.LEFT:
            door_cords = (int((offset_y + 0.5) * utils.ROOM_DIMENSIONS[1]), 0)
        elif self.direction == Direction.RIGHT:
            door_cords = (int((offset_y + 0.5) * utils.ROOM_DIMENSIONS[1]), len(self.room.layout[0]) - 1)

        #self.room.layout[door_cords[0]][door_cords[1]] = 11

        return door_cords

class Room:
    position: Tuple[int, int]
    size: tuple[int, int]
    end: bool
    neighbors: list[Neighbor]
    master: typing.Optional[Tuple[int, int]]
    merged_with: list

    def __init__(self, x, y):
        self.position = (x, y)
        self.size = (1, 1)
        self.end = False
        self.neighbors = []
        self.doors = []
        self.enemy_list = []
        self.item_list = []
        self.master = None
        self.merged_with = []
        self.layout = []
        self.seed = random.randint(0, 1000000)

    def make_empty_layout(self):
        dimensions = [a * b for a, b in zip(self.size, utils.ROOM_DIMENSIONS)]
        room_layout = np.ones((dimensions[1], dimensions[0]))
        # room_layout = np.ones(dimensions)
        room_layout[1:-1, 1:-1] = 0

        self.layout = room_layout
        return room_layout

    def add_doors(self):
        for neighbor in self.neighbors:
            door = Door(self, neighbor)
            self.doors.append(door)

    def merge_with(self, room, direction):
        self.merged_with.append(room)
        room.master = self.position

        self.neighbors = [n for n in self.neighbors if not n.direction == direction]
        room.neighbors = [n for n in room.neighbors if not n.direction == direction.opposite()]
        self.neighbors.extend(room.neighbors)
        room.neighbors = []


def find_missing_neighbors(grid, dungeon_size, x, y):
    missing_neighbors = []

    for direction in list(direction_dict.values()):
        new_x, new_y = x + direction[0], y + direction[1]
        if 0 <= new_x < dungeon_size and 0 <= new_y < dungeon_size:
            if not grid[new_x, new_y]:
                missing_neighbors.append((x, y, direction))

    return missing_neighbors


def connect_rooms(first_room, second_room, direction_vector):
    # Find corresponding directions for the vector
    for direction in list(direction_dict.keys()):
        if direction_vector == direction_dict.get(direction):
            # Add neighbors to the rooms
            first_room.neighbors.append(Neighbor(first_room.position, direction))
            second_room.neighbors.append(Neighbor(second_room.position, direction.opposite()))


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
        for neighbor in list(room.neighbors):
            if previous_room is None or (x + direction_dict.get(neighbor.direction)[0],
                                         y + direction_dict.get(neighbor.direction)[1]) != previous_room.position:
                direction_vector = direction_dict.get(neighbor.direction)
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


def get_master(room, grid):
    return room if room.master is None else get_master(grid[room.master[0], room.master[1]], grid)


def merge_rooms(grid, dungeon_size, max_merges, max_merge_attempts):
    merges = 0
    merge_attempts = 0

    while merges < max_merges and merge_attempts < max_merge_attempts:
        merge_attempts += 1
        # Select a random room
        room = grid[random.randint(0, dungeon_size - 1), random.randint(0, dungeon_size - 1)]
        room = get_master(room, grid)

        if len(room.neighbors) == 0:
            continue

        # Select a random neighboring room
        direction = random.choice(room.neighbors).direction
        direction_vector = direction_dict.get(direction)

        new_x, new_y = room.position[0] + direction_vector[0], room.position[1] + direction_vector[1]
        if 0 <= new_x < dungeon_size and 0 <= new_y < dungeon_size:
            new_room = grid[new_x, new_y]
            new_room = get_master(new_room, grid)

            # Always select the room with the smallest position as the master
            if room.position[0] > new_x or room.position[1] > new_y:
                room, new_room = new_room, room
                swapped = True
            else:
                swapped = False

            if not new_room.end and not room.end:
                # Check if the rooms can be merged
                if direction.is_vertical() and room.size[0] == new_room.size[0] and room.position[0] == new_room.position[0]:
                    new_size = (room.size[0], room.size[1] + new_room.size[1])
                elif not direction.is_vertical() and room.size[1] == new_room.size[1] and room.position[1] == new_room.position[1]:
                    new_size = (room.size[0] + new_room.size[0], room.size[1])
                else:
                    continue

                # Merge rooms if the new size is valid
                if new_size in valid_sizes:
                    if swapped:
                        room.merge_with(new_room, direction.opposite())
                    else:
                        room.merge_with(new_room, direction)
                    merges += 1
                    room.size = new_size
                    new_room.size = new_size


def fill_rooms(grid):
    for x in range(len(grid)):
        for y in range(len(grid)):
            room = grid[x, y]
            if room.master is None:
                room.make_empty_layout()
                room.add_doors()


def generate_dungeon(dungeon_size, room_count):
    # Generate the main path
    grid = generate_main_path(dungeon_size, room_count)

    # Add missing rooms
    add_missing_rooms(grid, dungeon_size)

    # Merge rooms
    merge_rooms(grid, dungeon_size, 10, 100)

    fill_rooms(grid)

    return grid
