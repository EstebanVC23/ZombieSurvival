import pygame
import os
import sys

class PauseMenu:
    def __init__(self, screen, font, screen_width, screen_height):
        self.screen = screen
        self.font = font
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.options = ["Resume Game", "Settings", "Main Menu", "Exit Game"]

        pause_path = os.path.join("assets", "images", "menus", "pause_menu.png")
        if os.path.exists(pause_path):
            print(f"[INFO] Imagen de pausa encontrada correctamente en: {pause_path}")
            self.image = pygame.image.load(pause_path).convert_alpha()
            self.image = pygame.transform.scale(self.image, (500, 500))
        else:
            print(f"[WARN] No se encontró la imagen del menú de pausa en: {pause_path}")
            self.image = None

    def get_option_rects(self):
        center_x = self.screen_width // 2
        start_y = self.screen_height // 2
        spacing = 60
        rects = []

        for i, option in enumerate(self.options):
            text_surface = self.font.render(option, True, (255, 0, 0))
            rect = text_surface.get_rect(center=(center_x, start_y + i * spacing))
            rects.append((option, rect))

        return rects

    def draw(self):
        overlay = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 100))
        self.screen.blit(overlay, (0, 0))

        if self.image:
            rect = self.image.get_rect(center=(self.screen_width // 2, self.screen_height // 2))
            self.screen.blit(self.image, rect)
        else:
            print("[DEBUG] Imagen del menú de pausa no cargada correctamente")

        mouse_pos = pygame.mouse.get_pos()
        for option, rect in self.get_option_rects():
            hovered = rect.collidepoint(mouse_pos)
            color = (255, 100, 100) if hovered else (255, 0, 0)
            size = 22 if hovered else 18

            try:
                font = pygame.font.Font("assets/fonts/PressStart2P-Regular.ttf", size)
            except:
                font = pygame.font.SysFont("Arial", size)

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
                    print("[INFO] Regresando al menú principal...")
                    pygame.quit()
                    os.system("python launcher.py")
                    sys.exit()
                elif option == "Exit Game":
                    print("[INFO] Cerrando juego...")
                    game_instance.running = False
