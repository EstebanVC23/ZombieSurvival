import pygame
import math
import time
import os
from settings import (
    WEAPON_BASE_DAMAGE,
    WEAPON_BASE_RPM,
    WEAPON_BASE_MAGAZINE,
    WEAPON_BASE_RESERVE_AMMO,
    WEAPON_BASE_RELOAD_TIME,
    BULLET_BASE_LIFETIME,
    ASSETS_SOUNDS,
)
from entities.bullet import Bullet

class Weapon:
    """Clase que controla el comportamiento del arma del jugador."""

    def __init__(self, owner, damage=None, rpm=None, ammo=None, reserve=None, level=1, reload_time=None):
        self.owner = owner
        self.damage = damage if damage is not None else WEAPON_BASE_DAMAGE
        self.rpm = rpm if rpm is not None else WEAPON_BASE_RPM
        self.max_ammo = ammo if ammo is not None else WEAPON_BASE_MAGAZINE
        self.reserve_ammo = reserve if reserve is not None else WEAPON_BASE_RESERVE_AMMO
        self.reload_time = reload_time if reload_time is not None else WEAPON_BASE_RELOAD_TIME
        self.level = level

        self.current_ammo = int(self.max_ammo)
        self.last_shot_time = 0.0
        self.is_reloading = False
        self.reload_timer = 0.0
        # cooldown en segundos entre disparos
        self.cooldown = 60.0 / max(1.0, float(self.rpm))

        # Sonido de disparo
        self.shot_sound = None
        self._load_shot_sound()

    def _load_shot_sound(self):
        path = os.path.join(ASSETS_SOUNDS, "shot.mp3")
        if os.path.exists(path):
            try:
                # Inicializar mixer sólo si no está inicializado
                if not pygame.mixer.get_init():
                    pygame.mixer.init()
                self.shot_sound = pygame.mixer.Sound(path)
                self.shot_sound.set_volume(0.2)
            except Exception as e:
                print(f"[WARN] No se pudo cargar sonido: {e}")
        else:
            # Ruta alternativa por compatibilidad
            alt = os.path.join("assets", "sounds", "shot.mp3")
            if os.path.exists(alt):
                try:
                    if not pygame.mixer.get_init():
                        pygame.mixer.init()
                    self.shot_sound = pygame.mixer.Sound(alt)
                    self.shot_sound.set_volume(0.2)
                except Exception as e:
                    print(f"[WARN] No se pudo cargar sonido alternativo: {e}")
            else:
                print(f"[INFO] No se encontró el sonido de disparo en {path}")

    def fire(self, pos, target, game):
        # No dispara si recargando
        if self.is_reloading:
            return None

        now = time.time()
        if now - self.last_shot_time < self.cooldown:
            return None

        if self.current_ammo <= 0:
            self.start_reload()
            return None

        # Asegurar Vector2
        pos_v = pygame.math.Vector2(pos)
        target_v = pygame.math.Vector2(target)
        dir_vec = target_v - pos_v
        if dir_vec.length_squared() == 0:
            dir_vec = pygame.math.Vector2(1, 0)
        else:
            dir_vec = dir_vec.normalize()

        # Crear bala con damage y lifetime por defecto del settings
        bullet = Bullet(pos_v, dir_vec, damage=self.damage, lifetime=BULLET_BASE_LIFETIME)
        # añadir al grupo
        game.bullets.add(bullet)

        self.current_ammo -= 1
        self.last_shot_time = now

        # Sonido: tocar el sonido brevemente (maxtime en ms)
        if self.shot_sound:
            try:
                ch = pygame.mixer.find_channel(True)
                ch.play(self.shot_sound, maxtime=int(0.5 * 1000))
            except Exception:
                pass

        return bullet

    # Recarga
    def start_reload(self):
        if not self.is_reloading and self.reserve_ammo > 0 and self.current_ammo < self.max_ammo:
            self.is_reloading = True
            self.reload_timer = 0.0

    def update(self, dt):
        if self.is_reloading:
            self.reload_timer += dt
            if self.reload_timer >= self.reload_time:
                self.finish_reload()

    def finish_reload(self):
        needed = int(self.max_ammo) - int(self.current_ammo)
        to_load = min(needed, int(self.reserve_ammo))
        self.current_ammo += to_load
        self.reserve_ammo -= to_load
        self.is_reloading = False
        self.reload_timer = 0.0

    # Upgrades
    def apply_fire_rate_bonus(self, value):
        # value asumido en RPM (incremento)
        self.rpm = min(1200, float(self.rpm) + float(value))
        self.cooldown = 60.0 / max(1.0, self.rpm)
        print(f"[UPGRADE] Nueva cadencia: {self.rpm} RPM")

    def apply_damage_bonus(self, value):
        self.damage += value
        print(f"[UPGRADE] Daño aumentado a {self.damage}")

    def apply_reload_bonus(self, factor):
        # factor <1 reduce el tiempo (por ejemplo 0.9)
        self.reload_time *= factor
        print(f"[UPGRADE] Tiempo de recarga reducido a {self.reload_time:.2f}s")

    def debug_stats(self):
        return {
            "damage": self.damage,
            "rpm": self.rpm,
            "cooldown": self.cooldown,
            "max_ammo": self.max_ammo,
            "current_ammo": self.current_ammo,
            "reserve_ammo": self.reserve_ammo,
            "reload_time": self.reload_time,
        }
