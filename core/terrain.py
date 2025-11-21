import os
import math
import random
import pygame
from utils.helpers import load_image_safe, clean_image_background
from settings import WORLD_WIDTH, WORLD_HEIGHT, TERRAIN_TILE_SIZE, TERRAIN_DEFAULT_LETTER, TERRAIN_LETTER_MAP
from settings import OBJECT_SIZES, TERRAIN_TO_OBJECT, OBJECT_SPAWN_CHANCE
from settings import TILE_OBJECT_PROBABILITY
from settings import TERRAIN_TILE_SIZE

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

class TileMap:
    _texture_cache = {}
    _object_cache = {}

    def __init__(self, matrix, tile_size=None, object_chance=0.25):
        self.tile_size = int(tile_size or TERRAIN_TILE_SIZE)
        self.object_chance = object_chance  # probabilidad de que aparezca un objeto en un tile

        self.cols = math.ceil(WORLD_WIDTH / self.tile_size)
        self.rows = math.ceil(WORLD_HEIGHT / self.tile_size)

        self.matrix = matrix or []
        self._normalize_matrix_size()

        self.pixel_width = WORLD_WIDTH
        self.pixel_height = WORLD_HEIGHT

        self.tiles = []
        self.objects = []

        self._prepare_tiles_from_matrix(self.matrix)
        self._prepare_objects()

    def _normalize_matrix_size(self):
        rows = []
        for r in self.matrix:
            if isinstance(r, str):
                rows.append(list(r))
            else:
                rows.append([str(c) for c in r])

        normalized = []
        for y in range(self.rows):
            if y < len(rows):
                row = rows[y]
                if len(row) >= self.cols:
                    normalized.append(row[:self.cols])
                else:
                    normalized.append(row + [TERRAIN_DEFAULT_LETTER]*(self.cols - len(row)))
            else:
                normalized.append([TERRAIN_DEFAULT_LETTER]*self.cols)
        self.matrix = normalized

    def _load_texture(self, terrain_name):
        if terrain_name in self._texture_cache:
            return self._texture_cache[terrain_name]

        relative = os.path.join("terrain", f"{terrain_name}.png")
        img = load_image_safe(relative)
        if img is None:
            surf = pygame.Surface((self.tile_size, self.tile_size), pygame.SRCALPHA)
            surf.fill((160, 0, 160, 255))
            self._texture_cache[terrain_name] = surf
            return surf

        try:
            surf = pygame.transform.scale(img, (self.tile_size, self.tile_size)).convert_alpha()
        except Exception:
            surf = pygame.transform.scale(img, (self.tile_size, self.tile_size))
        self._texture_cache[terrain_name] = surf
        return surf

    def _load_object_texture(self, object_name):
        if object_name in self._object_cache:
            return self._object_cache[object_name]

        relative = os.path.join("objects", f"{object_name}.png")
        img = load_image_safe(relative)
        if img is None:
            surf = pygame.Surface(OBJECT_SIZES.get(object_name, (40,40)), pygame.SRCALPHA)
            surf.fill((255,0,255,255))
            self._object_cache[object_name] = surf
            return surf

        self._object_cache[object_name] = img
        return img

    def _prepare_tiles_from_matrix(self, matrix):
        self.tiles = []
        for ty in range(self.rows):
            for tx in range(self.cols):
                char = matrix[ty][tx].upper() if ty < len(matrix) and tx < len(matrix[ty]) else TERRAIN_DEFAULT_LETTER
                terrain_name = TERRAIN_LETTER_MAP.get(char, TERRAIN_LETTER_MAP.get(TERRAIN_DEFAULT_LETTER))
                surf = self._load_texture(terrain_name)
                px = tx * self.tile_size
                py = ty * self.tile_size
                self.tiles.append(Tile(surf, px, py, self.tile_size))

    def _prepare_objects(self):
        self.objects = []
        for ty in range(self.rows):
            for tx in range(self.cols):
                char = self.matrix[ty][tx].upper()
                possible_objs = TERRAIN_TO_OBJECT.get(char, [])
                if possible_objs and random.random() < TILE_OBJECT_PROBABILITY:
                    # elegir objeto según probabilidad
                    weights = [OBJECT_SPAWN_CHANCE.get(o, 0.1) for o in possible_objs]
                    selected_obj = random.choices(possible_objs, weights=weights, k=1)[0]
                    img = self._load_object_texture(selected_obj)
                    px = tx * self.tile_size
                    py = ty * self.tile_size
                    self.objects.append(DecorTile(img, px, py, selected_obj))

    def draw(self, surface, camera):
        if not self.tiles:
            return
        vw, vh = surface.get_width(), surface.get_height()
        vx, vy = camera.offset.x, camera.offset.y
        viewport = pygame.Rect(vx, vy, vw, vh)

        left_col = max(0, int(viewport.left // self.tile_size))
        right_col = min(self.cols-1, int(math.ceil(viewport.right / self.tile_size)))
        top_row = max(0, int(viewport.top // self.tile_size))
        bottom_row = min(self.rows-1, int(math.ceil(viewport.bottom / self.tile_size)))

        # dibujar tiles
        for ty in range(top_row, bottom_row+1):
            for tx in range(left_col, right_col+1):
                idx = ty * self.cols + tx
                tile = self.tiles[idx]
                dest_rect = camera.apply(tile.rect)
                surface.blit(tile.image, dest_rect)

        # dibujar objetos encima
        for obj in self.objects:
            dest_rect = camera.apply(obj.rect)
            surface.blit(obj.image, dest_rect)
