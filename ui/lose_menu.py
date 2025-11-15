import pygame
from utils.helpers import load_image_safe

class LoseMenu:
    """Menú de derrota con botones funcionales Restart, Main Menu y Exit."""

    def __init__(self, screen, screen_width, screen_height):
        self.screen = screen
        self.screen_width = screen_width
        self.screen_height = screen_height

        # Fondo
        self.background = load_image_safe("menus/lose.png")
        if self.background:
            self.background = pygame.transform.scale(self.background, (screen_width, screen_height))
        else:
            self.background = pygame.Surface((screen_width, screen_height))
            self.background.fill((10, 10, 10))

        # Fuente
        self.font_path = "assets/fonts/PressStart2P-Regular.ttf"
        try:
            self.font = pygame.font.Font(self.font_path, 20)  # Fuente un poco más pequeña
        except:
            self.font = pygame.font.Font(None, 20)

        # Botones
        self.buttons = [
            {"text": "RESTART", "rect": None},
            {"text": "MAIN MENU", "rect": None},
            {"text": "EXIT", "rect": None}
        ]
        self.button_width = 200   # Caja más ancha
        self.button_height = 60   # Caja más alta
        self.button_color = (50, 50, 50)
        self.button_hover_color = (70, 70, 70)
        self.button_text_color = (255, 255, 255)
        self.button_border_color = (200, 200, 200)

        # Posición de los botones
        spacing = 30
        total_width = len(self.buttons) * self.button_width + (len(self.buttons)-1) * spacing
        start_x = (screen_width - total_width) // 2
        y = screen_height - self.button_height - 50
        for i, btn in enumerate(self.buttons):
            x = start_x + i * (self.button_width + spacing)
            btn["rect"] = pygame.Rect(x, y, self.button_width, self.button_height)

    def draw(self):
        self.screen.blit(self.background, (0, 0))
        mouse_pos = pygame.mouse.get_pos()
        for btn in self.buttons:
            rect = btn["rect"]
            color = self.button_hover_color if rect.collidepoint(mouse_pos) else self.button_color
            pygame.draw.rect(self.screen, color, rect)
            pygame.draw.rect(self.screen, self.button_border_color, rect, 3)
            font_size = 24 if rect.collidepoint(mouse_pos) else 20  # Ajustado según hover
            font = pygame.font.Font(self.font_path, font_size)
            label = font.render(btn["text"], True, self.button_text_color)
            label_rect = label.get_rect(center=rect.center)
            self.screen.blit(label, label_rect)

    def handle_click(self, mouse_pos, game):
        for btn in self.buttons:
            if btn["rect"].collidepoint(mouse_pos):
                if btn["text"] == "RESTART":
                    game.load_resources()  # recarga recursos si es necesario
                    game.reset_game()
                elif btn["text"] == "MAIN MENU":
                    game.return_to_main_menu = True
                    game.lose_menu = None
                    game.paused = False
                elif btn["text"] == "EXIT":
                    pygame.quit()
                    exit()
