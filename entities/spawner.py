import random
import pygame
from entities.zombie import Zombie

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

    def start_next_wave(self):
        self.current_wave += 1
        base = 5 + int(self.current_wave * 3.5)
        self.enemies_to_spawn = base
        self.in_wave = True
        self.spawn_timer = 0.0
        print(f"[WaveManager] Wave {self.current_wave} started. Enemies to spawn: {self.enemies_to_spawn}")

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
            else:
                self.start_next_wave()

    def spawn_enemy(self):
        sw, sh = self.game.screen.get_size()
        margin = 60
        side = random.choice(["top", "bottom", "left", "right"])
        if side == "top":
            pos = (random.randint(-margin, sw+margin), -margin)
        elif side == "bottom":
            pos = (random.randint(-margin, sw+margin), sh + margin)
        elif side == "left":
            pos = (-margin, random.randint(-margin, sh+margin))
        else:
            pos = (sw + margin, random.randint(-margin, sh+margin))

        t = "common"
        if self.current_wave >= 5 and random.random() < 0.12:
            t = "fast"
        if self.current_wave >= 8 and random.random() < 0.08:
            t = "tank"
        if self.current_wave % 10 == 0 and random.random() < 0.3:
            t = "boss"

        z = Zombie(pos, ztype=t)
        self.game.zombies.add(z)
