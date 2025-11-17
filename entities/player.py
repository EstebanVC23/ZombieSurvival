import pygame
import os

from utils.math_utils import MathUtils
from utils.movement_utils import MovementUtils
from utils.helpers import load_image_safe, clean_image_background
from entities.weapon import Weapon

from settings import (
    PLAYER_SPEED, PLAYER_SIZE, PLAYER_BASE_HEALTH, PLAYER_BASE_ARMOR,
    PLAYER_BASE_FIRE_RATE, PLAYER_BASE_MAGAZINE, PLAYER_BASE_RESERVE_AMMO,
    UPGRADE_VALUES, WORLD_WIDTH, WORLD_HEIGHT, PLAYER_MAX_ARMOR
)


class Player(pygame.sprite.Sprite):

    def __init__(self, pos):
        super().__init__()

        self.pos = pygame.Vector2(pos)
        self.speed = PLAYER_SPEED

        # ------------------------------
        # ESTADÍSTICAS
        # ------------------------------
        self.health = PLAYER_BASE_HEALTH
        self.max_health = PLAYER_BASE_HEALTH

        self.shield = PLAYER_BASE_ARMOR
        self.max_shield = PLAYER_MAX_ARMOR

        self.score = 0

        # ------------------------------
        # SPRITES
        # ------------------------------
        self.size = PLAYER_SIZE
        self.direction = "front"
        self.angle = 0

        # Placeholder inicial
        self.image = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (40, 180, 40), (self.size // 2, self.size // 2), self.size // 2)
        self.rect = self.image.get_rect(center=self.pos)

        # Cargar sprites reales
        self.frames = {}
        self._load_sprites()

        # ------------------------------
        # ARMA
        # ------------------------------
        self.weapon = Weapon(
            self,
            damage=None,
            rpm=PLAYER_BASE_FIRE_RATE,
            ammo=PLAYER_BASE_MAGAZINE,
            reserve=PLAYER_BASE_RESERVE_AMMO,
            level=1,
            reload_time=None
        )

    # ============================================================
    # 🔹 Utils
    # ============================================================
    @property
    def x(self): return self.pos.x

    @property
    def y(self): return self.pos.y

    # ============================================================
    # 🎨 CARGA DE SPRITES
    # ============================================================
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
            self.rect = self.image.get_rect(center=self.pos)

    # ============================================================
    # ⌨ MOVIMIENTO E INPUT
    # ============================================================
    def handle_input(self, dt, mouse_pos, camera):
        move = pygame.Vector2(0, 0)
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w] or keys[pygame.K_UP]: move.y -= 1
        if keys[pygame.K_s] or keys[pygame.K_DOWN]: move.y += 1
        if keys[pygame.K_a] or keys[pygame.K_LEFT]: move.x -= 1
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]: move.x += 1

        if move.length_squared() > 0:
            move = move.normalize()

        # Movimiento usando utils
        self.pos += move * self.speed * dt
        self.pos = MovementUtils.clamp_position(self.pos, WORLD_WIDTH, WORLD_HEIGHT)
        self.rect.center = self.pos

        self._update_direction(mouse_pos, camera)

        if keys[pygame.K_r]:
            self.weapon.start_reload()

        if self.frames:
            self.image = self.frames[self.direction]

    # ============================================================
    # 🎯 Dirección basada en mouse
    # ============================================================
    def _update_direction(self, mouse_pos, camera):
        world_mouse = pygame.Vector2(mouse_pos) + camera.offset
        v = world_mouse - self.pos

        if abs(v.x) > abs(v.y):
            self.direction = "right" if v.x > 0 else "left"
        else:
            self.direction = "front" if v.y > 0 else "back"

    # ============================================================
    # 🔄 UPDATE
    # ============================================================
    def update(self, dt, game):
        self.handle_input(dt, pygame.mouse.get_pos(), game.camera)
        self.weapon.update(dt)

    # ============================================================
    # 🔫 DISPARO
    # ============================================================
    def shoot(self, target, game):
        world_target = pygame.Vector2(target) + game.camera.offset
        return self.weapon.fire(self.pos, world_target, game)

    # ============================================================
    # 💥 DAÑO
    # ============================================================
    def take_damage(self, amount):
        if self.shield > 0:
            self.shield -= amount
            if self.shield < 0:
                self.health -= -self.shield
                self.shield = 0
        else:
            self.health -= amount

        self.health = max(0, self.health)

    # ============================================================
    # 🧩 UPGRADES
    # ============================================================
    def apply_upgrade(self, up):
        val = UPGRADE_VALUES.get(up, 0)

        if up == "vida":
            self.health = min(self.max_health, self.health + val)
        elif up == "vida_extra":
            self.max_health += val
            self.health += val
        elif up == "armadura":
            self.shield = min(self.max_shield, self.shield + val)
        elif up == "velocidad":
            self.speed += val
        elif up == "balas":
            self.weapon.reserve_ammo += val
        elif up == "cargador":
            self.weapon.max_ammo += val
            self.weapon.current_ammo = self.weapon.max_ammo
        elif up == "cadencia":
            self.weapon.apply_fire_rate_bonus(val)
        elif up == "daño":
            self.weapon.apply_damage_bonus(val)
