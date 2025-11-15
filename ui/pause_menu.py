import pygame
import sys
from utils.helpers import load_image_safe
from ui.buttons import ButtonTextOnly, Buttons

class PauseMenu:
    """Menú de pausa con overlay y opciones clicables."""

    def __init__(self, screen, screen_width, screen_height,
                 text_color=(255,0,0), hover_color=(255,100,100)):
        self.screen = screen
        self.screen_width = screen_width
        self.screen_height = screen_height

        self.image = load_image_safe("menus/pause_menu.png")
        if self.image:
            self.image = pygame.transform.scale(self.image, (500,500))

        font_path = "assets/fonts/PressStart2P-Regular.ttf"
        options = ["Resume Game", "Settings", "Main Menu", "Exit Game"]
        center_x = screen_width//2
        start_y = screen_height//2
        spacing = 60
        buttons_list = [
            ButtonTextOnly(opt, (center_x, start_y+i*spacing), font_path,
                           text_color=text_color, hover_color=hover_color)
            for i,opt in enumerate(options)
        ]
        self.buttons = Buttons(screen, buttons_list)

    def draw(self):
        overlay = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
        overlay.fill((0,0,0,100))
        self.screen.blit(overlay, (0,0))

        if self.image:
            rect = self.image.get_rect(center=(self.screen_width//2, self.screen_height//2))
            self.screen.blit(self.image, rect)

        self.buttons.draw()

    def handle_click(self, mouse_pos, game_instance):
        clicked = self.buttons.handle_click(mouse_pos)
        if clicked == "Resume Game":
            game_instance.paused = False
            game_instance.current_cursor = game_instance.cursor_game
        elif clicked == "Settings":
            print("[DEBUG] Abrir ajustes (pendiente)")
        elif clicked == "Main Menu":
            pygame.quit()
            sys.exit()
        elif clicked == "Exit Game":
            game_instance.running = False
