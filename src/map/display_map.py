import pygame

from src import utils

TILE_SIZE = utils.TILE_SIZE

# Define colors
background_color = (20, 0, 10)
unknown_color = (255, 0, 255)
# nice_red = (210, 70, 70)

colors_dict = {
    0:(100, 160, 160),  # floor
    1:(30, 50, 50),     # wall
    11:(255, 0, 0),     # UP_door
    12:(0, 255, 0),     # DOWN_door
    13:(255, 255, 0),   # LEFT_door
    14:(0,0,255),       # RIGHT_door
    100:(255, 140, 80)  # test
}

def draw_room(dungeon_layout, screen):
    room_size = (len(dungeon_layout[0]) * TILE_SIZE, len(dungeon_layout) * TILE_SIZE)
    top_left_corner = [(a - b)/2 for a, b in zip(utils.SCREEN_SIZE, room_size)]
    # print(room_size)
    # print(top_left_corner)

    # Clear the screen
    screen.fill(background_color)

    # Draw the dungeon
    for y, row in enumerate(dungeon_layout):
        for x, tile in enumerate(row):
            rect = pygame.Rect(top_left_corner[0] + x * TILE_SIZE, top_left_corner[1] + y * TILE_SIZE, TILE_SIZE, TILE_SIZE)

            pygame.draw.rect(screen, colors_dict.get(tile, unknown_color), rect)

    # Update the display
    pygame.display.flip()