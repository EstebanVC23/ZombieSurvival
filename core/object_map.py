# object_map.py
import os
import random
import math
import pygame
from core.tile import DecorTile
from utils.helpers import load_image_safe
from settings import (
    TERRAIN_TO_OBJECT, OBJECT_SPAWN_CHANCE,
    TILE_OBJECT_PROBABILITY, OBJECT_SIZES,
    TERRAIN_LETTER_MAP, TERRAIN_DEFAULT_LETTER,
    WORLD_WIDTH, WORLD_HEIGHT, TERRAIN_TILE_SIZE
)

class ObjectMap:

    _object_cache = {}

    def __init__(self, matrix, tile_size=None):
        self.tile_size = tile_size or TERRAIN_TILE_SIZE
        self.matrix = matrix
        self.cols = math.ceil(WORLD_WIDTH / self.tile_size)
        self.rows = math.ceil(WORLD_HEIGHT / self.tile_size)

        self.objects = []
        self._prepare_objects()

    # -------------------------------------------
    def _load_object_texture(self, object_name):
        if object_name in self._object_cache:
            return self._object_cache[object_name]

        relative = os.path.join("objects", f"{object_name}.png")
        img = load_image_safe(relative)

        if img is None:
            surf = pygame.Surface(OBJECT_SIZES.get(object_name, (40,40)), pygame.SRCALPHA)
            surf.fill((255, 0, 255, 255))
            self._object_cache[object_name] = surf
            return surf

        self._object_cache[object_name] = img
        return img

    # -------------------------------------------
    def _prepare_objects(self):
        self.objects = []

        for ty in range(self.rows):
            for tx in range(self.cols):

                char = self.matrix[ty][tx].upper()
                possible_objs = TERRAIN_TO_OBJECT.get(char, [])

                if not possible_objs:
                    continue

                if random.random() > TILE_OBJECT_PROBABILITY:
                    continue

                # elegir objeto por pesos
                weights = [OBJECT_SPAWN_CHANCE.get(o, 0.1) for o in possible_objs]
                selected = random.choices(possible_objs, weights=weights, k=1)[0]

                img = self._load_object_texture(selected)
                px = tx * self.tile_size
                py = ty * self.tile_size

                self.objects.append(DecorTile(img, px, py, selected))

    # -------------------------------------------
    def draw(self, surface, camera):
        for obj in self.objects:
            dest = camera.apply(obj.rect)
            surface.blit(obj.image, dest)
