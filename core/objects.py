# core/terrain.py
import os
import math
import pygame
from utils.helpers import load_image_safe  # tu helper (usa ASSETS_IMAGES internamente)
from settings import WORLD_WIDTH, WORLD_HEIGHT, TERRAIN_TILE_SIZE, TERRAIN_DEFAULT_LETTER, TERRAIN_LETTER_MAP

# intentar obtener TERRAIN_TILE_SIZE desde settings si existe; fallback 100
try:
    from settings import TERRAIN_TILE_SIZE
except Exception:
    TERRAIN_TILE_SIZE = 100  # default pedido


class Tile:
    def __init__(self, surface, x, y, tile_size):
        self.image = surface
        self.x = x
        self.y = y
        self.rect = pygame.Rect(x, y, tile_size, tile_size)


class TileMap:
    """
    TileMap que utiliza WORLD_WIDTH/WORLD_HEIGHT como límites del mundo.
    - matrix: lista de strings (cada string = fila)
    - tile_size: TILE SIZE (p.ej. 100)
    """

    _texture_cache = {}  # cache de superficies por "terrain_name"

    def __init__(self, matrix, tile_size=None):
        self.tile_size = int(tile_size or TERRAIN_TILE_SIZE)
        # número de columnas/filas que cubren el mundo completo
        self.cols = math.ceil(WORLD_WIDTH / self.tile_size)
        self.rows = math.ceil(WORLD_HEIGHT / self.tile_size)

        # matrix provista (si es menor se rellena con default; si mayor se recorta)
        self.matrix = matrix or []
        self._normalize_matrix_size()

        self.pixel_width = WORLD_WIDTH
        self.pixel_height = WORLD_HEIGHT

        self.tiles = []
        self._prepare_tiles_from_matrix(self.matrix)

    def _normalize_matrix_size(self):
        """
        Asegura que self.matrix tenga exactly self.rows filas, y cada fila tenga self.cols columnas.
        Rellena con TERRAIN_DEFAULT_LETTER si falta.
        """
        rows = []
        for r in self.matrix:
            if isinstance(r, str):
                rows.append(list(r))
            else:
                rows.append([str(c) for c in r])

        # recortar o rellenar filas
        normalized = []
        for y in range(self.rows):
            if y < len(rows):
                row = rows[y]
                # recortar o rellenar cada fila a cols
                if len(row) >= self.cols:
                    normalized.append(row[:self.cols])
                else:
                    normalized.append(row + [TERRAIN_DEFAULT_LETTER] * (self.cols - len(row)))
            else:
                # fila faltante -> rellenar con default
                normalized.append([TERRAIN_DEFAULT_LETTER] * self.cols)

        self.matrix = normalized

    # -------------------------
    # Cargar textura (cacheada)
    # -------------------------
    def _load_texture(self, terrain_name):
        """
        Carga assets/images/terrain/{terrain_name}.png mediante load_image_safe.
        Devuelve superficie escalada a tile_size.
        """
        if terrain_name in self._texture_cache:
            return self._texture_cache[terrain_name]

        relative = os.path.join("terrain", f"{terrain_name}.png")
        img = load_image_safe(relative)  # tu helper resuelve ASSETS_IMAGES + relative
        if img is None:
            # placeholder (transparente con color para debug)
            surf = pygame.Surface((self.tile_size, self.tile_size), pygame.SRCALPHA)
            surf.fill((160, 0, 160, 255))  # morado debug (si ves morado indica assets faltan)
            self._texture_cache[terrain_name] = surf
            return surf

        # escalar a tile_size
        try:
            surf = pygame.transform.scale(img, (self.tile_size, self.tile_size)).convert_alpha()
        except Exception:
            surf = pygame.transform.scale(img, (self.tile_size, self.tile_size))
        self._texture_cache[terrain_name] = surf
        return surf

    # -------------------------
    # Construcción tiles
    # -------------------------
    def _prepare_tiles_from_matrix(self, matrix):
        self.tiles = []
        for ty in range(self.rows):
            for tx in range(self.cols):
                char = matrix[ty][tx].upper() if ty < len(matrix) and tx < len(matrix[ty]) else TERRAIN_DEFAULT_LETTER
                terrain_name = TERRAIN_LETTER_MAP.get(char, TERRAIN_LETTER_MAP.get(TERRAIN_DEFAULT_LETTER))
                surf = self._load_texture(terrain_name)
                px = tx * self.tile_size
                py = ty * self.tile_size
                tile = Tile(surf, px, py, self.tile_size)
                self.tiles.append(tile)

    # -------------------------
    # Dibujo optimizado
    # -------------------------
    def draw(self, surface, camera):
        if not self.tiles:
            return

        # viewport rect en coordenadas del mundo
        vw = surface.get_width()
        vh = surface.get_height()
        vx = camera.offset.x
        vy = camera.offset.y
        viewport = pygame.Rect(vx, vy, vw, vh)

        # calcular rango de tiles visibles (más rápido que iterar todas)
        left_col = max(0, int(viewport.left // self.tile_size))
        right_col = min(self.cols - 1, int(math.ceil(viewport.right / self.tile_size)))
        top_row = max(0, int(viewport.top // self.tile_size))
        bottom_row = min(self.rows - 1, int(math.ceil(viewport.bottom / self.tile_size)))

        for ty in range(top_row, bottom_row + 1):
            for tx in range(left_col, right_col + 1):
                idx = ty * self.cols + tx
                tile = self.tiles[idx]
                dest_rect = camera.apply(tile.rect)
                surface.blit(tile.image, dest_rect)
