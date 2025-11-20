import pygame
import os
import random
import math
from settings import (
    WORLD_WIDTH, WORLD_HEIGHT,
    ZOMBIE_COMMON_HP, ZOMBIE_COMMON_SPEED, ZOMBIE_COMMON_SIZE, ZOMBIE_COMMON_DAMAGE,
    ZOMBIE_FAST_HP, ZOMBIE_FAST_SPEED, ZOMBIE_FAST_SIZE, ZOMBIE_FAST_DAMAGE,
    ZOMBIE_TANK_HP, ZOMBIE_TANK_SPEED, ZOMBIE_TANK_SIZE, ZOMBIE_TANK_DAMAGE,
    ZOMBIE_BOSS_HP, ZOMBIE_BOSS_SPEED, ZOMBIE_BOSS_SIZE, ZOMBIE_BOSS_DAMAGE,
    ZOMBIE_RARITY_MULT, ZOMBIE_RARITY_UPGRADE_COUNT,
    ZOMBIE_RARITY_SCORE_MULT, ZOMBIE_MIN_DISTANCE_TO_PLAYER,
    ZOMBIE_LEVEL_UP_STATS,
    ZOMBIE_SCORE_VALUES, ZOMBIE_UPGRADE_DROP_SYSTEM,
    ZOMBIE_ATTACK_COOLDOWN, ZOMBIE_DETECTION_RADIUS, ZOMBIE_ALERT_RADIUS,
    ZOMBIE_WANDER_CHANGE_DIR_CHANCE, ZOMBIE_WANDER_SPEED_MULT,
    ZOMBIE_REPULSION_RADIUS, ZOMBIE_REPULSION_FORCE,

    # 🔥 nuevas constantes
    ZOMBIE_SOUND_DISTANCE,
    ZOMBIE_SOUND_MIN_INTERVAL,
    ZOMBIE_SOUND_MAX_INTERVAL
)
from utils.helpers import load_image_safe, clean_image_background
from utils.sound_utils import load_sound, SoundUtils


