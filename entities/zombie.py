import pygame
import os
import random
from settings import (
    ZOMBIE_COMMON_HP, ZOMBIE_COMMON_SPEED, ZOMBIE_COMMON_SIZE, ZOMBIE_COMMON_DAMAGE,
    ZOMBIE_FAST_HP, ZOMBIE_FAST_SPEED, ZOMBIE_FAST_SIZE, ZOMBIE_FAST_DAMAGE,
    ZOMBIE_TANK_HP, ZOMBIE_TANK_SPEED, ZOMBIE_TANK_SIZE, ZOMBIE_TANK_DAMAGE,
    ZOMBIE_BOSS_HP, ZOMBIE_BOSS_SPEED, ZOMBIE_BOSS_SIZE, ZOMBIE_BOSS_DAMAGE,
    ZOMBIE_RARITY_CHANCE, ZOMBIE_RARITY_MULT, ZOMBIE_RARITY_UPGRADE_COUNT,
    ZOMBIE_RARITY_SCORE_MULT, ZOMBIE_RARITY_DROP_BONUS,
    ZOMBIE_SCORE_VALUES,
    WORLD_WIDTH, WORLD_HEIGHT
)
from utils.helpers import load_image_safe, clean_image_background, load_sound


class Zombie(pygame.sprite.Sprite):
    # ===============================
    # ESTADÍSTICAS BASE POR TIPO
    # ===============================
    TYPE_STATS = {
        "common": {"hp": ZOMBIE_COMMON_HP, "speed": ZOMBIE_COMMON_SPEED, "radius": ZOMBIE_COMMON_SIZE//2, "damage": ZOMBIE_COMMON_DAMAGE},
        "fast":   {"hp": ZOMBIE_FAST_HP, "speed": ZOMBIE_FAST_SPEED, "radius": ZOMBIE_FAST_SIZE//2, "damage": ZOMBIE_FAST_DAMAGE},
        "tank":   {"hp": ZOMBIE_TANK_HP, "speed": ZOMBIE_TANK_SPEED, "radius": ZOMBIE_TANK_SIZE//2, "damage": ZOMBIE_TANK_DAMAGE},
        "boss":   {"hp": ZOMBIE_BOSS_HP, "speed": ZOMBIE_BOSS_SPEED, "radius": ZOMBIE_BOSS_SIZE//2, "damage": ZOMBIE_BOSS_DAMAGE},
    }

    # ===============================
    # AUMENTO DE STATS POR NIVEL (depende del tipo)
    # ===============================
    LEVEL_UP_STATS = {
        "common": {"hp": 3, "damage": 2, "speed": 1.5},
        "fast":   {"hp": 2, "damage": 1, "speed": 4},
        "tank":   {"hp": 8, "damage": 4, "speed": 0.8},
        "boss":   {"hp": 20, "damage": 10, "speed": 1.0},
    }

    # ===============================
    # SISTEMA DE RAREZAS
    # ===============================
    RARITY_TABLE = [
        ("common",    ZOMBIE_RARITY_CHANCE["common"]),
        ("uncommon",  ZOMBIE_RARITY_CHANCE["uncommon"]),
        ("rare",      ZOMBIE_RARITY_CHANCE["rare"]),
        ("epic",      ZOMBIE_RARITY_CHANCE["epic"]),
        ("legendary", ZOMBIE_RARITY_CHANCE["legendary"]),
    ]

    def __init__(self, pos, ztype="common", level=1, rarity=None):
        super().__init__()
        stats = self.TYPE_STATS.get(ztype, self.TYPE_STATS["common"])
        self.type = ztype
        self.level = level
        self.pos = pygame.Vector2(pos)
        self.direction = "front"
        self.dead = False
        self.dead_timer = 0.0
        self.fade = 0.0
        self.dead_image = None

        # ===============================
        # APLICAR RAREZA
        # ===============================
        self.rarity = rarity if rarity else self.roll_rarity()
        rarity_mult = ZOMBIE_RARITY_MULT[self.rarity]
        possible_stats = ["hp", "speed", "damage"]
        num_stats_to_upgrade = ZOMBIE_RARITY_UPGRADE_COUNT[self.rarity]
        stats_to_upgrade = random.sample(possible_stats, num_stats_to_upgrade)

        # Stats base
        self.hp = stats["hp"]
        self.speed = stats["speed"]
        self.damage = stats["damage"]
        self.radius = stats["radius"]  # Tamaño fijo

        # Aplicar multiplicador de rareza a stats seleccionados
        for s in stats_to_upgrade:
            setattr(self, s, getattr(self, s) * rarity_mult)

        # ===============================
        # APLICAR INCREMENTO POR NIVEL SEGÚN TIPO
        # ===============================
        if self.level > 1:
            level_increase = self.LEVEL_UP_STATS[self.type]
            self.hp += level_increase["hp"] * (self.level - 1)
            self.damage += level_increase["damage"] * (self.level - 1)
            self.speed += level_increase["speed"] * (self.level - 1)

        # ===============================
        # Puntaje y drop
        # ===============================
        self.score_value = int(ZOMBIE_SCORE_VALUES[self.type] * ZOMBIE_RARITY_SCORE_MULT[self.rarity])
        self.drop_bonus = ZOMBIE_RARITY_DROP_BONUS[self.rarity]

        # ===============================
        # SPRITES
        # ===============================
        self.image = pygame.Surface((self.radius*2, self.radius*2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (150,180,40), (self.radius,self.radius), self.radius)
        self.rect = self.image.get_rect(center=(round(self.pos.x), round(self.pos.y)))

        base = os.path.join("zombie", "common")
        f = load_image_safe(os.path.join(base, "common_frente.png"))
        b = load_image_safe(os.path.join(base, "common_espalda.png"))
        s = load_image_safe(os.path.join(base, "common_lateral.png"))

        self.frames = {}
        if f and b and s:
            self.frames["front"] = clean_image_background(pygame.transform.scale(f, (self.radius*2,self.radius*2)))
            self.frames["back"] = clean_image_background(pygame.transform.scale(b, (self.radius*2,self.radius*2)))
            self.frames["left"] = clean_image_background(pygame.transform.scale(s, (self.radius*2,self.radius*2)))
            self.frames["right"] = pygame.transform.flip(self.frames["left"], True, False)
            self.image = self.frames["front"]

        raw_dead = load_image_safe(os.path.join(base, "dead.png"))
        self.dead_sprite = clean_image_background(pygame.transform.scale(raw_dead, (self.radius*2, self.radius*2))) if raw_dead else None

        # Sonido
        self.sound = load_sound("zombie_common.mp3", volume=0.0)
        if self.sound: self.sound.play(loops=-1)
        self.max_sound_distance = max(600, (WORLD_WIDTH+WORLD_HEIGHT)/10)

    # =======================================================
    # ROLL RAREZA
    # =======================================================
    def roll_rarity(self):
        r = random.random()*100
        cumulative = 0
        for rarity, chance in self.RARITY_TABLE:
            cumulative += chance
            if r <= cumulative:
                return rarity
        return "common"

    # =======================================================
    # PROPIEDADES
    # =======================================================
    @property
    def x(self): return self.pos.x
    @property
    def y(self): return self.pos.y

    # =======================================================
    # UPDATE
    # =======================================================
    def update(self, dt, game):
        if self.dead:
            self.dead_timer += dt
            self._show_death_sprite(dt)
            if self.sound: self.sound.set_volume(0.0)
            if self.dead_timer >= 4.0: self.kill()
            return

        if not game.player: return
        if getattr(game, "paused", False):
            if self.sound: self.sound.stop()
            return

        # Movimiento
        dir_vec = game.player.pos - self.pos
        if dir_vec.length_squared() > 0:
            d = dir_vec.normalize()
            self.pos += d * self.speed * dt
            self.rect.center = (round(self.pos.x), round(self.pos.y))
            self._set_dir(d)

        if self.frames:
            self.image = self.frames.get(self.direction, self.image)

        # Colisión jugador
        if pygame.sprite.collide_circle(self, game.player):
            game.player.take_damage(self.damage * dt)

        # Sonido
        if self.sound:
            dist = self.pos.distance_to(game.player.pos)
            vol = max(0.0, min(1.0, (1-(dist/self.max_sound_distance))**2)) if dist<self.max_sound_distance else 0.0
            self.sound.set_volume(vol)

    # =======================================================
    # RECIBIR DAÑO (MÉTODO COMPLETO CORREGIDO)
    # =======================================================
    def take_damage(self, dmg, game=None):
        if self.dead: return

        self.hp -= dmg
        if self.hp > 0: return

        self.dead = True
        self.dead_timer = 0.0
        if self.sound:
            try: self.sound.stop()
            except Exception: pass

        # ✅ DROP Y SCORE CON SISTEMA UNIFICADO
        if game:
            from settings import ZOMBIE_UPGRADE_DROP_SYSTEM
            from core.upgrade import Upgrade
            
            drop_config = ZOMBIE_UPGRADE_DROP_SYSTEM.get(self.type)
            
            if drop_config:
                # Aplicar bonus de rareza a la probabilidad base
                drop_chance = drop_config["base_chance"] + self.drop_bonus
                
                # Check si dropea algo
                if random.random() * 100 < drop_chance:
                    Upgrade.spawn_from_zombie(game.upgrades, self)
            
            game.player.score += self.score_value

        # Mostrar sprite muerto
        if self.dead_sprite:
            rotated = self.dead_sprite
            if self.direction=="back": rotated = pygame.transform.rotate(self.dead_sprite, 180)
            elif self.direction=="left": rotated = pygame.transform.rotate(self.dead_sprite, -90)
            elif self.direction=="right": rotated = pygame.transform.rotate(self.dead_sprite, 90)
        else:
            rotated = self.image.copy()

        self.dead_image = rotated
        self.damage = 0
        self.radius = 0 # Evitar más colisiones

    # =======================================================
    # AUXILIARES
    # =======================================================
    def _set_dir(self, v):
        dx, dy = v.x, v.y
        if abs(dx)>abs(dy): self.direction = "right" if dx>0 else "left"
        else: self.direction = "front" if dy>0 else "back"

    def _show_death_sprite(self, dt):
        if not self.dead_image: return
        if self.fade<255: self.fade += 400*dt
        if self.fade>255: self.fade=255
        corpse = self.dead_image.copy()
        corpse.set_alpha(int(self.fade))
        self.image = corpse
        self.rect = self.image.get_rect(center=(round(self.pos.x), round(self.pos.y)))