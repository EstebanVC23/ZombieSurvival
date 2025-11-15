# core/camera.py
import pygame

class Camera:
    def __init__(self, width, height):
        self.offset = pygame.Vector2(0, 0)
        self.width = width
        self.height = height

    def update(self, target, screen_width, screen_height):
        """Centrar cámara en el jugador"""
        self.offset.x = target.pos.x - screen_width / 2
        self.offset.y = target.pos.y - screen_height / 2

        # Limitar a bordes del mapa
        self.offset.x = max(0, min(self.offset.x, self.width - screen_width))
        self.offset.y = max(0, min(self.offset.y, self.height - screen_height))

    def apply(self, rect):
        """Aplica el desplazamiento de cámara"""
        return rect.move(-self.offset.x, -self.offset.y)
