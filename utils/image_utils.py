import pygame

from helpers import load_image_safe  # usar siempre helpers para cargar imágenes

# image_utils.py
def scale_image(img: pygame.Surface, factor: float):
    if img is None:
        return None
    w, h = img.get_size()
    return pygame.transform.scale(img, (int(w * factor), int(h * factor)))

def resize_image(img: pygame.Surface, width: int, height: int):
    if img is None:
        return None
    return pygame.transform.scale(img, (width, height))

def set_colorkey(img: pygame.Surface, color):
    if img is not None:
        img.set_colorkey(color)
    return img

def rotate_image(img: pygame.Surface, angle: float):
    if img is None:
        return None
    return pygame.transform.rotate(img, angle)