# ================================================================
# SISTEMA DE STATS
# ================================================================
class ZombieStats:
    TYPE_STATS = {
        "common": {"hp": ZOMBIE_COMMON_HP, "speed": ZOMBIE_COMMON_SPEED, "radius": ZOMBIE_COMMON_SIZE//2, "damage": ZOMBIE_COMMON_DAMAGE},
        "fast":   {"hp": ZOMBIE_FAST_HP,   "speed": ZOMBIE_FAST_SPEED,   "radius": ZOMBIE_FAST_SIZE//2,   "damage": ZOMBIE_FAST_DAMAGE},
        "tank":   {"hp": ZOMBIE_TANK_HP,   "speed": ZOMBIE_TANK_SPEED,   "radius": ZOMBIE_TANK_SIZE//2,   "damage": ZOMBIE_TANK_DAMAGE},
        "boss":   {"hp": ZOMBIE_BOSS_HP,   "speed": ZOMBIE_BOSS_SPEED,   "radius": ZOMBIE_BOSS_SIZE//2,   "damage": ZOMBIE_BOSS_DAMAGE},
    }

    @staticmethod
    def build(type_name, level, rarity):
        base = ZombieStats.TYPE_STATS[type_name]
        hp = base["hp"]
        speed = base["speed"]
        dmg = base["damage"]
        radius = base["radius"]

        rarity_mult = ZOMBIE_RARITY_MULT.get(rarity, 1)
        n_upgrades = ZOMBIE_RARITY_UPGRADE_COUNT.get(rarity, 0)
        possible = ["hp", "speed", "damage"]
        chosen = random.sample(possible, n_upgrades)

        if "hp" in chosen:
            hp *= rarity_mult
        if "speed" in chosen:
            speed *= rarity_mult
        if "damage" in chosen:
            dmg *= rarity_mult

        # Level-ups
        if level > 1:
            lv = ZOMBIE_LEVEL_UP_STATS[type_name]
            hp += lv["hp"] * (level - 1)
            dmg += lv["damage"] * (level - 1)
            speed += lv["speed"] * (level - 1)

        return {"hp": hp, "speed": speed, "damage": dmg, "radius": radius}



# ================================================================
# SPRITES (con caché global)
# ================================================================
class ZombieSprites:
    _cache = {}  # <---- cache global

    def __new__(cls, type_name, radius):
        key = (type_name, radius)
        if key not in cls._cache:
            cls._cache[key] = super(ZombieSprites, cls).__new__(cls)
            cls._cache[key]._init(type_name, radius)
        return cls._cache[key]

    def _init(self, type_name, radius):
        self.radius = radius
        self.frames = {}

        base_path = os.path.join("zombie", type_name)
        f = load_image_safe(os.path.join(base_path, "frente.png"))
        b = load_image_safe(os.path.join(base_path, "espalda.png"))
        l = load_image_safe(os.path.join(base_path, "lateral.png"))
        raw_dead = load_image_safe(os.path.join(base_path, "dead.png"))

        if not f or not b or not l:
            common = os.path.join("zombie", "common")
            f = f or load_image_safe(os.path.join(common, "frente.png"))
            b = b or load_image_safe(os.path.join(common, "espalda.png"))
            l = l or load_image_safe(os.path.join(common, "lateral.png"))
            raw_dead = raw_dead or load_image_safe(os.path.join(common, "dead.png"))

        def safe_circle(color):
            surf = pygame.Surface((radius*2, radius*2), pygame.SRCALPHA)
            pygame.draw.circle(surf, color, (radius, radius), radius)
            return surf

        f = f or safe_circle((140,180,60))
        b = b or safe_circle((120,160,50))
        l = l or safe_circle((100,140,40))
        raw_dead = raw_dead or safe_circle((80,80,80))

        self.frames["front"] = clean_image_background(pygame.transform.scale(f, (radius*2, radius*2)))
        self.frames["back"]  = clean_image_background(pygame.transform.scale(b, (radius*2, radius*2)))
        self.frames["left"]  = clean_image_background(pygame.transform.scale(l, (radius*2, radius*2)))
        self.frames["right"] = pygame.transform.flip(self.frames["left"], True, False)

        self.dead_sprite = clean_image_background(pygame.transform.scale(raw_dead, (radius*2, radius*2)))

    def get_frame(self, direction):
        return self.frames.get(direction, self.frames["front"])

    def get_dead(self, direction):
        img = self.dead_sprite
        if direction == "back":
            return pygame.transform.rotate(img, 180)
        if direction == "left":
            return pygame.transform.rotate(img, -90)
        if direction == "right":
            return pygame.transform.rotate(img, 90)
        return img


# ================================================================
# INTELIGENCIA DE ZOMBIE (no modificada)
# ================================================================
class ZombieAI:
    @staticmethod
    def choose_direction_from_vector(vec):
        if vec.length() == 0:
            return "front"
        angle = math.degrees(math.atan2(vec.y, vec.x))
        if -45 <= angle < 45:
            return "right"
        elif 45 <= angle < 135:
            return "down"
        elif -135 <= angle < -45:
            return "up"
        else:
            return "left"

    @staticmethod
    def move_towards(zombie, target_pos, dt, all_zombies=None):
        move_vec = target_pos - zombie.pos
        dist_to_player = move_vec.length()
        min_dist = zombie.radius + ZOMBIE_MIN_DISTANCE_TO_PLAYER

        if hasattr(zombie, 'target_player') and zombie.target_player:
            min_dist += zombie.target_player.radius

        if dist_to_player <= min_dist:
            return

        move_dir = move_vec.normalize()

        if all_zombies:
            for other in all_zombies:
                if other == zombie or other.dead:
                    continue
                offset = zombie.pos - other.pos
                dist = offset.length()
                if dist < ZOMBIE_REPULSION_RADIUS and dist > 0:
                    move_dir += offset.normalize() * (ZOMBIE_REPULSION_FORCE / dist)
            move_dir = move_dir.normalize()

        zombie.pos += move_dir * zombie.speed * dt
        zombie.rect.center = (round(zombie.pos.x), round(zombie.pos.y))

        dir_map = {"up": "back", "down": "front", "left": "left", "right": "right"}
        zombie.direction = dir_map.get(ZombieAI.choose_direction_from_vector(move_vec), "front")
        zombie.image = zombie.sprites.get_frame(zombie.direction)

    @staticmethod
    def wander(zombie, dt):
        if not hasattr(zombie, "_wander_dir") or random.random() < ZOMBIE_WANDER_CHANGE_DIR_CHANCE:
            angle = random.uniform(0, 2*math.pi)
            zombie._wander_dir = pygame.Vector2(math.cos(angle), math.sin(angle))

        zombie.pos += zombie._wander_dir * zombie.speed * dt * ZOMBIE_WANDER_SPEED_MULT

        bounced = False
        if zombie.pos.x < 0:
            zombie.pos.x = 0
            bounced = True
        elif zombie.pos.x > WORLD_WIDTH:
            zombie.pos.x = WORLD_WIDTH
            bounced = True
        if zombie.pos.y < 0:
            zombie.pos.y = 0
            bounced = True
        elif zombie.pos.y > WORLD_HEIGHT:
            zombie.pos.y = WORLD_HEIGHT
            bounced = True
        if bounced:
            angle = random.uniform(0, 2*math.pi)
            zombie._wander_dir = pygame.Vector2(math.cos(angle), math.sin(angle))

        zombie.rect.center = (round(zombie.pos.x), round(zombie.pos.y))
        dir_map = {"up": "back", "down": "front", "left": "left", "right": "right"}
        zombie.direction = dir_map.get(ZombieAI.choose_direction_from_vector(zombie._wander_dir), "front")
        zombie.image = zombie.sprites.get_frame(zombie.direction)



# ================================================================
# SONIDO DE ZOMBIES (optimizado, con intervalos)
# ================================================================
class ZombieSound:
    def __init__(self, zombie):
        self.zombie = zombie
        self.sound = load_sound("zombie_common.mp3", volume=0.0)
        self.max_dist = ZOMBIE_SOUND_DISTANCE

        # Tiempo para el próximo gruñido
        self.next_time = random.uniform(ZOMBIE_SOUND_MIN_INTERVAL,
                                        ZOMBIE_SOUND_MAX_INTERVAL)
        self.timer = 0.0

    def update(self, dt, player_pos):
        if not self.sound:
            return

        self.timer += dt

        # Solo hacer sonido cuando toca
        if self.timer >= self.next_time:
            try:
                self.sound.play()
            except:
                pass

            # Reiniciar para el próximo gruñido
            self.timer = 0.0
            self.next_time = random.uniform(
                ZOMBIE_SOUND_MIN_INTERVAL,
                ZOMBIE_SOUND_MAX_INTERVAL
            )

        # Ajustar volumen por distancia SIEMPRE que esté sonando
        dist = self.zombie.pos.distance_to(player_pos)
        SoundUtils.apply_distance_volume(self.sound, dist, self.max_dist)

    def stop(self):
        if self.sound:
            try: self.sound.stop()
            except: pass



# ================================================================
# ZOMBIE PRINCIPAL
# ================================================================
class Zombie(pygame.sprite.Sprite):
    ai_instance = ZombieAI()

    def __init__(self, pos, ztype="common", level=1, rarity=None):
        super().__init__()
        self.pos = pygame.Vector2(pos)
        self.direction = "front"
        self.dead = False
        self.dead_timer = 0
        self.fade = 0

        self.type = ztype
        self.level = level
        self.rarity = rarity

        stats = ZombieStats.build(ztype, level, self.rarity)
        self.hp = stats["hp"]
        self.speed = stats["speed"]
        self.damage = stats["damage"]
        self.radius = stats["radius"]

        self.attack_timer = 0.0
        self.alerted = False
        self.score_value = int(ZOMBIE_SCORE_VALUES[ztype] * ZOMBIE_RARITY_SCORE_MULT.get(self.rarity, 1))
        self.drop_bonus = 0

        self.sprites = ZombieSprites(ztype, self.radius)
        self.image = self.sprites.get_frame("front")
        self.rect = self.image.get_rect(center=self.pos)

        self.sound = ZombieSound(self)
        self.dead_image = None

    def update(self, dt, game):
        if self.dead:
            self._update_death(dt)
            return

        if not game.player:
            return

        # Actualizar sonido (intervalos y distancia)
        self.sound.update(dt, game.player.pos)

        dist_to_player = self.pos.distance_to(game.player.pos)

        if dist_to_player <= ZOMBIE_DETECTION_RADIUS or self.alerted:
            self.alerted = True

            # Propagar alerta
            for z in game.zombies:
                if z != self and not z.dead and z.pos.distance_to(self.pos) <= ZOMBIE_ALERT_RADIUS:
                    z.alerted = True

            ZombieAI.move_towards(self, game.player.pos, dt, all_zombies=game.zombies)

            self.attack_timer += dt
            cooldown = ZOMBIE_ATTACK_COOLDOWN.get(self.type, 1.0)
            if self.attack_timer >= cooldown:
                if pygame.sprite.collide_circle(self, game.player):
                    game.player.take_damage(self.damage)
                self.attack_timer = 0.0
        else:
            ZombieAI.wander(self, dt)

    def take_damage(self, dmg, game=None):
        if self.dead:
            return

        self.hp -= dmg
        self.alerted = True

        if game:
            for z in game.zombies:
                if z != self and not z.dead and z.pos.distance_to(self.pos) <= ZOMBIE_ALERT_RADIUS:
                    z.alerted = True

        if self.hp > 0:
            return

        # Muerte
        self.dead = True
        self.dead_timer = 0
        self.damage = 0
        self.radius = 0
        self.sound.stop()

        # Drop
        if game:
            cfg = ZOMBIE_UPGRADE_DROP_SYSTEM.get(self.type)
            if cfg:
                drop_chance = cfg["base_chance"] + self.drop_bonus
                if random.random() * 100 < drop_chance:
                    from core.upgrade import Upgrade
                    Upgrade.spawn_from_zombie(game.upgrades, self)

            game.player.score += self.score_value

        self.dead_image = self.sprites.get_dead(self.direction)

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
