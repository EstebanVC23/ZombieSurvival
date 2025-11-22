import pygame
import math
import os
from settings import WEAPON_BULLET_SPEED, BULLET_BASE_LIFETIME
from utils.helpers import load_image_safe
from core.impact import Impact

SPRITE_ANGLE_OFFSET = 45.0


class Bullet(pygame.sprite.Sprite):
    """Bala disparada por el jugador, con colisión contra zombies y objetos decorativos."""

    def __init__(self, pos, direction, damage=None, lifetime=None):
        super().__init__()
        self.pos = pygame.math.Vector2(pos)
        self.direction = self._normalize_vector(direction)
        self.image, self.rect = self._load_bullet_image()

        self.velocity = self.direction * WEAPON_BULLET_SPEED
        self.damage = damage if damage is not None else 0
        self.lifetime = lifetime if lifetime is not None else BULLET_BASE_LIFETIME

        self.alive_time = 0.0
        self.radius = max(1, self.rect.width // 2)

    # ------------------------------------------------------------------
    # Inicialización y utilidades
    # ------------------------------------------------------------------
    def _normalize_vector(self, vec):
        v = pygame.math.Vector2(vec)
        return v.normalize() if v.length_squared() > 0 else pygame.math.Vector2(1, 0)

    def _load_bullet_image(self):
        path = os.path.join("weapons", "bullet.png")
        base_img = load_image_safe(path)

        # si no hay sprite, usar una bala circular
        if not base_img:
            surf = pygame.Surface((12, 12), pygame.SRCALPHA)
            pygame.draw.circle(surf, (255, 230, 100), (6, 6), 6)
            return surf, surf.get_rect(center=self.pos)

        # limpiar imagen y rotarla
        base_img = pygame.transform.scale(base_img, (24, 24))
        base_img = self._clean_image(base_img)

        angle = math.degrees(math.atan2(self.direction.y, self.direction.x))
        rotation = -angle - SPRITE_ANGLE_OFFSET
        rotated = pygame.transform.rotate(base_img, rotation)

        return rotated, rotated.get_rect(center=self.pos)

    def _clean_image(self, img):
        """Elimina fondos blancos o casi transparentes."""
        img = img.convert_alpha()
        clean = pygame.Surface(img.get_size(), pygame.SRCALPHA)
        img.lock()

        w, h = img.get_size()
        for x in range(w):
            for y in range(h):
                r, g, b, a = img.get_at((x, y))
                if (r + g + b) / 3 > 200 or a < 80:
                    img.set_at((x, y), (0, 0, 0, 0))

        img.unlock()
        clean.blit(img, (0, 0))
        return clean

    # ------------------------------------------------------------------
    #   LÓGICA DE ACTUALIZACIÓN
    # ------------------------------------------------------------------
    def update(self, dt, game):
        # Movimiento
        self.pos += self.velocity * dt
        self.rect.center = (round(self.pos.x), round(self.pos.y))
        self.alive_time += dt

        # ============================================================
        #   IMPACTO CONTRA ZOMBIES
        # ============================================================
        for zombie in game.zombies:
            zpos = pygame.math.Vector2(zombie.rect.center)
            zrad = getattr(zombie, "radius", zombie.rect.width // 2)

            if self.pos.distance_to(zpos) <= zrad * 0.6:

                # aplicar daño
                try:
                    zombie.take_damage(self.damage, game)
                except TypeError:
                    zombie.take_damage(self.damage)

                # efecto de impacto
                try:
                    game.effects.add(Impact(zombie.rect.center))
                except Exception:
                    pass

                self.kill()
                return

        # ============================================================
        #   IMPACTO CONTRA OBJETOS DEL MUNDO
        # ============================================================
        if hasattr(game, "object_map") and game.object_map:

            for deco in game.object_map.objects:

                # ignorar objetos no sólidos
                if not deco.solid or not deco.hitbox:
                    continue

                if self.rect.colliderect(deco.hitbox):
                    # crear impacto
                    try:
                        game.effects.add(Impact(self.rect.center))
                    except Exception:
                        pass

                    self.kill()
                    return

        # ============================================================
        #   MUERTE POR TIEMPO DE VIDA
        # ============================================================
        if self.alive_time >= self.lifetime:
            self.kill()
