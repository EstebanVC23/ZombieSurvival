# tile.py
import pygame
from utils.helpers import clean_image_background
from settings import OBJECT_SIZES

class Tile:
    def __init__(self, surface, x, y, tile_size):
        self.image = surface
        self.x = x
        self.y = y
        self.rect = pygame.Rect(x, y, tile_size, tile_size)

class DecorTile:
    """Tile decorativo con tamaño propio."""
    def __init__(self, surface, x, y, object_name):
        self.width, self.height = OBJECT_SIZES.get(object_name, (40, 40))
        surf = pygame.transform.scale(surface, (self.width, self.height))
        self.image = clean_image_background(surf)
        self.x = x
        self.y = y
        self.rect = pygame.Rect(x, y, self.width, self.height)
