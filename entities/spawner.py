import random
import pygame

from entities.zombie import Zombie
from utils.math_utils import MathUtils
from settings import (
    ZOMBIE_LEVEL_MIN_VARIATION,
    ZOMBIE_LEVEL_MAX_VARIATION,
    WORLD_WIDTH, WORLD_HEIGHT,
    ZOMBIE_RARITY_CHANCE,
    ZOMBIE_LEVEL_BASE_PER_WAVE,
    ZOMBIE_LEVEL_INCREMENT_PER_WAVE
)


class Spawner:
    """Controlador de olas y generación de zombies."""

    def __init__(self, game):
        self.game = game

        self.current_wave = 0
        self.time_between_waves = 3.0
        self.wave_cooldown = 0.0

        self.in_wave = False
        self.enemies_to_spawn = 0

        self.spawn_interval = 0.5
        self.spawn_timer = 0.0

        # Distancia mínima desde el jugador
        self.min_spawn_distance = 450

    # ============================================================
    # 🚀 Iniciar nueva ola
    # ============================================================
    def start_next_wave(self):
        self.current_wave += 1
        self.enemies_to_spawn = 5 + int(self.current_wave * 3.5)
        self.spawn_timer = 0.0
        self.in_wave = True

        print(f"[Spawner] Wave {self.current_wave} started -> {self.enemies_to_spawn} zombies")

    # ============================================================
    # 🔄 Update general
    # ============================================================
    def update(self, dt):
        if self.in_wave:
            self.spawn_timer -= dt

            if self.spawn_timer <= 0 and self.enemies_to_spawn > 0:
                self.spawn_timer = self.spawn_interval
                self.spawn_enemy()
                self.enemies_to_spawn -= 1

            # Fin de ola cuando ya no quedan por spawnear ni zombies vivos
            if self.enemies_to_spawn <= 0 and len(self.game.zombies) == 0:
                self.in_wave = False
                self.wave_cooldown = self.time_between_waves

        else:
            if self.wave_cooldown > 0:
                self.wave_cooldown -= dt

            if self.wave_cooldown <= 0:
                self.start_next_wave()

    # ============================================================
    # 🎚 Nivel según ola
    # ============================================================
    def _choose_level_for_wave(self):
        base = ZOMBIE_LEVEL_BASE_PER_WAVE + (self.current_wave * ZOMBIE_LEVEL_INCREMENT_PER_WAVE)
        variation = random.randint(ZOMBIE_LEVEL_MIN_VARIATION, ZOMBIE_LEVEL_MAX_VARIATION)
        return max(1, int(base + variation))

    # ============================================================
    # ⭐ Rareza progresiva
    # ============================================================
    def choose_rarity(self):
        r = random.random() * 100
        cumulative = 0

        # Factor de progresión de 0 → 1
        wave_factor = min(self.current_wave / 20, 1.0)

        adjusted = {}
        for rarity, base in ZOMBIE_RARITY_CHANCE.items():
            if rarity == "common":
                adjusted[rarity] = max(base * (1 - wave_factor), 5)
            else:
                adjusted[rarity] = base * wave_factor

        total = sum(adjusted.values())
        for k in adjusted:
            adjusted[k] = adjusted[k] / total * 100

        for rarity, chance in adjusted.items():
            cumulative += chance
            if r <= cumulative:
                return rarity

        return "common"

    # ============================================================
    # 🧟 Spawn enemigo
    # ============================================================
    def spawn_enemy(self):
        pos = self._generate_spawn_pos()

        z_type = self._choose_type()
        level = self._choose_level_for_wave()
        rarity = self.choose_rarity()

        z = Zombie(pos, ztype=z_type, level=level, rarity=rarity)
        self.game.zombies.add(z)

        print(f"[Spawner] Spawned {rarity.upper()} {z_type.upper()} (Lv.{level}) at {pos}")

    # ============================================================
    # 🗺 Generar spawn lejos del jugador
    # ============================================================
    def _generate_spawn_pos(self):
        sw, sh = WORLD_WIDTH, WORLD_HEIGHT
        margin = 80

        side = random.choice(["top", "bottom", "left", "right"])
        player_pos = pygame.Vector2(self.game.player.pos)

        for _ in range(20):
            if side == "top":
                pos = pygame.Vector2(random.randint(0, sw), -margin)
            elif side == "bottom":
                pos = pygame.Vector2(random.randint(0, sw), sh + margin)
            elif side == "left":
                pos = pygame.Vector2(-margin, random.randint(0, sh))
            else:
                pos = pygame.Vector2(sw + margin, random.randint(0, sh))

            if MathUtils.distance(pos, player_pos) >= self.min_spawn_distance:
                return pos

        return pos  # fallback

    # ============================================================
    # 🧟 Tipo de zombie
    # ============================================================
    def _choose_type(self):
        if self.current_wave % 10 == 0 and random.random() < 0.35:
            return "boss"
        if self.current_wave >= 8 and random.random() < 0.10:
            return "tank"
        if self.current_wave >= 5 and random.random() < 0.15:
            return "fast"
        return "common"
