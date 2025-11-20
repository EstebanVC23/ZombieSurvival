import pygame
import os

from utils.helpers import load_image_safe, clean_image_background

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
