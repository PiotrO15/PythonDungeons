import pygame
import generator
import random

from src import utils

TILE_SIZE = utils.TILE_SIZE

# Define colors
background_color = (20, 0, 10)
unknown_color = (255, 0, 255)
# nice_red = (210, 70, 70)

colors_dict = {
    0:(100, 160, 160),  # floor
    1:(30, 50, 50),     # wall
    11:(255, 0, 0),     # door
    12:(0, 255, 0),     # G
    13:(255, 255, 0),   # Y
    14:(0,0,255),       # B
    100:(255, 140, 80)  # test
}


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

    if corners:
        if is_up and is_left:
            return corners[0]
        if is_up and is_right:
            return corners[1]
        if is_down and is_left:
            return corners[2]
        if is_down and is_right:
            return corners[3]

    if is_up:
        return up
    elif is_right:
        return right
    elif is_left:
        return left
    elif is_down:
        return down

    else:
        return down


def draw_room(room: generator.Room, screen):
    room_size_px = (room.size[0] * utils.ROOM_DIMENSIONS[0] * TILE_SIZE, room.size[1] * utils.ROOM_DIMENSIONS[1] * TILE_SIZE)
    top_left_corner = [(a - b)/2 for a, b in zip(utils.SCREEN_SIZE, room_size_px)]

    # Clear the screen
    screen.fill(background_color)
    random.seed(room.seed)

    # Draw the dungeon
    for y, row in enumerate(room.layout):
        for x, tile in enumerate(row):
            rect = pygame.Rect(top_left_corner[0] + x * TILE_SIZE, top_left_corner[1] + y * TILE_SIZE, TILE_SIZE, TILE_SIZE)

            pygame.draw.rect(screen, colors_dict.get(tile, unknown_color), rect)

            if tile == 11:
                room.doors_rect.append({'rect': rect,'destination': room.doors[(y, x)]})
                screen.blit(map_tile_set[7][8], rect)
                screen.blit(choose_rotation((y, x), room, map_tile_set[3][7], map_tile_set[4][7], map_tile_set[3][6], map_tile_set[4][8]).convert_alpha(), rect)

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

            if tile == 0:
                # Get random tile set from [0][6] to [2][9]
                random_tile = map_tile_set[random.randint(0, 2)][random.randint(6, 9)]

                screen.blit(random_tile, (top_left_corner[0] + x * TILE_SIZE, top_left_corner[1] + y * TILE_SIZE))


    # Update the display
    pygame.display.flip()