import pygame
import os

from utils.helpers import load_image_safe, clean_image_background

class ZombieSprites:
    def __init__(self, type_name, radius):
        self.radius = radius
        self.frames = {}

        base_path = os.path.join("zombie", type_name)
        f = load_image_safe(os.path.join(base_path, "frente.png"))
        b = load_image_safe(os.path.join(base_path, "espalda.png"))
        l = load_image_safe(os.path.join(base_path, "lateral.png"))
        raw_dead = load_image_safe(os.path.join(base_path, "dead.png"))

        if not f or not b or not l:
            common_base = os.path.join("zombie", "common")
            f = f or load_image_safe(os.path.join(common_base, "frente.png"))
            b = b or load_image_safe(os.path.join(common_base, "espalda.png"))
            l = l or load_image_safe(os.path.join(common_base, "lateral.png"))
            raw_dead = raw_dead or load_image_safe(os.path.join(common_base, "dead.png"))

        if not f:
            f = pygame.Surface((radius*2, radius*2), pygame.SRCALPHA)
            pygame.draw.circle(f, (140,180,60), (radius, radius), radius)
        if not b:
            b = pygame.Surface((radius*2, radius*2), pygame.SRCALPHA)
            pygame.draw.circle(b, (120,160,50), (radius, radius), radius)
        if not l:
            l = pygame.Surface((radius*2, radius*2), pygame.SRCALPHA)
            pygame.draw.circle(l, (100,140,40), (radius, radius), radius)
        if not raw_dead:
            raw_dead = pygame.Surface((radius*2, radius*2), pygame.SRCALPHA)
            pygame.draw.circle(raw_dead, (80,80,80), (radius, radius), radius)

        self.frames["front"] = clean_image_background(pygame.transform.scale(f, (radius*2, radius*2)))
        self.frames["back"] = clean_image_background(pygame.transform.scale(b, (radius*2, radius*2)))
        self.frames["left"] = clean_image_background(pygame.transform.scale(l, (radius*2, radius*2)))
        self.frames["right"] = pygame.transform.flip(self.frames["left"], True, False)

        self.dead_sprite = clean_image_background(pygame.transform.scale(raw_dead, (radius*2, radius*2)))

    def get_frame(self, direction):
        return self.frames.get(direction, self.frames["front"])

    def get_dead(self, direction):
        img = self.dead_sprite
        if not img:
            img = pygame.Surface((self.radius*2, self.radius*2), pygame.SRCALPHA)
            pygame.draw.circle(img, (80,80,80), (self.radius, self.radius), self.radius)
        if direction == "back":
            return pygame.transform.rotate(img, 180)
        if direction == "left":
            return pygame.transform.rotate(img, -90)
        if direction == "right":
            return pygame.transform.rotate(img, 90)
        return img