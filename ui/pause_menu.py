import pygame
import sys
from utils.helpers import load_image_safe

class PauseMenu:
    """Menú de pausa con overlay y opciones clicables."""

    def __init__(self, screen, screen_width, screen_height):
        self.screen = screen
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.options = ["Resume Game", "Settings", "Main Menu", "Exit Game"]

        # Cargar imagen de fondo del menú de pausa
        self.image = load_image_safe("menus/pause_menu.png")
        if self.image:
            self.image = pygame.transform.scale(self.image, (500, 500))
        else:
            print("[WARN] No se encontró la imagen del menú de pausa")

        # Fuente PressStart2P
        font_path = "assets/fonts/PressStart2P-Regular.ttf"
        if not pygame.font.get_init():
            pygame.font.init()
        self.base_font_path = font_path if pygame.font.Font(font_path, 18) else None

    def get_option_rects(self):
        center_x = self.screen_width // 2
        start_y = self.screen_height // 2
        spacing = 60
        rects = []

        for i, option in enumerate(self.options):
            font = pygame.font.Font(self.base_font_path, 18)
            text_surface = font.render(option, True, (255, 0, 0))
            rect = text_surface.get_rect(center=(center_x, start_y + i * spacing))
            rects.append((option, rect))

        return rects

    def draw(self):
        overlay = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 100))
        self.screen.blit(overlay, (0, 0))

        # Imagen de fondo del menú
        if self.image:
            rect = self.image.get_rect(center=(self.screen_width // 2, self.screen_height // 2))
            self.screen.blit(self.image, rect)

        mouse_pos = pygame.mouse.get_pos()
        for option, rect in self.get_option_rects():
            hovered = rect.collidepoint(mouse_pos)
            color = (255, 100, 100) if hovered else (255, 0, 0)
            size = 22 if hovered else 18
            font = pygame.font.Font(self.base_font_path, size)
            text = font.render(option, True, color)
            text_rect = text.get_rect(center=rect.center)
            self.screen.blit(text, text_rect)

    def handle_click(self, mouse_pos, game_instance):
        for option, rect in self.get_option_rects():
            if rect.collidepoint(mouse_pos):
                if option == "Resume Game":
                    game_instance.paused = False
                    game_instance.current_cursor = game_instance.cursor_game
                elif option == "Settings":
                    print("[DEBUG] Abrir ajustes (pendiente)")
                elif option == "Main Menu":
                    pygame.quit()
                    sys.exit()
                elif option == "Exit Game":
                    game_instance.running = False
