import pygame
import os
from settings import *
from utils.helpers import load_image_safe
from core.upgrade import Upgrade


class Zombie(pygame.sprite.Sprite):
    TYPE_STATS = {
        "common": {"hp": ZOMBIE_COMMON_HP, "speed": ZOMBIE_COMMON_SPEED, "radius": ZOMBIE_COMMON_SIZE // 2, "damage": ZOMBIE_COMMON_DAMAGE},
        "fast":   {"hp": ZOMBIE_FAST_HP, "speed": ZOMBIE_FAST_SPEED, "radius": ZOMBIE_FAST_SIZE // 2, "damage": ZOMBIE_FAST_DAMAGE},
        "tank":   {"hp": ZOMBIE_TANK_HP, "speed": ZOMBIE_TANK_SPEED, "radius": ZOMBIE_TANK_SIZE // 2, "damage": ZOMBIE_TANK_DAMAGE},
        "boss":   {"hp": ZOMBIE_BOSS_HP, "speed": ZOMBIE_BOSS_SPEED, "radius": ZOMBIE_BOSS_SIZE // 2, "damage": ZOMBIE_BOSS_DAMAGE},
    }

    def __init__(self, pos, ztype="common"):
        super().__init__()
        stats = self.TYPE_STATS.get(ztype, self.TYPE_STATS["common"])

        self.type = ztype
        self.hp = stats["hp"]
        self.speed = stats["speed"]
        self.radius = stats["radius"]
        self.damage = stats["damage"]
        self.direction = "front"
        self.pos = pygame.Vector2(pos)

        # Estado de muerte
        self.dead = False
        self.dead_timer = 0.0
        self.fade = 0.0
        self.dead_image = None

        # Imagen base (círculo si no hay sprites)
        self.image = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (150, 180, 40), (self.radius, self.radius), self.radius)
        self.rect = self.image.get_rect(center=(round(self.pos.x), round(self.pos.y)))

        # Frames de animación (vivo)
        base = os.path.join("zombie", "common")
        f = load_image_safe(os.path.join(base, "common_frente.png"))
        b = load_image_safe(os.path.join(base, "common_espalda.png"))
        s = load_image_safe(os.path.join(base, "common_lateral.png"))

        self.frames = {}
        if f and b and s:
            self.frames["front"] = self._prep(f)
            self.frames["back"] = self._prep(b)
            self.frames["left"] = self._prep(s)
            self.frames["right"] = pygame.transform.flip(self.frames["left"], True, False)
            self.image = self.frames["front"]

        # Sprite de muerte (preparado)
        self.dead_sprite = None
        raw_dead = load_image_safe(os.path.join("zombie", "common", "dead.png"))
        if raw_dead:
            self.dead_sprite = self._prep(raw_dead)

        # ------------------------
        # Audio por proximidad
        # ------------------------
        self.sound = None
        # usar ASSETS_SOUNDS (de settings)
        sound_path = os.path.join(ASSETS_SOUNDS, "zombie_common.mp3")
        if os.path.exists(sound_path):
            try:
                # inicializar mixer si aún no
                if not pygame.mixer.get_init():
                    pygame.mixer.init()
                # cargar sonido
                self.sound = pygame.mixer.Sound(sound_path)
                # iniciar con volumen 0 y en loop; iremos controlando volumen por distancia
                self.sound.set_volume(0.0)
                self.sound.play(loops=-1)
            except Exception:
                self.sound = None
        else:
            self.sound = None

        # distancia máxima a la que se oye este zombie (ajustable)
        self.max_sound_distance = max(600, (WORLD_WIDTH + WORLD_HEIGHT) / 10)

    @property
    def x(self):
        return self.pos.x

    @property
    def y(self):
        return self.pos.y

    # ------------------------------------------------------------------
    # Limpia fondo claro y escala la imagen al tamaño del zombie
    # ------------------------------------------------------------------
    def _prep(self, img):
        img = pygame.transform.scale(img, (self.radius * 2, self.radius * 2))
        clean = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
        clean.blit(img, (0, 0))
        clean.lock()
        for x in range(clean.get_width()):
            for y in range(clean.get_height()):
                r, g, b, a = clean.get_at((x, y))
                if (r + g + b) / 3 > 190 and a > 0:
                    clean.set_at((x, y), (0, 0, 0, 0))
        clean.unlock()
        return clean

    # ------------------------------------------------------------------
    # Mostrar transición al cadáver con fade
    # ------------------------------------------------------------------
    def _show_death_sprite(self, dt):
        if not self.dead_image:
            return
        if self.fade < 255:
            self.fade += 400 * dt
            if self.fade > 255:
                self.fade = 255
        corpse = self.dead_image.copy()
        corpse.set_alpha(int(self.fade))
        self.image = corpse
        # centrar en la posición del zombie al morir
        self.rect = self.image.get_rect(center=(round(self.pos.x), round(self.pos.y)))

    # ------------------------------------------------------------------
    # Pause / Resume del sonido del zombie
    # ------------------------------------------------------------------
    def pause_sound(self):
        """Detiene solo el sonido del zombie durante la pausa."""
        if self.sound:
            try:
                # Stop detiene la reproducción; guardamos que quedó parado
                self.sound.stop()
            except Exception:
                pass

    def resume_sound(self):
        """Reanuda el sonido del zombie al quitar pausa."""
        if self.sound:
            try:
                # Reproducir en loop y mantener volumen controlado por update
                self.sound.play(loops=-1)
            except Exception:
                pass

    # ------------------------------------------------------------------
    # Update principal (respeta pausa desde game.paused)
    # ------------------------------------------------------------------
    def update(self, dt, game):
        # Si zombie está muerto, mostrar cadáver y terminar
        if self.dead:
            self.dead_timer += dt
            self._show_death_sprite(dt)
            # detener sonido si aún suena
            if self.sound:
                try:
                    self.sound.set_volume(0.0)
                except Exception:
                    pass
            # desaparecer después de X s
            if self.dead_timer >= 4.0:
                self.kill()
            return

        # Si no hay jugador, no actualizamos ni sonido
        if not game.player:
            return

        # Si el juego está pausado: detener sonido y no mover ni cambiar volumen
        if getattr(game, "paused", False):
            # detener audio del zombie (no reseteamos más datos)
            self.pause_sound()
            return
        else:
            # si no está en pausa y el sonido no está sonando, arrancarlo
            if self.sound and self.sound.get_num_channels() == 0:
                self.resume_sound()

        # Movimiento hacia el jugador
        dir_vec = game.player.pos - self.pos
        if dir_vec.length_squared() > 0:
            d = dir_vec.normalize()
            self.pos += d * self.speed * dt
            self.rect.center = (round(self.pos.x), round(self.pos.y))
            self._set_dir(d)

        # Sprite vivo según dirección
        if self.frames:
            self.image = self.frames[self.direction]

        # Colisión con jugador (si implementa collide_circle)
        try:
            if pygame.sprite.collide_circle(self, game.player):
                game.player.take_damage(self.damage * dt)
        except Exception:
            pass

        # Ajustar volumen por proximidad al jugador
        if self.sound:
            dist = self.pos.distance_to(game.player.pos)
            if dist < self.max_sound_distance:
                vol = max(0.0, min(1.0, (1 - (dist / self.max_sound_distance)) ** 2))
            else:
                vol = 0.0
            try:
                self.sound.set_volume(vol)
            except Exception:
                pass

    # ------------------------------------------------------------------
    # Dirección según vector (para elegir sprite)
    # ------------------------------------------------------------------
    def _set_dir(self, v):
        dx, dy = v.x, v.y
        if abs(dx) > abs(dy):
            self.direction = "right" if dx > 0 else "left"
        else:
            self.direction = "front" if dy > 0 else "back"

    # ------------------------------------------------------------------
    # Recibir daño y morir -> preparar cadáver rotado + fade
    # ------------------------------------------------------------------
    def take_damage(self, dmg, game=None):
        if self.dead:
            return
        self.hp -= dmg
        if self.hp > 0:
            return

        # detener sonido inmediatamente
        if self.sound:
            try:
                self.sound.stop()
            except Exception:
                pass

        # soltar upgrade si aplica
        if game:
            try:
                Upgrade.spawn_from_zombie(game.upgrades, self)
            except Exception:
                pass

        # marcar muerto y preparar datos del cadáver
        self.dead = True
        self.dead_timer = 0.0
        self.fade = 0.0

        # rotar sprite de muerte según dirección
        if self.dead_sprite:
            if self.direction == "front":
                rotated = self.dead_sprite
            elif self.direction == "back":
                rotated = pygame.transform.rotate(self.dead_sprite, 180)
            elif self.direction == "left":
                rotated = pygame.transform.rotate(self.dead_sprite, -90)
            elif self.direction == "right":
                rotated = pygame.transform.rotate(self.dead_sprite, 90)
            else:
                rotated = self.dead_sprite
        else:
            # fallback: clonar la imagen actual
            rotated = self.image.copy()

        self.dead_image = rotated

        # quitar "física" / colisión: reducir radius y daño
        self.radius = 1
        self.damage = 0
