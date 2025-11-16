import random
import pygame

from entities.zombie import Zombie
from settings import (
    ZOMBIE_LEVEL_MIN_VARIATION,
    ZOMBIE_LEVEL_MAX_VARIATION,
    WORLD_WIDTH, WORLD_HEIGHT,
    ZOMBIE_RARITY_CHANCE,
    ZOMBIE_LEVEL_BASE_PER_WAVE,
    ZOMBIE_LEVEL_INCREMENT_PER_WAVE
)


class Spawner:
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
        self.in_wave = True
        self.spawn_timer = 0.0
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

            # Fin de ola si no quedan zombies
            if self.enemies_to_spawn <= 0 and len(self.game.zombies) == 0:
                self.in_wave = False
                self.wave_cooldown = self.time_between_waves
        else:
            if self.wave_cooldown > 0:
                self.wave_cooldown -= dt
            if self.wave_cooldown <= 0:
                self.start_next_wave()

    # ============================================================
    # 🎚 Nivel de zombie según ola
    # ============================================================
    def _choose_level_for_wave(self):
        """Nivel de zombie escalonado según ola y variación pequeña."""
        base_level = ZOMBIE_LEVEL_BASE_PER_WAVE + self.current_wave * ZOMBIE_LEVEL_INCREMENT_PER_WAVE
        variation = random.randint(ZOMBIE_LEVEL_MIN_VARIATION, ZOMBIE_LEVEL_MAX_VARIATION)
        lvl = int(base_level + variation)
        return max(1, lvl)


    # ============================================================
    # ⭐ Elegir rareza según probabilidades
    # ============================================================
    def choose_rarity(self):
        """Calcula rareza progresiva según ola."""
        r = random.random() * 100
        cumulative = 0

        # Escalar probabilidades según la ola
        wave_factor = min(self.current_wave / 20, 1.0)  # de 0 a 1
        adjusted_chances = {}
        for rarity, base_chance in ZOMBIE_RARITY_CHANCE.items():
            if rarity == "common":
                adjusted_chances[rarity] = max(base_chance * (1 - wave_factor), 5)
            else:
                adjusted_chances[rarity] = base_chance * wave_factor

        # Normalizar para sumar 100
        total = sum(adjusted_chances.values())
        for key in adjusted_chances:
            adjusted_chances[key] = adjusted_chances[key] / total * 100

        for rarity, chance in adjusted_chances.items():
            cumulative += chance
            if r <= cumulative:
                return rarity
        return "common"


    # ============================================================
    # 🧟 Spawn enemigo
    # ============================================================
    def spawn_enemy(self):
        pos = self._generate_spawn_pos()

        # Determinar tipo según ola y probabilidades
        z_type = self._choose_type()

        # Nivel según ola
        level = self._choose_level_for_wave()

        # Rareza
        rarity = self.choose_rarity()

        # Crear zombie
        z = Zombie(pos, ztype=z_type, level=level, rarity=rarity)
        self.game.zombies.add(z)
        print(f"[Spawner] Spawned {rarity.upper()} {z_type.upper()} (Lv.{level}) at {pos}")

    # ============================================================
    # 🗺 Generar posición de spawn lejos del jugador
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

            if pos.distance_to(player_pos) >= self.min_spawn_distance:
                return pos

        # Si no se encuentra, devolver la última generada
        return pos

    # ============================================================
    # 🧟 Determinar tipo de zombie según ola y probabilidad
    # ============================================================
    def _choose_type(self):
        t = "common"
        if self.current_wave >= 5 and random.random() < 0.15:
            t = "fast"
        if self.current_wave >= 8 and random.random() < 0.10:
            t = "tank"
        if self.current_wave % 10 == 0 and random.random() < 0.35:
            t = "boss"
        return t
