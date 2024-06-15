import pygame
import generator
import random

from src import utils
from src.utils import TILE_SIZE


def load_tile_set():
    # Splits the tile_set into a 2D array of 16x16 tiles and scales them to TILE_SIZE
    tile_set = []
    tiles = pygame.image.load("..\\assets\\map\\tile_set.png")
    for y in range(0, tiles.get_height(), 16):
        row = []
        for x in range(0, tiles.get_width(), 16):
            tile = pygame.Surface((16, 16), pygame.SRCALPHA, 32)
            tile.blit(tiles, (0, 0), (x, y, 16, 16))  # Copy the corresponding part of the tile set image
            tile = pygame.transform.scale(tile, (TILE_SIZE, TILE_SIZE))  # Scale the tile
            row.append(tile)
        tile_set.append(row)

    return tile_set


map_tile_set = load_tile_set()


def choose_rotation(position, room, up, right, down, left, corners=None):
    if corners is None:
        corners = []

    is_up = (position[0] == 0)
    is_right = (position[1] == (room.size[0] * utils.ROOM_DIMENSIONS[0] - 1))
    is_down = (position[0] == (room.size[1] * utils.ROOM_DIMENSIONS[1] - 1))
    is_left = (position[1] == 0)

    rotation_map = {
        (True, False, False, False): up,  # Up
        (False, True, False, False): right,  # Right
        (False, False, True, False): down,  # Down
        (False, False, False, True): left,  # Left
    }

    if corners:
        corner_map = {
            (True, False, False, True): corners[0],  # Upper Left
            (True, True, False, False): corners[1],  # Upper Right
            (False, False, True, True): corners[2],  # Bottom Left
            (False, True, True, False): corners[3],  # Bottom Right
        }
        rotation_map.update(corner_map)

    return rotation_map[(is_up, is_right, is_down, is_left)]


def draw_room(room: generator.Room, screen):
    room_size_px = (room.size[0] * utils.ROOM_DIMENSIONS[0] * TILE_SIZE, room.size[1] * utils.ROOM_DIMENSIONS[1] * TILE_SIZE)
    top_left_corner = [(a - b)/2 for a, b in zip(utils.SCREEN_SIZE, room_size_px)]

    # Clear the screen
    screen.fill(utils.BACKGROUND_COLOR)
    random.seed(room.seed)

    # Draw the dungeon
    for y, row in enumerate(room.layout):
        for x, tile in enumerate(row):
            rect = pygame.Rect(top_left_corner[0] + x * TILE_SIZE, top_left_corner[1] + y * TILE_SIZE, TILE_SIZE, TILE_SIZE)

            # Draw floor
            if tile == 0:
                # Get random tile set from [0][6] to [2][9]
                random_tile = map_tile_set[random.randint(0, 2)][random.randint(6, 9)]

                screen.blit(random_tile, (top_left_corner[0] + x * TILE_SIZE, top_left_corner[1] + y * TILE_SIZE))

            # Draw walls
            if tile == 1:
                up = map_tile_set[0][random.randint(1, 4)]
                right = map_tile_set[random.randint(1, 3)][5]
                down = map_tile_set[4][random.randint(1, 4)]
                left = map_tile_set[random.randint(1, 3)][0]
                upper_left = map_tile_set[0][0]
                upper_right = map_tile_set[0][5]
                bottom_left = map_tile_set[4][0]
                bottom_right = map_tile_set[4][5]
                screen.blit(choose_rotation((y, x), room, up, right, down, left, [upper_left, upper_right, bottom_left, bottom_right]), rect)

            # Draw doors
            if tile == 11:
                room.doors_rect.append({'rect': rect, 'destination': room.doors[(y, x)]})
                screen.blit(map_tile_set[7][8], rect)
                screen.blit(choose_rotation((y, x), room, map_tile_set[3][7], map_tile_set[4][7], map_tile_set[3][6], map_tile_set[4][8]).convert_alpha(), rect)

    # Update the display
    pygame.display.flip()
