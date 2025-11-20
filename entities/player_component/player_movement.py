import pygame

from utils.movement_utils import MovementUtils
from settings import WORLD_HEIGHT, WORLD_WIDTH, PLAYER_MIN_DISTANCE_TO_ZOMBIE

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
