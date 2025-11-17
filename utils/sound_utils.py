# utils/sound_utils.py
import pygame
from utils.helpers import load_sound

class SoundUtils:

    @staticmethod
    def load(path, volume=1.0, loop=False):
        """Carga un sonido seguro y opcionalmente lo inicia."""
        snd = load_sound(path, volume=volume)
        if snd and loop:
            try:
                snd.play(loops=-1)
            except Exception:
                pass
        return snd

    @staticmethod
    def play_one_shot(sound, max_time_ms=None):
        """Reproduce un sonido corto en cualquier canal libre."""
        if not sound:
            return
        try:
            ch = pygame.mixer.find_channel(True)
            ch.play(sound, maxtime=max_time_ms)
        except:
            pass

    @staticmethod
    def apply_distance_volume(sound, dist, max_dist):
        """Ajusta volumen según distancia (usando caída cuadrática)."""
        if not sound:
            return
        if dist >= max_dist:
            sound.set_volume(0.0)
            return
        vol = (1 - (dist / max_dist)) ** 2
        sound.set_volume(max(0.0, min(1.0, vol)))
