import csv
import os
import pygame

world_size = (21 * 64, 14 * 64)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
basic_entity_size = (64, 64)
font = './assets/Minecraft.ttf'
map_center = []


def resource_path(relative_path):
    base_path = os.path.abspath("..")
    return os.path.join(base_path, relative_path)


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