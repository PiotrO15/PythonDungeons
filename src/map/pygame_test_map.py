import random
import pygame
import sys

# BAD, DON'T USE

# Define constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800
TILE_SIZE = 64
GRID_SIZE_X = SCREEN_WIDTH // TILE_SIZE
GRID_SIZE_Y = SCREEN_HEIGHT // TILE_SIZE

# Define colors
background_color = (20, 0, 10)
floor_color = (100, 160, 160)
wall_color = (30, 50, 50)
test_color = (255, 140, 80)
nice_red = (210, 70, 70)
def bfs(start_x, start_y, room):
    rows = len(room)
    cols = len(room[0])
    visited = [[False for _ in range(cols)] for _ in range(rows)]
    queue = [(start_x, start_y)]
    visited[start_y][start_x] = True

    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    while queue:
        x, y = queue.pop(0)
        for dx, dy in directions:
            new_x, new_y = x + dx, y + dy
            if 0 <= new_x < cols and 0 <= new_y < rows and not visited[new_y][new_x]:
                if room[new_y][new_x] == 0:
                    visited[new_y][new_x] = True
                    queue.append((new_x, new_y))
    return visited


def check_if_accessible(x, y, room):
    rows = len(room)
    cols = len(room[0])

    walls = 0
    # Check above and below
    for i in [-1, 1]:
        if 0 <= y + i < rows:
            if room[y + i][x] != 1:
                walls += 1

    # Check left and right
    for i in [-1, 1]:
        if 0 <= x + i < cols:
            if room[y][x + i] == 1:
                walls += 1
    if walls == 4: return False
    return True


def ensure_accessibility(room):
    rows = len(room)
    cols = len(room[0])

    for y in range(rows):
        for x in range(cols):
            if room[y][x] == 0:
                visited = bfs(x, y, room)
                for i in range(rows):
                    for j in range(cols):
                        if room[i][j] == 0 and not visited[i][j]:
                            if check_if_accessible(j, i, room):
                                room[i][j] = 0  # Ensure the tile is accessible
                            else:
                                # Convert adjacent walls to floor to ensure connectivity
                                for dx, dy in [(-1, 0), (1, 0), (0, -1)]:
                                    new_x, new_y = j + dx, i + dy
                                    if 0 <= new_x < cols and 0 <= new_y < rows and room[new_y][new_x] == 1:
                                        room[new_y][new_x] = 100
                                        break


def create_room(x_size, y_size):
    # Create a simple dungeon layout (1 for walls, 0 for floor)
    room_layout = [[random.choice([0, 1]) for x in range(x_size)] for y in range(y_size)]

    ensure_accessibility(room_layout)

    return room_layout

def draw_map(dungeon_layout, screen):
    # Clear the screen
    #screen.fill(background_color)

    # Draw the dungeon
    for y, row in enumerate(dungeon_layout):
        for x, tile in enumerate(row):
            rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            if tile == 1:
                pygame.draw.rect(screen, wall_color, rect)
            elif tile == 100:
                pygame.draw.rect(screen, test_color, rect)
            else:
                pygame.draw.rect(screen, floor_color, rect)

    # Update the display
    pygame.display.flip()

def main():

    # Create the screen
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Dungeon Display")

    # dungeon_layout = create_room(GRID_SIZE_X, GRID_SIZE_Y)
    dungeon_layout = create_room(25, 20)

    draw_map(dungeon_layout, screen)

    # Main game loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False


if __name__ == "__main__":
    # Initialize Pygame
    pygame.init()

    main()

    # Quit Pygame
    pygame.quit()
    sys.exit()
