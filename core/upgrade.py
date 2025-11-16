import pygame
import os
import random
import math
from settings import (
    ASSETS_IMAGES,
    UPGRADE_ICON_SIZE,
    UPGRADE_SPAWN_CHANCE,
    UPGRADE_FALL_SPEED,
    UPGRADE_FALL_DECAY,
    UPGRADE_FALL_DURATION,
    ZOMBIE_UPGRADE_DROP_SYSTEM,
)
from utils.helpers import load_image_safe, clean_image_background


class Upgrade(pygame.sprite.Sprite):
    """Clase de mejoras (upgrades) que caen de zombies."""

    def __init__(self, upgrade_type, pos):
        super().__init__()
        self.type = upgrade_type
        self.image = self.load_icon(upgrade_type)
        self.rect = self.image.get_rect(center=pos)
        self.pos = pygame.Vector2(pos)

        # Animación de caída
        self.fall_timer = 0.0
        self.fall_speed = 0.0
        self.fall_angle = 0.0
        self.fall_distance = 0.0
        self.active_fall = False

    @property
    def x(self):
        return self.pos.x

    @property
    def y(self):
        return self.pos.y

    # ==========================================================
    # 🔹 Cargar ícono usando helpers
    # ==========================================================
    def load_icon(self, upgrade_type):
        """Carga la imagen de la mejora, la escala y limpia fondo claro."""
        path = os.path.join("upgrades", f"{upgrade_type}.png")
        img = load_image_safe(path)  # ✅ usa helpers

        if img:
            img = pygame.transform.scale(img, (UPGRADE_ICON_SIZE, UPGRADE_ICON_SIZE))
            img = clean_image_background(img)  # ✅ limpieza uniforme
            return img
        else:
            print(f"[WARN] Icono '{upgrade_type}' no encontrado, usando superficie básica.")
            surf = pygame.Surface((UPGRADE_ICON_SIZE, UPGRADE_ICON_SIZE), pygame.SRCALPHA)
            pygame.draw.rect(surf, (255, 255, 255), surf.get_rect(), border_radius=12)
            return surf

    # ==========================================================
    # 🔹 Animación de caída
    # ==========================================================
    def start_fall(self, angle_rad, speed, max_distance):
        """Configura la caída visual del upgrade."""
        self.fall_angle = angle_rad
        self.fall_speed = speed
        self.fall_distance = max_distance
        self.fall_timer = 0.0
        self.active_fall = True

    def update(self, dt, game=None):
        """Actualiza animación de caída y posición."""
        if self.active_fall:
            self.fall_timer += dt
            if self.fall_timer < UPGRADE_FALL_DURATION:
                decay_factor = math.pow(UPGRADE_FALL_DECAY, self.fall_timer * 60)
                dx = math.cos(self.fall_angle) * self.fall_speed * dt * decay_factor
                dy = math.sin(self.fall_angle) * self.fall_speed * dt * decay_factor
                self.pos.x += dx
                self.pos.y += dy
                self.rect.center = self.pos
            else:
                self.active_fall = False

    # ==========================================================
    # 🔹 Generación desde zombie
    # ==========================================================
    @staticmethod
    def spawn_from_zombie(group, zombie):
        """Genera upgrades según el nuevo sistema unificado."""
        drop_config = ZOMBIE_UPGRADE_DROP_SYSTEM.get(zombie.type)
        if not drop_config:
            print(f"[WARN] No drop config for zombie type '{zombie.type}'")
            return

        origin = zombie.rect.center if hasattr(zombie, "rect") else tuple(zombie.pos)
        
        # ✅ Calcular cantidad de drops
        min_drops = drop_config["min_drops"]
        max_drops = drop_config["max_drops"]
        multi_chance = drop_config["multi_drop_chance"]
        
        # Siempre dropea el mínimo garantizado
        total_drops = min_drops
        
        # Intentar dropear cartas adicionales
        for _ in range(max_drops - min_drops):
            if random.random() * 100 < multi_chance:
                total_drops += 1
        
        # ✅ Generar cada upgrade
        for i in range(total_drops):
            upgrade_type = Upgrade.select_random_upgrade()
            if upgrade_type:
                u = Upgrade(upgrade_type, origin)
                angle = random.uniform(0, 2 * math.pi) + (i * (2 * math.pi / max(1, total_drops)))
                speed = random.uniform(UPGRADE_FALL_SPEED * 0.5, UPGRADE_FALL_SPEED * 0.9)
                distance = random.uniform(40, 75)
                u.start_fall(angle_rad=angle, speed=speed, max_distance=distance)
                group.add(u)
                print(f"[Upgrade] Dropped '{upgrade_type}' from {zombie.rarity.upper()} {zombie.type} (card {i+1}/{total_drops})")
                
    # ==========================================================
    # 🔹 Selección ponderada
    # ==========================================================
    @staticmethod
    def select_random_upgrade():
        """Selecciona un upgrade según probabilidades definidas en settings."""
        total = sum(UPGRADE_SPAWN_CHANCE.values())
        roll = random.uniform(0, total)
        current = 0.0
        for name, chance in UPGRADE_SPAWN_CHANCE.items():
            current += chance
            if roll <= current:
                return name
        return None