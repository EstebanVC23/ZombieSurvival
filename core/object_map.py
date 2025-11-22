# core/object_map.py
import os
import random
import math
import pygame
from core.tile import DecorTile
from utils.helpers import load_image_safe, clean_image_background
from utils.movement_utils import MovementUtils
from settings import (
    TERRAIN_TO_OBJECT, OBJECT_SPAWN_CHANCE,
    TILE_OBJECT_PROBABILITY, OBJECT_SIZES,
    WORLD_WIDTH, WORLD_HEIGHT, OBJECT_DIR,
    TERRAIN_TILE_SIZE
)

class ObjectMap:
    _object_cache = {}

    def __init__(self, matrix, tile_size=None):
        self.tile_size = int(tile_size or TERRAIN_TILE_SIZE)
        self.matrix = matrix or []

        self.cols = math.ceil(WORLD_WIDTH / self.tile_size)
        self.rows = math.ceil(WORLD_HEIGHT / self.tile_size)

        self.objects = []
        self._prepare_objects()

    def _load_object_texture(self, name):
        if name in self._object_cache:
            return self._object_cache[name]

        path = os.path.join(OBJECT_DIR, f"{name}.png")
        img = load_image_safe(path)

        if img is None:
            w, h = OBJECT_SIZES.get(name, (40, 40))
            surf = pygame.Surface((w, h), pygame.SRCALPHA)
            surf.fill((255, 0, 255))
            self._object_cache[name] = surf
            return surf

        self._object_cache[name] = img
        return img

    def _prepare_objects(self):
        norm = []
        for row in self.matrix:
            norm.append(list(row) if isinstance(row, str) else [str(c) for c in row])

        for ty in range(self.rows):
            for tx in range(self.cols):
                ch = "G"
                if ty < len(norm) and tx < len(norm[ty]):
                    val = norm[ty][tx]
                    ch = val.upper() if val else "G"

                possible = TERRAIN_TO_OBJECT.get(ch, [])
                if not possible:
                    continue

                if random.random() > TILE_OBJECT_PROBABILITY:
                    continue

                weights = [OBJECT_SPAWN_CHANCE.get(o, 0.1) for o in possible]
                name = random.choices(possible, weights=weights, k=1)[0]

                img_raw = self._load_object_texture(name)

                w, h = OBJECT_SIZES.get(name, (40, 40))
                img = pygame.transform.scale(img_raw, (w, h))
                img = clean_image_background(img)

                # base del tile
                px = tx * self.tile_size
                py = ty * self.tile_size

                draw_x = px + max(0, (self.tile_size - w)//2)
                draw_y = py + (self.tile_size - h)

                obj = DecorTile(img, draw_x, draw_y, name)
                self.objects.append(obj)

    def resolve_collision(self, entity):
        for obj in self.objects:
            if not obj.solid:
                continue
            if not obj.hitbox:
                continue

            if entity.rect.colliderect(obj.hitbox):
                MovementUtils.push_out(entity.rect, obj.hitbox)
                entity.pos.xy = entity.rect.center

    def draw(self, surface, camera, player):
        drawables = self.objects + [player]

        drawables.sort(key=lambda obj: obj.rect.bottom)

        for obj in drawables:
            surface.blit(obj.image, camera.apply(obj.rect))

    def check_bullet_collision(self, bullet):
        """
        Revisa si una bala choca contra un objeto sólido.
        Devuelve True si colisiona.
        """
        for obj in self.objects:
            if not obj.solid:
                continue
            if not obj.hitbox:
                continue

            if bullet.rect.colliderect(obj.hitbox):
                return True

        return False
