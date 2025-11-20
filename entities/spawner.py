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
    SPAWNER_MULTIPLIER_WAVE_10,
    MAX_ZOMBIES_ON_MAP
)
import traceback


class Spawner:
    """Controlador principal de olas y spawn de zombies."""

    def __init__(self, game):
        self.game = game
        self.current_wave = 0

        # Cooldown entre olas
        self.time_between_waves = SPAWNER_TIME_BETWEEN_WAVES
        self.wave_cooldown = 0.0

        # Estado de la ola
        self.in_wave = False
        self.enemies_to_spawn = 0

        # Spawning interval
        self.spawn_interval = SPAWNER_SPAWN_INTERVAL
        self.spawn_timer = 0.0

        # Distancia mínima para spawnear
        self.min_spawn_distance = SPAWNER_MIN_DISTANCE_TO_PLAYER

        print("[Spawner] Inicializado")
        print("[Spawner] Spawneando 8 zombies iniciales (solo para poblar el mapa)...")
        self.spawn_initial_zombies(8)  # Solo para poblar mapa, no cuenta para ola 1

    # ============================================================
    # SPAWN INICIAL (seguro, lejos del jugador)
    # ============================================================
    def spawn_initial_zombies(self, count):
        for _ in range(count):
            try:
                pos = self._generate_spawn_pos_initial()
                z_type = self._choose_type_for_initial_wave()
                level = self._choose_level_for_wave()
                rarity = self.choose_rarity()

                if rarity is None:
                    print("[WARNING] Rareza inválida en spawn inicial.")
                    continue

                z = Zombie(pos, z_type, level=level, rarity=rarity)
                self.game.zombies.add(z)
                print(f"[Init] {rarity.upper()} {z_type.upper()} (Lv.{level}) en {pos}")

            except Exception:
                traceback.print_exc()

    def _generate_spawn_pos_initial(self):
        """Spawnea en los bordes y nunca cerca del jugador."""
        try:
            sw, sh = WORLD_WIDTH, WORLD_HEIGHT
            margin = 150
            player_pos = pygame.Vector2(self.game.player.pos)

            for _ in range(40):
                side = random.choice(["top", "bottom", "left", "right"])

                if side == "top":
                    pos = pygame.Vector2(random.randint(0, sw), -margin)
                elif side == "bottom":
                    pos = pygame.Vector2(random.randint(0, sw), sh + margin)
                elif side == "left":
                    pos = pygame.Vector2(-margin, random.randint(0, sh))
                else:
                    pos = pygame.Vector2(sw + margin, random.randint(0, sh))

                if pos.distance_to(player_pos) >= 600:
                    return pos

            return pygame.Vector2(sw + margin, sh + margin)
        except Exception:
            traceback.print_exc()

    # ============================================================
    # INICIO DE OLA
    # ============================================================
    def start_next_wave(self):
        try:
            if len(self.game.zombies) >= MAX_ZOMBIES_ON_MAP:
                print("[Spawner] Mapa lleno, posponiendo inicio de ola...")
                return

            self.current_wave += 1

            # Enemies to spawn SOLO para la ola actual
            self.enemies_to_spawn = int(self.current_wave * 3.5) + 5

            self.spawn_timer = 0.0
            self.in_wave = True

            print(f"\n[Spawner] ==== WAVE {self.current_wave} ====")
            print(f"[Spawner] Enemigos a spawnear: {self.enemies_to_spawn}")
            print(f"[Spawner] Zombies en mapa actualmente: {len(self.game.zombies)}")
            print(f"[Spawner] Máximo en mapa: {MAX_ZOMBIES_ON_MAP}")

        except Exception:
            traceback.print_exc()

    # ============================================================
    # UPDATE PRINCIPAL DEL SPAWNER
    # ============================================================
    def update(self, dt):
        try:
            if self.in_wave:
                self.spawn_timer -= dt
                zombies_alive = len(self.game.zombies)

                # Si el mapa está lleno → no restar enemies_to_spawn
                if zombies_alive >= MAX_ZOMBIES_ON_MAP:
                    self.spawn_timer = 0.1  # micro delay
                    return

                # Intento de spawn
                if self.spawn_timer <= 0 and self.enemies_to_spawn > 0:
                    if zombies_alive < MAX_ZOMBIES_ON_MAP:
                        self.spawn_enemy()
                        self.enemies_to_spawn -= 1
                    else:
                        print("[Spawner] Mapa lleno, esperando espacio para spawn...")

                    self.spawn_timer = self.spawn_interval

                # Fin de ola
                if self.enemies_to_spawn <= 0 and zombies_alive == 0:
                    print("[Spawner] Ola completada!")
                    self.in_wave = False
                    self.wave_cooldown = self.time_between_waves

            else:
                # Cooldown entre olas
                if self.wave_cooldown > 0:
                    self.wave_cooldown -= dt

                if self.wave_cooldown <= 0:
                    if len(self.game.zombies) < MAX_ZOMBIES_ON_MAP:
                        self.start_next_wave()

        except Exception:
            traceback.print_exc()

    # ============================================================
    # GENERACIÓN DE ESTADÍSTICAS DEL ZOMBIE
    # ============================================================
    def _choose_level_for_wave(self):
        try:
            base = ZOMBIE_LEVEL_BASE_PER_WAVE + (self.current_wave * ZOMBIE_LEVEL_INCREMENT_PER_WAVE)
            variation = random.randint(ZOMBIE_LEVEL_MIN_VARIATION, ZOMBIE_LEVEL_MAX_VARIATION)
            level = max(1, int(base + variation))
            return level
        except Exception:
            traceback.print_exc()

    def choose_rarity(self):
        try:
            total = sum(ZOMBIE_RARITY_CHANCE.values())
            r = random.uniform(0, total)
            cumulative = 0

            for rarity, chance in ZOMBIE_RARITY_CHANCE.items():
                cumulative += chance
                if r <= cumulative:
                    return rarity
        except Exception:
            traceback.print_exc()

    # ============================================================
    # SPAWN NORMAL
    # ============================================================
    def spawn_enemy(self):
        try:
            pos = self._generate_spawn_pos()
            z_type = self._choose_type()
            level = self._choose_level_for_wave()
            rarity = self.choose_rarity()

            if rarity is None:
                print("[WARNING] Rareza inválida, ignorando spawn.")
                return

            z = Zombie(pos, z_type, level=level, rarity=rarity)
            self.game.zombies.add(z)

            print(f"[Spawn] {rarity.upper()} {z_type.upper()} (Lv.{level}) en {pos}")
        except Exception:
            traceback.print_exc()

    def _generate_spawn_pos(self):
        try:
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
        except Exception:
            traceback.print_exc()

    # ============================================================
    # TIPOS DE ZOMBIE
    # ============================================================
    def _choose_type_for_initial_wave(self):
        try:
            base_probs = ZOMBIE_SPAWN_CHANCE_BY_WAVE["1-5"].copy()
            base_probs = {k: v for k, v in base_probs.items() if v > 0}

            total = sum(base_probs.values())
            if total == 0:
                return "common"

            types = list(base_probs.keys())
            weights = [v / total for v in base_probs.values()]
            return random.choices(types, weights=weights, k=1)[0]

        except Exception:
            traceback.print_exc()

    def _choose_type(self):
        try:
            if self.current_wave <= 5:
                base_probs = ZOMBIE_SPAWN_CHANCE_BY_WAVE["1-5"].copy()
            elif 6 <= self.current_wave <= 7:
                base_probs = ZOMBIE_SPAWN_CHANCE_BY_WAVE["6-7"].copy()
            elif 8 <= self.current_wave <= 9:
                base_probs = ZOMBIE_SPAWN_CHANCE_BY_WAVE["8-9"].copy()
            else:
                base_probs = ZOMBIE_SPAWN_CHANCE_BY_WAVE["10+"].copy()

            if self.current_wave >= 10 and self.current_wave % 10 == 0:
                print(f"[Spawner] Wave {self.current_wave}: multiplicadores aplicados.")
                for k, mult in SPAWNER_MULTIPLIER_WAVE_10.items():
                    if k in base_probs:
                        base_probs[k] *= mult

            base_probs = {k: v for k, v in base_probs.items() if v > 0}
            total = sum(base_probs.values())
            if total == 0:
                return "common"

            types = list(base_probs.keys())
            weights = [v / total for v in base_probs.values()]
            return random.choices(types, weights=weights, k=1)[0]

        except Exception:
            traceback.print_exc()
