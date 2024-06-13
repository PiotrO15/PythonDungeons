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
        self.master = None
        self.merged_with = []

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


def connect_rooms(first_room, second_room, direction):
    if direction == (0, -1):  # Up
        first_room.neighbors.append(Neighbor(first_room.position, Direction.UP))
        second_room.neighbors.append(Neighbor(second_room.position, Direction.DOWN))
    elif direction == (1, 0):  # Right
        first_room.neighbors.append(Neighbor(first_room.position, Direction.RIGHT))
        second_room.neighbors.append(Neighbor(second_room.position, Direction.LEFT))
    elif direction == (0, 1):  # Down
        first_room.neighbors.append(Neighbor(first_room.position, Direction.DOWN))
        second_room.neighbors.append(Neighbor(second_room.position, Direction.UP))
    elif direction == (-1, 0):  # Left
        first_room.neighbors.append(Neighbor(first_room.position, Direction.LEFT))
        second_room.neighbors.append(Neighbor(second_room.position, Direction.RIGHT))


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
            if previous_room is None or (x + direction_dict.get(neighbor.direction)[0], y + direction_dict.get(neighbor.direction)[1]) != previous_room.position:
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
    if room.master is None:
        return room
    else:
        return get_master(grid[room.master[0], room.master[1]], grid)


def generate_dungeon(dungeon_size, room_count):
    # Generate the main path
    grid = generate_main_path(dungeon_size, room_count)

    # Add missing rooms
    add_missing_rooms(grid, dungeon_size)

    # Merge rooms
    max_merges = 10
    merges = 0
    merge_attempts = 0
    max_merge_attempts = 100

    while merges < max_merges and merge_attempts < max_merge_attempts:
        merge_attempts += 1
        room = grid[random.randint(0, dungeon_size - 1), random.randint(0, dungeon_size - 1)]
        room = get_master(room, grid)

        swapped = False

        if len(room.neighbors) >= 1:
            direction = random.choice(room.neighbors).direction
            direction_vector = direction_dict.get(direction)
            new_x, new_y = room.position[0] + direction_vector[0], room.position[1] + direction_vector[1]
            if 0 <= new_x < dungeon_size and 0 <= new_y < dungeon_size:
                new_room = grid[new_x, new_y]
                new_room = get_master(new_room, grid)
                if room.position[0] > new_x or room.position[1] > new_y:
                    room, new_room = new_room, room
                    swapped = True

                if new_room.master is None and not new_room.end and not room.end:
                    # Calculate new size considering positions and sizes of both rooms
                    if (direction.is_vertical() and room.size[0] == new_room.size[0] and new_room.position[0] == room.position[0] or
                            not direction.is_vertical() and room.size[1] == new_room.size[1] and new_room.position[1] == room.position[1]):
                        if direction.is_vertical():
                            new_size = (room.size[0], room.size[1] + new_room.size[1])
                        else:
                            new_size = (room.size[0] + new_room.size[0], room.size[1])
                        if new_size in valid_sizes:
                            if swapped:
                                room.merge_with(new_room, direction.opposite())
                            else:
                                room.merge_with(new_room, direction)
                            merges += 1
                            room.size = new_size
                            new_room.size = new_size
    #
    #                             print(f"Merged room {room.position} with room {new_room.position} to size {room.size}")
    #                             #print(f"Room position: {room.position}, size: {room.size}, neighbors: {room.neighbors}, master: {room.master}, merged_with: {room.merged_with}")
    #                             #print(f"New room position: {new_room.position}, size: {new_room.size}, neighbors: {new_room.neighbors}, master: {new_room.master}, merged_with: {new_room.merged_with}")

    return grid
