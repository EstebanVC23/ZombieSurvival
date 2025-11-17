import pygame


class KnockbackController:
    """
    Controla un empuje temporal aplicado a una entidad.
    No toca su movimiento normal; solo lo desplaza visualmente
    sobre su posición real.
    """

    def __init__(self):
        self.offset = pygame.Vector2(0, 0)
        self.velocity = pygame.Vector2(0, 0)
        self.timer = 0
        self.duration = 0

    def apply_knockback(self, direction, force, duration=0.15):
        """
        direction: vector desde atacante -> objetivo (unitario)
        force: intensidad del empuje
        duration: tiempo del efecto
        """
        self.duration = duration
        self.timer = duration
        self.velocity = pygame.Vector2(direction) * force

    def update(self, dt):
        if self.timer <= 0:
            self.offset.update(0, 0)
            return

        self.timer -= dt
        self.offset += self.velocity * dt

        # amortiguación para que se frene suavemente
        self.velocity *= 0.85

        if self.timer <= 0 or self.velocity.length_squared() < 0.01:
            self.offset.update(0, 0)
