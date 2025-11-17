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
    ZOMBIE_SCORE_VALUES, ZOMBIE_UPGRADE_DROP_SYSTEM,
    ZOMBIE_ATTACK_COOLDOWN, ZOMBIE_DETECTION_RADIUS, ZOMBIE_ALERT_RADIUS,
    ZOMBIE_WANDER_CHANGE_DIR_CHANCE, ZOMBIE_WANDER_SPEED_MULT,
    ZOMBIE_REPULSION_RADIUS, ZOMBIE_REPULSION_FORCE,
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

    LEVEL_UP_STATS = {
        "common": {"hp": 3,  "damage": 2,  "speed": 1.5},
        "fast":   {"hp": 2,  "damage": 1,  "speed": 4},
        "tank":   {"hp": 8,  "damage": 4, "speed": 0.8},
        "boss":   {"hp": 20, "damage": 10, "speed": 1},
    }

    @staticmethod
    def roll_rarity():
        return "common"

    @staticmethod
    def build(type_name, level, rarity):
        base = ZombieStats.TYPE_STATS[type_name]
        hp = base["hp"]
        speed = base["speed"]
        dmg = base["damage"]
        radius = base["radius"]

        rarity_mult = ZOMBIE_RARITY_MULT.get(rarity, 1)
        n_upgrades = ZOMBIE_RARITY_UPGRADE_COUNT.get(rarity, 0)
        possible = ["hp","speed","damage"]
        chosen = random.sample(possible, n_upgrades)
        if "hp" in chosen: hp *= rarity_mult
        if "speed" in chosen: speed *= rarity_mult
        if "damage" in chosen: dmg *= rarity_mult

        if level > 1:
            lv = ZombieStats.LEVEL_UP_STATS[type_name]
            hp += lv["hp"] * (level - 1)
            dmg += lv["damage"] * (level - 1)
            speed += lv["speed"] * (level - 1)

        return {"hp": hp, "speed": speed, "damage": dmg, "radius": radius}

# ================================================================
# SPRITES
# ================================================================
class ZombieSprites:
    def __init__(self, type_name, radius):
        self.radius = radius
        base = os.path.join("zombie", type_name)
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
        self.dead_sprite = clean_image_background(pygame.transform.scale(raw_dead, (radius*2, radius*2))) if raw_dead else None

    def get_frame(self, direction):
        return self.frames.get(direction)

    def get_dead(self, direction):
        img = self.dead_sprite
        if not img: return None
        if direction == "back": return pygame.transform.rotate(img, 180)
        if direction == "left": return pygame.transform.rotate(img, -90)
        if direction == "right": return pygame.transform.rotate(img, 90)
        return img

# ================================================================
# IA DE ZOMBIES
# ================================================================
class ZombieAI:
    @staticmethod
    def choose_direction_from_vector(vec):
        angle = math.degrees(math.atan2(vec.y, vec.x))
        if -45 <= angle <= 45: return "right"
        elif 45 < angle <= 135: return "down"
        elif -135 <= angle < -45: return "up"
        else: return "left"

    @staticmethod
    def move_towards(zombie, target_pos, dt, all_zombies=None):
        move_vec = target_pos - zombie.pos
        dist_to_player = move_vec.length()

        # Evitar que zombie se meta dentro del player
        min_dist = zombie.radius + ZOMBIE_MIN_DISTANCE_TO_PLAYER
        if dist_to_player <= min_dist:
            return  # No moverse más cerca, sigue atacando

        move_dir = move_vec.normalize()

        # Repulsión entre zombies
        if all_zombies:
            for other in all_zombies:
                if other == zombie or other.dead: continue
                offset = zombie.pos - other.pos
                dist = offset.length()
                if dist < ZOMBIE_REPULSION_RADIUS and dist > 0:
                    move_dir += offset.normalize() * (ZOMBIE_REPULSION_FORCE / dist)
            move_dir = move_dir.normalize()

        # Mover zombie
        zombie.pos += move_dir * zombie.speed * dt
        zombie.rect.center = (round(zombie.pos.x), round(zombie.pos.y))
        zombie.direction = ZombieAI.choose_direction_from_vector(move_vec)


    @staticmethod
    def wander(zombie, dt):
        if not hasattr(zombie, "_wander_dir") or random.random() < ZOMBIE_WANDER_CHANGE_DIR_CHANCE:
            angle = random.uniform(0, 2*math.pi)
            zombie._wander_dir = pygame.Vector2(math.cos(angle), math.sin(angle))
        zombie.pos += zombie._wander_dir * zombie.speed * dt * ZOMBIE_WANDER_SPEED_MULT
        zombie.pos.x = max(0, min(WORLD_WIDTH, zombie.pos.x))
        zombie.pos.y = max(0, min(WORLD_HEIGHT, zombie.pos.y))
        zombie.rect.center = (round(zombie.pos.x), round(zombie.pos.y))
        zombie.direction = ZombieAI.choose_direction_from_vector(zombie._wander_dir)

