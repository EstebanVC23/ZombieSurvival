# utils/image_utils.py
import pygame
import os
from settings import ASSETS_IMAGES


# ===================================================
#  CARGA SEGURA DE IMÁGENES
# ===================================================

def load_image_safe(path: str):
    """
    Carga una imagen desde la carpeta de assets.
    Si no existe, retorna None y no crashea el juego.
    """
    full_path = os.path.join(ASSETS_IMAGES, path)

    if not os.path.exists(full_path):
        print(f"[DEBUG] Imagen no encontrada: {full_path}")
        return None

    try:
        return pygame.image.load(full_path).convert_alpha()
    except Exception as e:
        print(f"[DEBUG] Error cargando imagen {full_path}: {e}")
        return None


# ===================================================
#  TRANSFORMACIONES GENERALES
# ===================================================

def scale_image(img: pygame.Surface, factor: float):
    """
    Escala una imagen por un factor (1.0 = igual, 2.0 = doble tamaño).
    """
    if img is None:
        return None

    w, h = img.get_size()
    return pygame.transform.scale(img, (int(w * factor), int(h * factor)))


def resize_image(img: pygame.Surface, width: int, height: int):
    """
    Redimensiona una imagen a un tamaño exacto.
    """
    if img is None:
        return None

    return pygame.transform.scale(img, (width, height))


# ===================================================
#  FILTROS ADICIONALES (OPCIONAL)
# ===================================================

def set_colorkey(img: pygame.Surface, color):
    """
    Elimina un color sólido de fondo (para sprites sin alpha).
    """
    if img is not None:
        img.set_colorkey(color)
    return img


def rotate_image(img: pygame.Surface, angle: float):
    """
    Rotación segura de imagen.
    """
    if img is None:
        return None
    return pygame.transform.rotate(img, angle)
