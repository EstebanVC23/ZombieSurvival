# utils/movement_utils.py
import pygame

class MovementUtils:

    # ---------------------------------------------------------
    # Dirección de movimiento y ajuste del sprite
    # ---------------------------------------------------------
    @staticmethod
    def compute_direction_vector(start, end):
        """Vector normalizado desde start -> end."""
        v = pygame.Vector2(end) - pygame.Vector2(start)
        if v.length_squared() == 0:
            return pygame.Vector2(0, 0)
        return v.normalize()

    @staticmethod
    def choose_direction_from_vector(v):
        """Devuelve 'front', 'back', 'left', 'right' según vector."""
        dx, dy = v.x, v.y
        if abs(dx) > abs(dy):
            return "right" if dx > 0 else "left"
        return "front" if dy > 0 else "back"

    # ---------------------------------------------------------
    # Rotación y selección de sprite
    # ---------------------------------------------------------
    @staticmethod
    def rotate_image(img, angle):
        """Rota un sprite alrededor de su centro."""
        rotated = pygame.transform.rotate(img, angle)
        return rotated, rotated.get_rect(center=img.get_rect().center)

    @staticmethod
    def rotate_for_direction(base_img, direction):
        """Rota un sprite base según dirección textual."""
        if direction == "front":
            return base_img
        elif direction == "back":
            return pygame.transform.rotate(base_img, 180)
        elif direction == "left":
            return pygame.transform.rotate(base_img, -90)
        elif direction == "right":
            return pygame.transform.rotate(base_img, 90)
        return base_img

    # ---------------------------------------------------------
    # Movimiento físico simple
    # ---------------------------------------------------------
    @staticmethod
    def move_towards(pos, target_pos, speed, dt):
        v = MovementUtils.compute_direction_vector(pos, target_pos)
        return pos + v * speed * dt

    @staticmethod
    def clamp_position(pos, width, height):
        pos.x = max(0, min(width, pos.x))
        pos.y = max(0, min(height, pos.y))
        return pos

    # ---------------------------------------------------------
    # Desvanecimiento de sprites
    # ---------------------------------------------------------
    @staticmethod
    def apply_fade(img, alpha):
        surf = img.copy()
        surf.set_alpha(alpha)
        return surf

    # ---------------------------------------------------------
    # Colisión simple contra hitboxes
    # ---------------------------------------------------------
    @staticmethod
    def push_out(rect, hitbox):
        """Empuja rect fuera de un hitbox sólido."""
        dx_left   = rect.right  - hitbox.left
        dx_right  = hitbox.right - rect.left
        dy_top    = rect.bottom - hitbox.top
        dy_bottom = hitbox.bottom - rect.top

        min_dx = min(dx_left, dx_right)
        min_dy = min(dy_top, dy_bottom)

        if min_dx < min_dy:
            if dx_left < dx_right:
                rect.right = hitbox.left
            else:
                rect.left = hitbox.right
        else:
            if dy_top < dy_bottom:
                rect.bottom = hitbox.top
            else:
                rect.top = hitbox.bottom