# ================================================================
# SONIDO DE ZOMBIES
# ================================================================
class ZombieSound:
    def __init__(self, zombie):
        self.sound = load_sound("zombie_common.mp3", volume=0.0)
        self.zombie = zombie
        self.max_dist = ZOMBIE_DETECTION_RADIUS
        if self.sound:
            try: self.sound.play(loops=-1)
            except: pass

    def update_volume(self, player_pos):
        if not self.sound: return
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
        self.rarity = rarity if rarity else ZombieStats.roll_rarity()

        stats = ZombieStats.build(ztype, level, self.rarity)
        self.hp = stats["hp"]
        self.speed = stats["speed"]
        self.damage = stats["damage"]
        self.radius = stats["radius"]

        self.attack_timer = 0.0
        self.alerted = False
        self.score_value = int(ZOMBIE_SCORE_VALUES[ztype] * 1)
        self.drop_bonus = 0

        self.sprites = ZombieSprites(ztype, self.radius)
        img = self.sprites.get_frame("front")
        self.image = img if img else pygame.Surface((self.radius*2, self.radius*2), pygame.SRCALPHA)
        if not img: pygame.draw.circle(self.image, (140,180,60), (self.radius, self.radius), self.radius)
        self.rect = self.image.get_rect(center=self.pos)

        self.sound = ZombieSound(self)
        self.dead_image = None

    def update(self, dt, game):
        if self.dead:
            self._update_death(dt)
            return
        if not game.player: return

        # Actualizar sonido
        self.sound.update_volume(game.player.pos)

        # Distancia al jugador
        dist_to_player = self.pos.distance_to(game.player.pos)

        # Si detecta jugador
        if dist_to_player <= ZOMBIE_DETECTION_RADIUS or self.alerted:
            self.alerted = True

            # Alertar zombies cercanos
            for z in game.zombies:
                if z == self or z.dead: continue
                if z.pos.distance_to(self.pos) <= ZOMBIE_ALERT_RADIUS:
                    z.alerted = True

            # Perseguir jugador
            ZombieAI.move_towards(self, game.player.pos, dt, all_zombies=game.zombies)

            # Ataque con cooldown
            self.attack_timer += dt
            cooldown = ZOMBIE_ATTACK_COOLDOWN.get(self.type, 1.0)
            if self.attack_timer >= cooldown:
                if pygame.sprite.collide_circle(self, game.player):
                    game.player.take_damage(self.damage)
                self.attack_timer = 0.0
        else:
            # Vagando
            ZombieAI.wander(self, dt)

    def take_damage(self, dmg, game=None):
        if self.dead:
            return

        # Restar vida
        self.hp -= dmg

        # ALERTAR AL ZOMBIE CUANDO ES ATACADO
        self.alerted = True

        # Alertar a los zombies cercanos
        if game:
            for z in game.zombies:
                if z != self and not z.dead and z.pos.distance_to(self.pos) <= ZOMBIE_ALERT_RADIUS:
                    z.alerted = True

        # Si aún tiene vida, solo alertado, no muerto
        if self.hp > 0:
            return

        # Zombie muere
        self.dead = True
        self.dead_timer = 0
        self.damage = 0
        self.radius = 0
        self.sound.stop()

        # Drop de upgrades y puntaje
        if game:
            cfg = ZOMBIE_UPGRADE_DROP_SYSTEM.get(self.type)
            if cfg:
                drop_chance = cfg["base_chance"] + self.drop_bonus
                if random.random() * 100 < drop_chance:
                    from core.upgrade import Upgrade
                    Upgrade.spawn_from_zombie(game.upgrades, self)
            game.player.score += self.score_value

        # Sprite de cadáver
        self.dead_image = self.sprites.get_dead(self.direction)


    def _update_death(self, dt):
        self.dead_timer += dt
        if not self.dead_image: return
        self.fade = min(255, self.fade + 400*dt)
        corpse = self.dead_image.copy()
        corpse.set_alpha(int(self.fade))
        self.image = corpse
        self.rect = corpse.get_rect(center=self.pos)
        if self.dead_timer >= 4.0:
            self.kill()
