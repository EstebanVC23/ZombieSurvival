import pygame
import os
import random

from utils.math_utils import MathUtils
from utils.movement_utils import MovementUtils
from utils.sound_utils import SoundUtils
from utils.helpers import load_image_safe, clean_image_background, load_sound

from settings import (
    WORLD_WIDTH, WORLD_HEIGHT,
    ZOMBIE_COMMON_HP, ZOMBIE_COMMON_SPEED, ZOMBIE_COMMON_SIZE, ZOMBIE_COMMON_DAMAGE,
    ZOMBIE_FAST_HP, ZOMBIE_FAST_SPEED, ZOMBIE_FAST_SIZE, ZOMBIE_FAST_DAMAGE,
    ZOMBIE_TANK_HP, ZOMBIE_TANK_SPEED, ZOMBIE_TANK_SIZE, ZOMBIE_TANK_DAMAGE,
    ZOMBIE_BOSS_HP, ZOMBIE_BOSS_SPEED, ZOMBIE_BOSS_SIZE, ZOMBIE_BOSS_DAMAGE,
    ZOMBIE_RARITY_CHANCE, ZOMBIE_RARITY_MULT, ZOMBIE_RARITY_UPGRADE_COUNT,
    ZOMBIE_RARITY_SCORE_MULT, ZOMBIE_RARITY_DROP_BONUS,
    ZOMBIE_SCORE_VALUES
)


