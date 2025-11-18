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
    ZOMBIE_LEVEL_INCREMENT_PER_WAVE,
    SPAWNER_TIME_BETWEEN_WAVES,
    SPAWNER_SPAWN_INTERVAL,
    SPAWNER_MIN_DISTANCE_TO_PLAYER,
    ZOMBIE_SPAWN_CHANCE_BY_WAVE,
    SPAWNER_MULTIPLIER_WAVE_10
)

class Spawner:
    """Controlador de olas y generación de zombies."""

    def __init__(self, game):
        self.game = game
        self.current_wave = 0
        self.time_between_waves = SPAWNER_TIME_BETWEEN_WAVES
        self.wave_cooldown = 0.0

        self.in_wave = False
        self.enemies_to_spawn = 0

        self.spawn_interval = SPAWNER_SPAWN_INTERVAL
        self.spawn_timer = 0.0

        self.min_spawn_distance = SPAWNER_MIN_DISTANCE_TO_PLAYER

        # Spawn inicial usando probabilidades de ola 1
        self.spawn_initial_zombies(8)

    # ============================================================
    # Spawn inicial respetando probabilidades de la ola 1
    # ============================================================
    def spawn_initial_zombies(self, count):
        for _ in range(count):
            pos = self._generate_spawn_pos_initial()
            z_type = self._choose_type_for_initial_wave()
            level = self._choose_level_for_wave()
            rarity = self.choose_rarity()
            if rarity is None:
                continue
            z = Zombie(pos, z_type, level=level, rarity=rarity)
            self.game.zombies.add(z)
            print(f"[Spawner] Spawned initial {rarity.upper()} {z_type.upper()} (Lv.{level}) at {pos}")

    def _generate_spawn_pos_initial(self):
        """Posiciones iniciales lejos del jugador."""
        for _ in range(40):
            x = random.randint(0, WORLD_WIDTH)
            y = random.randint(0, WORLD_HEIGHT)
            pos = pygame.Vector2(x, y)
            if pos.distance_to(self.game.player.pos) >= 600:
                return pos
        return pygame.Vector2(WORLD_WIDTH, WORLD_HEIGHT)

    # ============================================================
    # Iniciar nueva ola
    # ============================================================
    def start_next_wave(self):
        self.current_wave += 1
        self.enemies_to_spawn = 5 + int(self.current_wave * 3.5)
        self.spawn_timer = 0.0
        self.in_wave = True
        print(f"[Spawner] Wave {self.current_wave} started -> {self.enemies_to_spawn} zombies")

    # ============================================================
    # Update general
    # ============================================================
    def update(self, dt):
        if self.in_wave:
            self.spawn_timer -= dt

            if self.spawn_timer <= 0 and self.enemies_to_spawn > 0:
                self.spawn_timer = self.spawn_interval
                self.spawn_enemy()
                self.enemies_to_spawn -= 1

            if self.enemies_to_spawn <= 0 and len(self.game.zombies) == 0:
                self.in_wave = False
                self.wave_cooldown = self.time_between_waves

        else:
            if self.wave_cooldown > 0:
                self.wave_cooldown -= dt

            if self.wave_cooldown <= 0:
                self.start_next_wave()

    # ============================================================
    # Nivel según ola
    # ============================================================
    def _choose_level_for_wave(self):
        base = ZOMBIE_LEVEL_BASE_PER_WAVE + (self.current_wave * ZOMBIE_LEVEL_INCREMENT_PER_WAVE)
        variation = random.randint(ZOMBIE_LEVEL_MIN_VARIATION, ZOMBIE_LEVEL_MAX_VARIATION)
        return max(1, int(base + variation))

    # ============================================================
    # Rareza progresiva
    # ============================================================
    def choose_rarity(self):
        total = sum(ZOMBIE_RARITY_CHANCE.values())
        r = random.uniform(0, total)
        cumulative = 0
        for rarity, chance in ZOMBIE_RARITY_CHANCE.items():
            cumulative += chance
            if r <= cumulative:
                return rarity

    # ============================================================
    # Spawn enemigo
    # ============================================================
    def spawn_enemy(self):
        pos = self._generate_spawn_pos()
        z_type = self._choose_type()
        level = self._choose_level_for_wave()
        rarity = self.choose_rarity()

        if rarity is None:
            print("[Spawner] No valid rarity, skipping spawn")
            return

        z = Zombie(pos, z_type, level=level, rarity=rarity)
        self.game.zombies.add(z)
        print(f"[Spawner] Spawned {rarity.upper()} {z_type.upper()} (Lv.{level}) at {pos}")

    # ============================================================
    # Generar spawn lejos del jugador
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

        return pos

    # ============================================================
    # Tipo de zombie
    # ============================================================
    def _choose_type_for_initial_wave(self):
        """Usado solo para los primeros spawns iniciales (ola 1)"""
        base_probs = ZOMBIE_SPAWN_CHANCE_BY_WAVE["1-5"].copy()
        # Filtrar probabilidades cero
        base_probs = {k: v for k, v in base_probs.items() if v > 0}
        total = sum(base_probs.values())
        if total == 0:
            return "common"
        types = list(base_probs.keys())
        weights = [v / total for v in base_probs.values()]
        return random.choices(types, weights=weights, k=1)[0]

    def _choose_type(self):
        """Escoge tipo según ola actual y multiplicadores"""
        # Probabilidades base por rango de ola
        if self.current_wave <= 5:
            base_probs = ZOMBIE_SPAWN_CHANCE_BY_WAVE["1-5"].copy()
        elif 6 <= self.current_wave <= 7:
            base_probs = ZOMBIE_SPAWN_CHANCE_BY_WAVE["6-7"].copy()
        elif 8 <= self.current_wave <= 9:
            base_probs = ZOMBIE_SPAWN_CHANCE_BY_WAVE["8-9"].copy()
        else:
            base_probs = ZOMBIE_SPAWN_CHANCE_BY_WAVE["10+"].copy()

        # Aplicar multiplicador para olas múltiplo de 10
        if self.current_wave >= 10 and self.current_wave % 10 == 0:
            for k, mult in SPAWNER_MULTIPLIER_WAVE_10.items():
                if k in base_probs:
                    base_probs[k] *= mult

        # Filtrar probabilidades cero
        base_probs = {k: v for k, v in base_probs.items() if v > 0}

        # Normalizar
        total = sum(base_probs.values())
        if total == 0:
            return "common"
        types = list(base_probs.keys())
        weights = [v / total for v in base_probs.values()]
        return random.choices(types, weights=weights, k=1)[0]
