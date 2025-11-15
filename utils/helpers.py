# utils/helpers.py
import pygame, os
from settings import ASSETS_IMAGES

def load_image_safe(path):
    """Carga imágenes sin crashear si no existen"""
    full = os.path.join(ASSETS_IMAGES, path)
    if not os.path.exists(full):
        print(f"[DEBUG] No se encontró {full}")
        return None
    try:
        return pygame.image.load(full).convert_alpha()
    except Exception as e:
        print(f"[ERROR] Falló al cargar {full}: {e}")
        return None
