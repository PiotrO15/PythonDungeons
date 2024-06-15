import csv
import os
import pygame

SCREEN_SIZE = (1600, 1000)

TILE_SIZE = 32
ROOM_DIMENSIONS = (13, 9) # (y, x)
BLACK = (0, 0, 0)
BACKGROUND_COLOR = (37, 19, 26)
WHITE = (255, 255, 255)
basic_entity_size = (30, 30)
font = '../assets/Minecraft.ttf'

def resource_path(relative_path):
    base_path = os.path.abspath("..")
    return os.path.join(base_path, relative_path)

def add_tuples(t_a, t_b):
    return tuple(a + b for a, b in zip(t_a, t_b))

def time_passed(timer, amount):
    if pygame.time.get_ticks() - timer > amount:
        timer = pygame.time.get_ticks()
        return True
def read_csv(filename):
    array = []
    with open(filename) as data:
        data = csv.reader(data, delimiter=',')
        for row in data:
            array.append(list(row))
    return array

def get_mask_rect(surf, top=0, left=0):
    """Returns minimal bounding rectangle of an image"""
    surf_mask = pygame.mask.from_surface(surf)
    rect_list = surf_mask.get_bounding_rects()
    if rect_list:
        surf_mask_rect = rect_list[0].unionall(rect_list)
        surf_mask_rect.move_ip(top, left)
        return surf_mask_rect
