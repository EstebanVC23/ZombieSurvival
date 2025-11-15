import pygame
from utils.helpers import load_image_safe

class LoadingScreen:
    """Pantalla de carga con imagen escalada horizontalmente y barra de progreso."""

    def __init__(self, screen, screen_width, screen_height, image_path="menus/loading.png"):
        self.screen = screen
        self.screen_width = screen_width
        self.screen_height = screen_height

        self.original_image = load_image_safe(image_path)
        if self.original_image:
            # Escalar solo horizontalmente
            orig_w, orig_h = self.original_image.get_size()
            scale_ratio = screen_width / orig_w
            new_height = int(orig_h * scale_ratio)  # mantiene proporción vertical
            self.background = pygame.transform.scale(self.original_image, (screen_width, new_height))
            self.background_rect = self.background.get_rect(center=(screen_width // 2, screen_height // 2))
        else:
            print("[WARN] No se encontró la imagen de carga, usando fondo negro.")
            self.background = pygame.Surface((screen_width, screen_height))
            self.background.fill((0, 0, 0))
            self.background_rect = self.background.get_rect(center=(screen_width // 2, screen_height // 2))

        # Barra de carga
        self.bar_width = screen_width * 0.8
        self.bar_height = 20
        self.bar_x = (screen_width - self.bar_width) // 2
        self.bar_y = screen_height - 50
        self.progress = 0  # Valor entre 0.0 y 1.0

        self.bar_color = (0, 255, 0)
        self.bar_bg_color = (50, 50, 50)
        self.clock = pygame.time.Clock()

    def update_progress(self, value):
        """Actualiza el progreso de la barra (0 a 1)."""
        self.progress = max(0.0, min(1.0, value))
        self.draw()
        pygame.display.flip()
        self.clock.tick(60)

    def draw(self):
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.background, self.background_rect)
        # Fondo de barra
        pygame.draw.rect(self.screen, self.bar_bg_color, (self.bar_x, self.bar_y, self.bar_width, self.bar_height))
        # Barra de progreso
        pygame.draw.rect(self.screen, self.bar_color, (self.bar_x, self.bar_y, self.bar_width * self.progress, self.bar_height))
