import pygame

from entities.weapon import Weapon
from settings import (
    PLAYER_SPEED, PLAYER_SIZE
)

from entities.player_component.player_graphics import PlayerGraphics
from entities.player_component.player_movement import PlayerMovement
from entities.player_component.player_stats import PlayerStats
import traceback

# ========================= Player Principal =========================
class Player(pygame.sprite.Sprite):

    def __init__(self, pos):
        super().__init__()

        print(f"[DEBUG][Player] Inicializando Player en posición {pos}")

        self.stats = PlayerStats()
        self.movement = PlayerMovement(pos, PLAYER_SPEED)
        self.graphics = PlayerGraphics(PLAYER_SIZE)
        self.weapon = Weapon(owner=self)

        # Inicializar rect
        self.graphics.rect.center = self.movement.pos
        self.rect = self.graphics.rect

        print("[DEBUG][Player] Player creado con stats, graphics, movement y weapon")

    # ========================= Propiedades alias =========================
    @property
    def pos(self):
        return self.movement.pos

    @property
    def health(self):
        return self.stats.health

    @health.setter
    def health(self, value):
        print(f"[DEBUG][Player] health cambiado a {value}")
        self.stats.health = value

    @property
    def shield(self):
        return self.stats.shield

    @shield.setter
    def shield(self, value):
        print(f"[DEBUG][Player] shield cambiado a {value}")
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
        print(f"[DEBUG][Player] speed cambiado a {value}")
        self.movement.speed = value

    @property
    def score(self):
        return self.stats.score

    @score.setter
    def score(self, value):
        print(f"[DEBUG][Player] score cambiado a {value}")
        self.stats.score = value

    # ========================= Input y actualización =========================
    def handle_input(self, dt, mouse_pos, camera, zombies=None):
        try:
            direction = self.movement.handle_input(dt, mouse_pos, camera, zombies, self.weapon)
            self.graphics.update_image(direction)
            self.graphics.rect.center = self.movement.pos
        except Exception:
            print("[ERROR][Player] Excepción en handle_input()")
            traceback.print_exc()

    def update(self, dt, game):
        try:
            self.handle_input(dt, pygame.mouse.get_pos(), game.camera, zombies=game.zombies)
            self.weapon.update(dt)
        except Exception:
            print("[ERROR][Player] Excepción en update()")
            traceback.print_exc()

    # ========================= Disparo =========================
    def shoot(self, target, game):
        try:
            world_target = pygame.Vector2(target) + game.camera.offset
            return self.weapon.fire(self.movement.pos, world_target, game)
        except Exception:
            print("[ERROR][Player] Excepción en shoot()")
            traceback.print_exc()

    # ========================= Daño =========================
    def take_damage(self, amount):
        print(f"[DEBUG][Player] Recibiendo daño: {amount}")
        self.stats.take_damage(amount)

    # ========================= Upgrades =========================
    def apply_upgrade(self, up):
        print(f"[DEBUG][Player] Aplicando upgrade: {up}")

        try:
            extra_speed = self.stats.apply_upgrade(up, self.weapon)
            if extra_speed:
                print(f"[DEBUG][Player] Upgrade dio extra_speed = {extra_speed}")
                self.movement.speed += extra_speed

            self.graphics.rect.center = self.movement.pos

        except Exception:
            print("[ERROR][Player] Excepción en apply_upgrade()")
            traceback.print_exc()
