import pygame
import generator

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

def draw_room(room: generator.Room, screen):
    room_size_px = (room.size[0] * utils.ROOM_DIMENSIONS[0] * TILE_SIZE, room.size[1] * utils.ROOM_DIMENSIONS[1] * TILE_SIZE)
    top_left_corner = [(a - b)/2 for a, b in zip(utils.SCREEN_SIZE, room_size_px)]

    # Clear the screen
    screen.fill(background_color)

    # Draw the dungeon
    for y, row in enumerate(room.layout):
        for x, tile in enumerate(row):
            rect = pygame.Rect(top_left_corner[0] + x * TILE_SIZE, top_left_corner[1] + y * TILE_SIZE, TILE_SIZE, TILE_SIZE)

            if tile == 11:
                room.doors_rect.append({'rect': rect,'destination': room.doors[(y, x)]})
            pygame.draw.rect(screen, colors_dict.get(tile, unknown_color), rect)

    # Update the display
    pygame.display.flip()