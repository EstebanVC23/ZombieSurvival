import pygame
import os
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


def load_font(font_name, size, fallback_name="Arial"):
    """Carga una fuente personalizada o usa fallback del sistema"""
    font_path = os.path.join("assets", "fonts", font_name)
    
    if os.path.exists(font_path):
        try:
            return pygame.font.Font(font_path, size)
        except Exception as e:
            print(f"[WARN] Error al cargar fuente {font_name}: {e}. Usando {fallback_name}.")
            return pygame.font.SysFont(fallback_name, size)
    else:
        print(f"[WARN] Fuente {font_name} no encontrada. Usando {fallback_name}.")
        return pygame.font.SysFont(fallback_name, size)


def load_sound(sound_path, volume=1.0):
    """Carga un efecto de sonido con volumen ajustable"""
    full_path = os.path.join("assets", "sounds", sound_path)
    
    if not os.path.exists(full_path):
        print(f"[WARN] Sonido no encontrado: {full_path}")
        return None
    
    try:
        sound = pygame.mixer.Sound(full_path)
        sound.set_volume(volume)
        return sound
    except Exception as e:
        print(f"[ERROR] Error al cargar sonido {sound_path}: {e}")
        return None


def load_music(music_path, volume=0.6, loop=-1):
    """Carga y reproduce música de fondo"""
    full_path = os.path.join("assets", "sounds", music_path)
    
    if not os.path.exists(full_path):
        print(f"[WARN] Música no encontrada: {full_path}")
        return False
    
    try:
        pygame.mixer.music.load(full_path)
        pygame.mixer.music.set_volume(volume)
        pygame.mixer.music.play(loop)
        return True
    except Exception as e:
        print(f"[ERROR] Error al cargar música {music_path}: {e}")
        return False


def stop_music():
    """Detiene la música actual"""
    try:
        pygame.mixer.music.stop()
    except Exception as e:
        print(f"[ERROR] Error al detener música: {e}")


def set_music_volume(volume):
    """Ajusta el volumen de la música (0.0 a 1.0)"""
    try:
        pygame.mixer.music.set_volume(max(0.0, min(1.0, volume)))
    except Exception as e:
        print(f"[ERROR] Error al ajustar volumen: {e}")


def load_cursor(path, size=(32, 32), threshold=160):
    """Carga un cursor personalizado limpiando fondos claros"""
    full_path = os.path.join(ASSETS_IMAGES, path)
    
    if not os.path.exists(full_path):
        print(f"[WARN] Cursor no encontrado: {full_path}")
        return None
    
    try:
        img = pygame.image.load(full_path).convert_alpha()
        img = pygame.transform.scale(img, size)
        clean = pygame.Surface(img.get_size(), pygame.SRCALPHA)
        img.lock()
        for x in range(img.get_width()):
            for y in range(img.get_height()):
                r, g, b, a = img.get_at((x, y))
                if (r + g + b) / 3 > threshold or a < 80:
                    img.set_at((x, y), (0, 0, 0, 0))
        img.unlock()
        clean.blit(img, (0, 0))
        return clean
    except Exception as e:
        print(f"[ERROR] Error al cargar cursor {full_path}: {e}")
        return None



def clean_image_background(image, threshold=200):
    """Elimina fondos claros de una imagen (útil para sprites)"""
    clean = pygame.Surface(image.get_size(), pygame.SRCALPHA)
    image.lock()
    for x in range(image.get_width()):
        for y in range(image.get_height()):
            r, g, b, a = image.get_at((x, y))
            if (r + g + b) / 3 > threshold and a > 0:
                image.set_at((x, y), (0, 0, 0, 0))
    image.unlock()
    clean.blit(image, (0, 0))
    return clean