import pygame
import math

class MathUtils:

    @staticmethod
    def normalize(vec):
        """Devuelve un vector normalizado sin riesgo de división por cero."""
        v = pygame.Vector2(vec)
        if v.length_squared() == 0:
            return pygame.Vector2(0, 0)
        return v.normalize()

    @staticmethod
    def direction(a, b):
        """Vector de dirección desde a -> b normalizado."""
        v = pygame.Vector2(b) - pygame.Vector2(a)
        return MathUtils.normalize(v)

    @staticmethod
    def distance(a, b):
        """Distancia entre dos posiciones."""
        return pygame.Vector2(a).distance_to(pygame.Vector2(b))

    @staticmethod
    def clamp(value, min_v, max_v):
        """Limita un valor entre un rango."""
        return max(min_v, min(max_v, value))

    @staticmethod
    def angle_between(a, b):
        """Ángulo en grados entre dos puntos."""
        dx = b[0] - a[0]
        dy = b[1] - a[1]
        return math.degrees(math.atan2(dy, dx))

    @staticmethod
    def lerp(a, b, t):
        """Interpolación lineal."""
        return a + (b - a) * t
