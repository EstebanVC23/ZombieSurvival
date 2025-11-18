import pygame
import os

from utils.movement_utils import MovementUtils
from utils.helpers import load_image_safe, clean_image_background
from entities.weapon import Weapon

from settings import (
    PLAYER_SPEED, PLAYER_SIZE, PLAYER_BASE_HEALTH, PLAYER_BASE_ARMOR,
    UPGRADE_VALUES, WORLD_WIDTH, WORLD_HEIGHT, PLAYER_MAX_ARMOR,
    PLAYER_MIN_DISTANCE_TO_ZOMBIE
)

# ========================= Stats del Player =========================
class PlayerStats:
    """Manejo de salud, shield, upgrades y puntuación."""

    def __init__(self):
        self.health = PLAYER_BASE_HEALTH
        self.max_health = PLAYER_BASE_HEALTH
        self.shield = PLAYER_BASE_ARMOR
        self.max_shield = PLAYER_MAX_ARMOR
        self.score = 0

    def take_damage(self, amount):
        if self.shield > 0:
            self.shield -= amount
            if self.shield < 0:
                self.health -= -self.shield
                self.shield = 0
        else:
            self.health -= amount
        self.health = max(0, self.health)

    def apply_upgrade(self, up, weapon):
        val = UPGRADE_VALUES.get(up, 0)
        if up == "vida":
            self.health = min(self.max_health, self.health + val)
        elif up == "vida_extra":
            self.max_health += val
            self.health += val
        elif up == "armadura":
            self.shield = min(self.max_shield, self.shield + val)
        elif up == "velocidad":
            return val
        elif up == "balas":
            weapon.reserve_ammo += val
        elif up == "cargador":
            weapon.max_ammo += val
            weapon.current_ammo = weapon.max_ammo
        elif up == "cadencia":
            weapon.apply_fire_rate_bonus(val)
        elif up == "daño":
            weapon.apply_damage_bonus(val)

# ========================= Gráficos del Player =========================
class PlayerGraphics:
    """Carga sprites, maneja dirección y selección de frame."""

    def __init__(self, size):
        self.size = size
        self.direction = "front"
        self.image = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (40, 180, 40), (self.size // 2, self.size // 2), self.size // 2)
        self.rect = self.image.get_rect()
        self.frames = {}
        self._load_sprites()

    def _load_sprites(self):
        front = load_image_safe(os.path.join("player", "player_frente.png"))
        back = load_image_safe(os.path.join("player", "player_espalda.png"))
        side = load_image_safe(os.path.join("player", "player_lateral.png"))

        if front and back and side:
            self.frames["front"] = clean_image_background(pygame.transform.scale(front, (self.size, self.size)))
            self.frames["back"] = clean_image_background(pygame.transform.scale(back, (self.size, self.size)))
            self.frames["right"] = clean_image_background(pygame.transform.scale(side, (self.size, self.size)))
            self.frames["left"] = pygame.transform.flip(self.frames["right"], True, False)
            self.image = self.frames["front"]
            self.rect = self.image.get_rect()

    def update_image(self, direction):
        self.direction = direction
        if self.frames:
            self.image = self.frames[self.direction]
            self.rect = self.image.get_rect(center=self.rect.center)

# ========================= Movimiento del Player =========================
class PlayerMovement:
    """Gestiona input, movimiento y colisiones."""

    def __init__(self, pos, speed):
        self.pos = pygame.Vector2(pos)
        self.speed = speed
        self.angle = 0
        self.direction = "front"

    @property
    def x(self): return self.pos.x
    @property
    def y(self): return self.pos.y

    def handle_input(self, dt, mouse_pos, camera, zombies, weapon):
        move = pygame.Vector2(0, 0)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] or keys[pygame.K_UP]: move.y -= 1
        if keys[pygame.K_s] or keys[pygame.K_DOWN]: move.y += 1
        if keys[pygame.K_a] or keys[pygame.K_LEFT]: move.x -= 1
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]: move.x += 1

        if move.length_squared() > 0:
            move = move.normalize()

        new_pos = self.pos + move * self.speed * dt
        new_pos = MovementUtils.clamp_position(new_pos, WORLD_WIDTH, WORLD_HEIGHT)

        # Evitar atravesar zombies
        if zombies:
            for z in zombies:
                if z.dead: 
                    continue
                min_dist = z.radius + PLAYER_MIN_DISTANCE_TO_ZOMBIE
                offset = new_pos - z.pos
                dist = offset.length()
                if dist < min_dist:
                    if dist > 0:
                        offset.scale_to_length(min_dist)
                        new_pos = z.pos + offset
                    else:
                        new_pos += pygame.Vector2(min_dist, 0)

        self.pos = new_pos

        # Dirección
        self._update_direction(mouse_pos, camera)

        if keys[pygame.K_r]:
            weapon.start_reload()

        return self.direction

    def _update_direction(self, mouse_pos, camera):
        world_mouse = pygame.Vector2(mouse_pos) + camera.offset
        v = world_mouse - self.pos
        if abs(v.x) > abs(v.y):
            self.direction = "right" if v.x > 0 else "left"
        else:
            self.direction = "front" if v.y > 0 else "back"

# ========================= Player Principal =========================
class Player(pygame.sprite.Sprite):

    def __init__(self, pos):
        super().__init__()
        self.stats = PlayerStats()
        self.movement = PlayerMovement(pos, PLAYER_SPEED)
        self.graphics = PlayerGraphics(PLAYER_SIZE)
        self.weapon = Weapon(owner=self)

        # Inicializar rect
        self.graphics.rect.center = self.movement.pos
        self.rect = self.graphics.rect

    # ========================= Propiedades alias =========================
    @property
    def pos(self):
        return self.movement.pos

    @property
    def health(self):
        return self.stats.health
    @health.setter
    def health(self, value):
        self.stats.health = value

    @property
    def shield(self):
        return self.stats.shield
    @shield.setter
    def shield(self, value):
        self.stats.shield = value

    @property
    def image(self):
        return self.graphics.image

    @property
    def rect(self):
        return self.graphics.rect
    @rect.setter
    def rect(self, value):
        self.graphics.rect = value

    @property
    def direction(self):
        return self.movement.direction

    @property
    def speed(self):
        return self.movement.speed
    @speed.setter
    def speed(self, value):
        self.movement.speed = value

    @property
    def score(self):
        return self.stats.score
    @score.setter
    def score(self, value):
        self.stats.score = value

    # ========================= Input y actualización =========================
    def handle_input(self, dt, mouse_pos, camera, zombies=None):
        direction = self.movement.handle_input(dt, mouse_pos, camera, zombies, self.weapon)
        self.graphics.update_image(direction)
        self.graphics.rect.center = self.movement.pos

    def update(self, dt, game):
        self.handle_input(dt, pygame.mouse.get_pos(), game.camera, zombies=game.zombies)
        self.weapon.update(dt)

    # ========================= Disparo =========================
    def shoot(self, target, game):
        world_target = pygame.Vector2(target) + game.camera.offset
        return self.weapon.fire(self.movement.pos, world_target, game)

    # ========================= Daño =========================
    def take_damage(self, amount):
        self.stats.take_damage(amount)

    # ========================= Upgrades =========================
    def apply_upgrade(self, up):
        extra_speed = self.stats.apply_upgrade(up, self.weapon)
        if extra_speed:
            self.movement.speed += extra_speed
        self.graphics.rect.center = self.movement.pos
