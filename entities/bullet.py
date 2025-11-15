import pygame
import math
import os
from settings import WEAPON_BULLET_SPEED, BULLET_BASE_LIFETIME
from utils.helpers import load_image_safe
from core.impact import Impact  # efecto visual (si existe)

# Ajuste en grados: si tu sprite apunta diagonal arriba-derecha, usa +45.
# Si apunta en otra dirección, cambia este valor (por ejemplo -90, +90, 0).
SPRITE_ANGLE_OFFSET = 45.0

class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos, direction, damage=None, lifetime=None):
        super().__init__()

        # Asegurar Vector2
        self.pos = pygame.math.Vector2(pos)
        if not isinstance(direction, pygame.math.Vector2):
            direction = pygame.math.Vector2(direction)
        if direction.length_squared() > 0:
            self.direction = direction.normalize()
        else:
            self.direction = pygame.math.Vector2(1, 0)

        # Imagen: buscar en carpeta de assets (load_image_safe espera ruta relativa dentro de ASSETS_IMAGES)
        image_path = os.path.join("weapons", "bullet.png")
        base_img = load_image_safe(image_path)

        if base_img:
            # Escalado base
            base_img = pygame.transform.scale(base_img, (24, 24))
            base_img = self.clean_image(base_img)

            # Ángulo de la dirección deseada (en grados)
            angle = math.degrees(math.atan2(self.direction.y, self.direction.x))

            # Aplicar offset para compensar orientación original del sprite:
            # pygame.transform.rotate rota la imagen COUNTER-CLOCKWISE por el ángulo dado.
            # La formulación final resulta en: rotación = (angle - sprite_initial_angle)
            # pero como usamos la convención de rotación negativa anteriormente, aplicamos:
            rotation = -angle - SPRITE_ANGLE_OFFSET

            self.image = pygame.transform.rotate(base_img, rotation)

            # Ajustar rect al centro original
            self.rect = self.image.get_rect(center=(round(self.pos.x), round(self.pos.y)))
        else:
            print(f"[WARN] No se encontró la imagen de bala en: {image_path}")
            self.image = pygame.Surface((12, 12), pygame.SRCALPHA)
            pygame.draw.circle(self.image, (255, 230, 100), (6, 6), 6)
            self.rect = self.image.get_rect(center=(round(self.pos.x), round(self.pos.y)))

        # Velocidad y duración usando settings por defecto si no se pasan
        self.velocity = self.direction * WEAPON_BULLET_SPEED
        self.damage = damage if damage is not None else 0
        self.lifetime = lifetime if lifetime is not None else BULLET_BASE_LIFETIME
        self.alive_time = 0.0
        self.radius = max(1, self.rect.width // 2)

    def clean_image(self, img):
        img = img.convert_alpha()
        clean = pygame.Surface(img.get_size(), pygame.SRCALPHA)
        img.lock()
        for x in range(img.get_width()):
            for y in range(img.get_height()):
                r, g, b, a = img.get_at((x, y))
                brightness = (r + g + b) / 3
                if brightness > 200 or a < 80:
                    img.set_at((x, y), (0, 0, 0, 0))
        img.unlock()
        clean.blit(img, (0, 0))
        return clean

    def update(self, dt, game):
        # Movimiento
        self.pos += self.velocity * dt
        self.rect.center = (round(self.pos.x), round(self.pos.y))
        self.alive_time += dt

        # Colisión con zombies: comprobación por distancia al centro (más precisa)
        for zombie in game.zombies:
            z_center = pygame.math.Vector2(zombie.rect.center)
            dist = self.pos.distance_to(z_center)
            if dist <= (getattr(zombie, "radius", zombie.rect.width // 2) * 0.6):
                try:
                    zombie.take_damage(self.damage, game)
                except TypeError:
                    zombie.take_damage(self.damage)
                try:
                    impact = Impact(zombie.rect.center)
                    game.effects.add(impact)
                except Exception:
                    pass
                self.kill()
                return

        # Vida de la bala
        if self.alive_time >= self.lifetime:
            self.kill()
