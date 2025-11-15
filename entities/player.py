import pygame
import os
import math
from settings import (
    PLAYER_SPEED, PLAYER_SIZE, PLAYER_BASE_HEALTH, PLAYER_BASE_ARMOR,
    PLAYER_BASE_FIRE_RATE, PLAYER_BASE_MAGAZINE, PLAYER_BASE_RESERVE_AMMO,
    UPGRADE_VALUES, WORLD_WIDTH, WORLD_HEIGHT, PLAYER_MAX_ARMOR
)
from utils.helpers import load_image_safe, clean_image_background
from entities.weapon import Weapon

class Player(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.pos = pygame.math.Vector2(pos)
        self.speed = PLAYER_SPEED

        # Estadísticas
        self.health = PLAYER_BASE_HEALTH
        self.max_health = PLAYER_BASE_HEALTH
        self.shield = PLAYER_BASE_ARMOR
        self.max_shield = PLAYER_MAX_ARMOR

        self.size = PLAYER_SIZE
        self.direction = "front"
        self.angle = 0.0

        # Imagen base (placeholder)
        self.image = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (30, 200, 30), (self.size // 2, self.size // 2), self.size // 2)
        self.rect = self.image.get_rect(center=(round(self.pos.x), round(self.pos.y)))

        # Sprites jugador
        front_img = load_image_safe(os.path.join("player", "player_frente.png"))
        back_img = load_image_safe(os.path.join("player", "player_espalda.png"))
        side_img = load_image_safe(os.path.join("player", "player_lateral.png"))

        self.frames = {}
        if front_img and back_img and side_img:
            self.frames["front"] = clean_image_background(pygame.transform.scale(front_img, (self.size, self.size)))
            self.frames["back"] = clean_image_background(pygame.transform.scale(back_img, (self.size, self.size)))
            self.frames["right"] = clean_image_background(pygame.transform.scale(side_img, (self.size, self.size)))
            self.frames["left"] = pygame.transform.flip(self.frames["right"], True, False)
            self.image = self.frames["front"]
            self.rect = self.image.get_rect(center=(round(self.pos.x), round(self.pos.y)))

        # Arma
        self.weapon = Weapon(
            self,
            damage=None,
            rpm=PLAYER_BASE_FIRE_RATE,
            ammo=PLAYER_BASE_MAGAZINE,
            reserve=PLAYER_BASE_RESERVE_AMMO,
            level=1,
            reload_time=None
        )

        # Puntuación
        self.score = 0

    @property
    def x(self): return self.pos.x
    @property
    def y(self): return self.pos.y

    def handle_input(self, dt, mouse_pos, camera):
        move = pygame.math.Vector2(0, 0)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] or keys[pygame.K_UP]: move.y -= 1
        if keys[pygame.K_s] or keys[pygame.K_DOWN]: move.y += 1
        if keys[pygame.K_a] or keys[pygame.K_LEFT]: move.x -= 1
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]: move.x += 1
        if move.length_squared() > 0: move = move.normalize()
        self.pos += move * self.speed * dt

        self.pos.x = max(0, min(WORLD_WIDTH, self.pos.x))
        self.pos.y = max(0, min(WORLD_HEIGHT, self.pos.y))
        self.rect.center = (round(self.pos.x), round(self.pos.y))

        self.update_direction_by_mouse(mouse_pos, camera)
        if keys[pygame.K_r]:
            self.weapon.start_reload()
        if self.frames:
            self.image = self.frames[self.direction]

    def update_direction_by_mouse(self, mouse_pos, camera):
        world_mouse_x = mouse_pos[0] + camera.offset.x
        world_mouse_y = mouse_pos[1] + camera.offset.y
        dx = world_mouse_x - self.pos.x
        dy = world_mouse_y - self.pos.y
        self.angle = math.degrees(math.atan2(dy, dx))
        if abs(dx) > abs(dy):
            self.direction = "right" if dx > 0 else "left"
        else:
            self.direction = "front" if dy > 0 else "back"

    def update(self, dt, game):
        self.handle_input(dt, pygame.mouse.get_pos(), game.camera)
        self.weapon.update(dt)

    def shoot(self, target, game):
        target_world = (target[0] + game.camera.offset.x, target[1] + game.camera.offset.y)
        return self.weapon.fire(self.pos, target_world, game)

    def take_damage(self, amount):
        if self.shield > 0:
            self.shield -= amount
            if self.shield < 0:
                self.health -= -self.shield
                self.shield = 0
            return
        self.health -= amount
        if self.health < 0: self.health = 0

    def apply_upgrade(self, upgrade_type):
        value = UPGRADE_VALUES.get(upgrade_type, 0)
        if upgrade_type == "vida":
            self.health = min(self.max_health, self.health + value)
        elif upgrade_type == "cadencia":
            self.weapon.apply_fire_rate_bonus(value)
        elif upgrade_type == "velocidad":
            self.speed += value
        elif upgrade_type == "balas":
            self.weapon.reserve_ammo += value
        elif upgrade_type == "cargador":
            self.weapon.max_ammo += value
            self.weapon.current_ammo = self.weapon.max_ammo
        elif upgrade_type == "armadura":
            self.shield = min(self.max_shield, self.shield + value)
