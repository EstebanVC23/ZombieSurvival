import random
import pygame

from entities.zombie import Zombie
from settings import (
    ZOMBIE_LEVEL_MIN_VARIATION,
    ZOMBIE_LEVEL_MAX_VARIATION,
    WORLD_WIDTH, WORLD_HEIGHT,
    ZOMBIE_RARITY_CHANCE  # 🔥 antes era RARITY_TABLE
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

        # ⚠️ Nueva regla: distancia mínima entre jugador y spawn
        self.min_spawn_distance = 450

    # ============================================================
    # 🚀 Iniciar nueva ola
    # ============================================================
    def start_next_wave(self):
        self.current_wave += 1

        base = 5 + int(self.current_wave * 3.5)

        self.enemies_to_spawn = base
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

            # Fin ola si ya no quedan zombies
            if self.enemies_to_spawn <= 0 and len(self.game.zombies) == 0:
                self.in_wave = False
                self.wave_cooldown = self.time_between_waves

        else:
            if self.wave_cooldown > 0:
                self.wave_cooldown -= dt
                if self.wave_cooldown <= 0:
                    self.start_next_wave()
            else:
                self.start_next_wave()

    # ============================================================
    # 🎚 Sistema de niveles
    # ============================================================
    def _choose_level_for_wave(self):
        """Calcula el nivel de un zombie según la ola con variación."""
        variation = random.randint(
            ZOMBIE_LEVEL_MIN_VARIATION,
            ZOMBIE_LEVEL_MAX_VARIATION
        )
        lvl = self.current_wave + variation
        return max(1, lvl)


    # ============================================================
    # ⭐ Elegir rareza según probabilidades
    # ============================================================
    def choose_rarity(self):
        r = random.random() * 100
        cumulative = 0
        for rarity, chance in ZOMBIE_RARITY_CHANCE.items():
            cumulative += chance
            if r <= cumulative:
                return rarity
        return "common"

    # ============================================================
    # 🧟 Spawn enemigo
    # ============================================================
    def spawn_enemy(self):
        sw, sh = WORLD_WIDTH, WORLD_HEIGHT
        margin = 80

        # ----------------------------
        # Elegir lado de aparición
        # ----------------------------
        side = random.choice(["top", "bottom", "left", "right"])

        if side == "top":
            pos = (random.randint(0, sw), -margin)
        elif side == "bottom":
            pos = (random.randint(0, sw), sh + margin)
        elif side == "left":
            pos = (-margin, random.randint(0, sh))
        else:
            pos = (sw + margin, random.randint(0, sh))

        # ----------------------------
        # Evitar spawns cerca del jugador
        # ----------------------------
        player_pos = pygame.Vector2(self.game.player.pos)

        for _ in range(20):
            if pygame.Vector2(pos).distance_to(player_pos) >= self.min_spawn_distance:
                break

            if side == "top":
                pos = (random.randint(0, sw), -margin)
            elif side == "bottom":
                pos = (random.randint(0, sw), sh + margin)
            elif side == "left":
                pos = (-margin, random.randint(0, sh))
            else:
                pos = (sw + margin, random.randint(0, sh))

        # ----------------------------
        # Selección del tipo original
        # ----------------------------
        t = "common"

        if self.current_wave >= 5 and random.random() < 0.15:
            t = "fast"

        if self.current_wave >= 8 and random.random() < 0.10:
            t = "tank"

        if self.current_wave % 10 == 0 and random.random() < 0.35:
            t = "boss"

        # ----------------------------
        # Nivel según ola
        # ----------------------------
        level = self._choose_level_for_wave()

        # ----------------------------
        # ⭐ Nueva: rareza
        # ----------------------------
        rarity = self.choose_rarity()

        # ----------------------------
        # Crear zombie final
        # ----------------------------
        z = Zombie(pos, ztype=t, level=level, rarity=rarity)
        self.game.zombies.add(z)

        print(f"[Spawner] Spawned {rarity.upper()} {t.upper()} (Lv.{level}) at {pos}")
