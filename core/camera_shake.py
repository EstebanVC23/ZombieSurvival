# core/camera_shake.py
import random
import pygame

class CameraShake:
    """
    Sistema de sacudidas de cámara con trauma.
    Compatible con game.camera_shake.offset ya usado por tu cámara.
    """

    def __init__(self):
        self.trauma = 0.0          # intensidad actual
        self.decay = 1.35          # qué tan rápido se reduce
        self.max_offset = 18       # desplazamiento máximo en píxeles
        self.offset = pygame.Vector2(0, 0)  # desplazamiento resultante

    # -----------------------------------------------------------
    # Añadir trauma (golpes, explosiones, impactos enemigos)
    # -----------------------------------------------------------
    def add_trauma(self, amount: float):
        self.trauma = min(1.0, self.trauma + amount)

    # -----------------------------------------------------------
    # Actualización por frame
    # -----------------------------------------------------------
    def update(self, dt):
        if self.trauma > 0:
            # Intensidad
            shake = self.trauma * self.trauma

            # Movimiento aleatorio
            self.offset.x = random.uniform(-1, 1) * self.max_offset * shake
            self.offset.y = random.uniform(-1, 1) * self.max_offset * shake

            # Reducir trauma con el tiempo
            self.trauma -= self.decay * dt
            self.trauma = max(self.trauma, 0)
        else:
            self.offset.update(0, 0)
