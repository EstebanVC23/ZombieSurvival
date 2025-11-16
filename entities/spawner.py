import random
import pygame
from entities.zombie import Zombie


class Spawner:
    """Sistema unificado de generación segura de enemigos."""

    def __init__(self, world_width, world_height):
        self.world_width = world_width
        self.world_height = world_height

    def spawn_far_from_player(self, player_pos, min_distance):
        """
        Genera una posición alejada del jugador dentro del mundo.
        """
        while True:
            x = random.randint(0, self.world_width)
            y = random.randint(0, self.world_height)
            pos = pygame.Vector2(x, y)

            if pos.distance_to(player_pos) >= min_distance:
                return (x, y)

    def spawn_at_world_edges(self, screen_w, screen_h, margin):
        """
        Spawnea zombies en los bordes de la pantalla actual.
        """
        side = random.choice(["top", "bottom", "left", "right"])

        if side == "top":
            pos = (random.randint(-margin, screen_w + margin), -margin)
        elif side == "bottom":
            pos = (random.randint(-margin, screen_w + margin), screen_h + margin)
        elif side == "left":
            pos = (-margin, random.randint(-margin, screen_h + margin))
        else:
            pos = (screen_w + margin, random.randint(-margin, screen_h + margin))

        return pos


class WaveManager:
    def __init__(self, game):
        self.game = game
        self.current_wave = 0
        self.time_between_waves = 3.0
        self.wave_cooldown = 0.0
        self.in_wave = False
        self.enemies_to_spawn = 0
        self.spawn_interval = 0.5
        self.spawn_timer = 0.0

        # Spawner seguro
        self.spawner = Spawner(game.world_width, game.world_height)

        # Distancia mínima para oleadas
        self.wave_min_distance = 550

    def start_next_wave(self):
        self.current_wave += 1
        base = 5 + int(self.current_wave * 3.5)
        self.enemies_to_spawn = base
        self.in_wave = True
        self.spawn_timer = 0.0

        print(f"[WaveManager] WAVE {self.current_wave} | spawn={self.enemies_to_spawn}")

    def update(self, dt):
        if self.in_wave:
            self.spawn_timer -= dt

            if self.spawn_timer <= 0 and self.enemies_to_spawn > 0:
                self.spawn_timer = self.spawn_interval
                self.spawn_enemy()
                self.enemies_to_spawn -= 1

            # Fin de oleada
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

    def spawn_enemy(self):
        """
        Spawnea un zombie lejos del jugador.
        """

        # Obtener spawn seguro en los bordes de pantalla
        sw, sh = self.game.screen_width, self.game.screen_height

        pos = self.spawner.spawn_at_world_edges(sw, sh, margin=80)

        # Rechazar si está demasiado cerca del jugador
        player_pos = self.game.player.pos
        while pygame.Vector2(pos).distance_to(player_pos) < self.wave_min_distance:
            pos = self.spawner.spawn_at_world_edges(sw, sh, margin=80)

        # Selección de tipo
        zt = "common"
        if self.current_wave >= 5 and random.random() < 0.12: zt = "fast"
        if self.current_wave >= 8 and random.random() < 0.08: zt = "tank"
        if self.current_wave % 10 == 0 and random.random() < 0.3: zt = "boss"

        z = Zombie(pos, ztype=zt)
        self.game.zombies.add(z)
