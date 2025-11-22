# core/terrain_map.py
import os
import math
import pygame
from utils.helpers import load_image_safe
from settings import (
    WORLD_WIDTH, WORLD_HEIGHT, TERRAIN_TILE_SIZE,
    TERRAIN_DEFAULT_LETTER, TERRAIN_LETTER_MAP, TERRAIN_DIR
)

class Tile:
    def __init__(self, image, x, y):
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))


class TerrainMap:
    _texture_cache = {}

    def __init__(self, matrix, tile_size=None):
        self.tile_size = int(tile_size or TERRAIN_TILE_SIZE)
        self.cols = math.ceil(WORLD_WIDTH / self.tile_size)
        self.rows = math.ceil(WORLD_HEIGHT / self.tile_size)

        self.matrix = matrix or []
        self._normalize_matrix_size()

        self.tiles = []
        self._prepare_tiles()

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
                    normalized.append(row + [TERRAIN_DEFAULT_LETTER]*(self.cols-len(row)))
            else:
                normalized.append([TERRAIN_DEFAULT_LETTER]*self.cols)

        self.matrix = normalized

    def _load_texture(self, terrain_name):
        if terrain_name in self._texture_cache:
            return self._texture_cache[terrain_name]

        relative = os.path.join(TERRAIN_DIR, f"{terrain_name}.png")
        img = load_image_safe(relative)

        if img is None:
            surf = pygame.Surface((self.tile_size, self.tile_size))
            surf.fill((150,120,60))
            self._texture_cache[terrain_name] = surf
            return surf

        surf = pygame.transform.scale(img, (self.tile_size, self.tile_size)).convert_alpha()
        self._texture_cache[terrain_name] = surf
        return surf

    def _prepare_tiles(self):
        self.tiles = []
        for y in range(self.rows):
            for x in range(self.cols):
                ch = self.matrix[y][x].upper()
                terrain_name = TERRAIN_LETTER_MAP.get(ch, TERRAIN_LETTER_MAP[TERRAIN_DEFAULT_LETTER])
                img = self._load_texture(terrain_name)
                tile = Tile(img, x*self.tile_size, y*self.tile_size)
                self.tiles.append(tile)

    def draw(self, surface, camera):
        vw, vh = surface.get_width(), surface.get_height()
        vx, vy = camera.offset.x, camera.offset.y
        viewport = pygame.Rect(vx, vy, vw, vh)

        left   = max(0, int(viewport.left  // self.tile_size))
        right  = min(self.cols, int(math.ceil(viewport.right  / self.tile_size)))
        top    = max(0, int(viewport.top   // self.tile_size))
        bottom = min(self.rows, int(math.ceil(viewport.bottom / self.tile_size)))

        for ty in range(top, bottom):
            for tx in range(left, right):
                idx = ty*self.cols + tx
                tile = self.tiles[idx]
                surface.blit(tile.image, camera.apply(tile.rect))
