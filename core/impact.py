import pygame
import os
from utils.helpers import load_image_safe

class Impact(pygame.sprite.Sprite):
    def __init__(self, pos, size=(50, 50)):
        super().__init__()

        # ----------------------------------------------------------
        # 🔹 Cargar imagen de impacto (sin duplicar assets/images)
        # ----------------------------------------------------------
        image_path = "weapons/impact.png"
        img = load_image_safe(image_path)

        if img:
            img = pygame.transform.scale(img, size)
            img = self.clean_image(img)
            self.image = img
        else:
            print(f"[DEBUG] No se encontró {image_path}, usando placeholder.")
            self.image = pygame.Surface(size, pygame.SRCALPHA)
            pygame.draw.circle(self.image, (255, 180, 50), (size[0] // 2, size[1] // 2), size[0] // 2)

        self.rect = self.image.get_rect(center=pos)
        self.timer = 0.0
        self.duration = 0.25  # segundos visibles
        self.alpha = 255

        # ----------------------------------------------------------
        # 🔊 Reproducir sonido de impacto desde 0.1 segundos
        # ----------------------------------------------------------
        sound_path = os.path.join("assets", "sounds", "impact.mp3")

        if os.path.exists(sound_path):
            try:
                # Detenemos música previa y cargamos el efecto
                pygame.mixer.music.load(sound_path)
                pygame.mixer.music.set_volume(0.4)
                pygame.mixer.music.play(loops=0, start=0.1)  # empieza desde 0.1 segundos
            except Exception as e:
                print(f"[WARN] No se pudo reproducir el sonido de impacto: {e}")
        else:
            print(f"[WARN] No se encontró el sonido de impacto en: {sound_path}")

    # ----------------------------------------------------------
    # 🧼 Limpieza del fondo blanco/gris
    # ----------------------------------------------------------
    def clean_image(self, img):
        img = img.convert_alpha()
        clean = pygame.Surface(img.get_size(), pygame.SRCALPHA)
        img.lock()
        for x in range(img.get_width()):
            for y in range(img.get_height()):
                r, g, b, a = img.get_at((x, y))
                if (r + g + b) / 3 > 200 or a < 50:
                    img.set_at((x, y), (0, 0, 0, 0))
        img.unlock()
        clean.blit(img, (0, 0))
        return clean

    # ----------------------------------------------------------
    # ⏳ Actualización (desvanecimiento suave)
    # ----------------------------------------------------------
    def update(self, dt):
        self.timer += dt
        if self.timer > self.duration:
            self.kill()
        else:
            self.alpha = max(0, 255 * (1 - self.timer / self.duration))
            self.image.set_alpha(self.alpha)