# ================================================================
#   SISTEMA DE STATS
# ================================================================
class ZombieStats:

    TYPE_STATS = {
        "common": {"hp": ZOMBIE_COMMON_HP, "speed": ZOMBIE_COMMON_SPEED, "radius": ZOMBIE_COMMON_SIZE//2, "damage": ZOMBIE_COMMON_DAMAGE},
        "fast":   {"hp": ZOMBIE_FAST_HP,   "speed": ZOMBIE_FAST_SPEED,   "radius": ZOMBIE_FAST_SIZE//2,   "damage": ZOMBIE_FAST_DAMAGE},
        "tank":   {"hp": ZOMBIE_TANK_HP,   "speed": ZOMBIE_TANK_SPEED,   "radius": ZOMBIE_TANK_SIZE//2,   "damage": ZOMBIE_TANK_DAMAGE},
        "boss":   {"hp": ZOMBIE_BOSS_HP,   "speed": ZOMBIE_BOSS_SPEED,   "radius": ZOMBIE_BOSS_SIZE//2,   "damage": ZOMBIE_BOSS_DAMAGE},
    }

    LEVEL_UP_STATS = {
        "common": {"hp": 3,  "damage": 2,  "speed": 1.5},
        "fast":   {"hp": 2,  "damage": 1,  "speed": 4},
        "tank":   {"hp": 8,  "damage": 4,  "speed": 0.8},
        "boss":   {"hp": 20, "damage": 10, "speed": 1},
    }

    RARITY_TABLE = [
        ("common",    ZOMBIE_RARITY_CHANCE["common"]),
        ("uncommon",  ZOMBIE_RARITY_CHANCE["uncommon"]),
        ("rare",      ZOMBIE_RARITY_CHANCE["rare"]),
        ("epic",      ZOMBIE_RARITY_CHANCE["epic"]),
        ("legendary", ZOMBIE_RARITY_CHANCE["legendary"]),
    ]

    @staticmethod
    def roll_rarity():
        r = random.random() * 100
        acc = 0
        for rarity, chance in ZombieStats.RARITY_TABLE:
            acc += chance
            if r <= acc:
                return rarity
        return "common"

    @staticmethod
    def build(type_name, level, rarity):

        base = ZombieStats.TYPE_STATS[type_name]
        hp = base["hp"]
        speed = base["speed"]
        dmg = base["damage"]
        radius = base["radius"]

        # ----------------------------- RAREZA
        rarity_mult = ZOMBIE_RARITY_MULT[rarity]
        possible = ["hp", "speed", "damage"]
        n_upgrades = ZOMBIE_RARITY_UPGRADE_COUNT[rarity]
        chosen = random.sample(possible, n_upgrades)

        # Aplicar mejoras
        if "hp" in chosen: hp *= rarity_mult
        if "speed" in chosen: speed *= rarity_mult
        if "damage" in chosen: dmg *= rarity_mult

        # ----------------------------- NIVEL
        if level > 1:
            lv = ZombieStats.LEVEL_UP_STATS[type_name]
            hp += lv["hp"] * (level - 1)
            dmg += lv["damage"] * (level - 1)
            speed += lv["speed"] * (level - 1)

        return {
            "hp": hp,
            "speed": speed,
            "damage": dmg,
            "radius": radius
        }


# ================================================================
#   SISTEMA DE SPRITES
# ================================================================
class ZombieSprites:
    def __init__(self, type_name, radius):
        self.radius = radius
        base = os.path.join("zombie", "common")  # TODO: soportar sprites por tipo

        f = load_image_safe(os.path.join(base, "common_frente.png"))
        b = load_image_safe(os.path.join(base, "common_espalda.png"))
        s = load_image_safe(os.path.join(base, "common_lateral.png"))

        self.frames = {}
        if f and b and s:
            self.frames["front"] = clean_image_background(pygame.transform.scale(f, (radius*2, radius*2)))
            self.frames["back"] = clean_image_background(pygame.transform.scale(b, (radius*2, radius*2)))
            self.frames["left"] = clean_image_background(pygame.transform.scale(s, (radius*2, radius*2)))
            self.frames["right"] = pygame.transform.flip(self.frames["left"], True, False)

        raw_dead = load_image_safe(os.path.join(base, "dead.png"))
        self.dead_sprite = (
            clean_image_background(pygame.transform.scale(raw_dead, (radius*2, radius*2)))
            if raw_dead else None
        )

    def get_frame(self, direction):
        return self.frames.get(direction)

    def get_dead(self, direction):
        img = self.dead_sprite
        if not img:
            return None
        if direction == "back": return pygame.transform.rotate(img, 180)
        if direction == "left": return pygame.transform.rotate(img, -90)
        if direction == "right": return pygame.transform.rotate(img, 90)
        return img


# ================================================================
#   SISTEMA DE SONIDO
# ================================================================
class ZombieSound:
    def __init__(self):
        self.sound = load_sound("zombie_common.mp3", volume=0.0)
        if self.sound:
            try:
                self.sound.play(loops=-1)
            except: pass

        self.max_dist = max(600, (WORLD_WIDTH + WORLD_HEIGHT) / 10)

    def update_volume(self, zombie_pos, player_pos):
        if not self.sound:
            return
        dist = zombie_pos.distance_to(player_pos)
        SoundUtils.apply_distance_volume(self.sound, dist, self.max_dist)

    def stop(self):
        if not self.sound:
            return
        try:
            self.sound.stop()
        except:
            pass


# ================================================================
#   ZOMBIE (CLASE PRINCIPAL)
# ================================================================
class Zombie(pygame.sprite.Sprite):

    def __init__(self, pos, ztype="common", level=1, rarity=None):
        super().__init__()

        # ----------------------------- Posición
        self.pos = pygame.Vector2(pos)
        self.direction = "front"
        self.dead = False
        self.dead_timer = 0
        self.fade = 0

        # ----------------------------- RAREZA
        self.type = ztype
        self.level = level
        self.rarity = rarity if rarity else ZombieStats.roll_rarity()

        # ----------------------------- STATS
        stats = ZombieStats.build(ztype, level, self.rarity)
        self.hp = stats["hp"]
        self.speed = stats["speed"]
        self.damage = stats["damage"]
        self.radius = stats["radius"]

        # ----------------------------- SCORE & BONUS
        self.score_value = int(ZOMBIE_SCORE_VALUES[ztype] * ZOMBIE_RARITY_SCORE_MULT[self.rarity])
        self.drop_bonus = ZOMBIE_RARITY_DROP_BONUS[self.rarity]

        # ----------------------------- SPRITES
        self.sprites = ZombieSprites(ztype, self.radius)
        img = self.sprites.get_frame("front")
        if img:
            self.image = img
        else:
            self.image = pygame.Surface((self.radius*2, self.radius*2), pygame.SRCALPHA)
            pygame.draw.circle(self.image, (140,180,60), (self.radius, self.radius), self.radius)

        self.rect = self.image.get_rect(center=self.pos)

        # ----------------------------- SONIDO
        self.sound = ZombieSound()

        # ----------------------------- DEAD IMAGE
        self.dead_image = None

    # -----------------------------------------------------------------
    # Update principal
    # -----------------------------------------------------------------
    def update(self, dt, game):
        if self.dead:
            self._update_death(dt)
            return

        if getattr(game, "paused", False):
            self.sound.stop()
            return

        if not game.player:
            return

        # --------- Movimiento
        self._update_movement(dt, game.player)

        # --------- Cambio de sprite según dirección
        frame = self.sprites.get_frame(self.direction)
        if frame:
            self.image = frame

        # --------- Colisión con el jugador
        if pygame.sprite.collide_circle(self, game.player):
            game.player.take_damage(self.damage * dt)

        # --------- Sonido
        self.sound.update_volume(self.pos, game.player.pos)

    # -----------------------------------------------------------------
    # Movimiento
    # -----------------------------------------------------------------
    def _update_movement(self, dt, player):
        dvec = player.pos - self.pos
        if dvec.length_squared() == 0:
            return

        dnorm = MathUtils.normalize(dvec)
        self.pos += dnorm * self.speed * dt
        self.rect.center = (round(self.pos.x), round(self.pos.y))
        self.direction = MovementUtils.choose_direction_from_vector(dnorm)

    # -----------------------------------------------------------------
    # Muerte
    # -----------------------------------------------------------------
    def take_damage(self, dmg, game=None):
        if self.dead:
            return

        self.hp -= dmg
        if self.hp > 0:
            return

        # ----------- Muerte activada
        self.dead = True
        self.dead_timer = 0
        self.sound.stop()
        self.damage = 0
        self.radius = 0

        # ----------- Drop & Score
        if game:
            from settings import ZOMBIE_UPGRADE_DROP_SYSTEM
            from core.upgrade import Upgrade

            cfg = ZOMBIE_UPGRADE_DROP_SYSTEM.get(self.type)
            if cfg:
                drop_chance = cfg["base_chance"] + self.drop_bonus
                if random.random() * 100 < drop_chance:
                    Upgrade.spawn_from_zombie(game.upgrades, self)

            game.player.score += self.score_value

        # --------- Sprite muerto
        self.dead_image = self.sprites.get_dead(self.direction)

    # -----------------------------------------------------------------
    # Animación de muerte (Fade + linger)
    # -----------------------------------------------------------------
    def _update_death(self, dt):
        self.dead_timer += dt
        if not self.dead_image:
            return

        self.fade = min(255, self.fade + 400 * dt)
        corpse = self.dead_image.copy()
        corpse.set_alpha(int(self.fade))

        self.image = corpse
        self.rect = corpse.get_rect(center=self.pos)

        if self.dead_timer >= 4.0:
            self.kill()
