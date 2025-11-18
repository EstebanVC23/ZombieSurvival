# ui/lose_menu.py
import pygame
import sys
from utils.helpers import load_image_safe, load_music
from ui.buttons import ButtonWithBackground, Buttons

class LoseMenu:
    """Menú de derrota con botones funcionales y colores parametrizables."""

    def __init__(self, screen, screen_width, screen_height,
                 text_color=(255,255,255), hover_text_color=(255,255,255),
                 color=(50,50,50), hover_color=(70,70,70), border_color=(200,200,200)):
        self.screen = screen
        self.screen_width = screen_width
        self.screen_height = screen_height

        self.background = load_image_safe("menus/lose.png")
        if self.background:
            self.background = pygame.transform.scale(self.background, (screen_width, screen_height))
        else:
            self.background = pygame.Surface((screen_width,screen_height))
            self.background.fill((10,10,10))

        font_path = "assets/fonts/PressStart2P-Regular.ttf"
        button_texts = ["RESTART","MAIN MENU","EXIT"]
        button_width, button_height, spacing = 200,60,30
        total_width = len(button_texts)*button_width + (len(button_texts)-1)*spacing
        start_x = (screen_width-total_width)//2
        y = screen_height - button_height - 50

        buttons_list = [
            ButtonWithBackground(text,
                                 pygame.Rect(start_x + i*(button_width+spacing), y, button_width, button_height),
                                 font_path,
                                 color=color, hover_color=hover_color,
                                 text_color=text_color, border_color=border_color)
            for i,text in enumerate(button_texts)
        ]
        self.buttons = Buttons(screen, buttons_list)

    def draw(self):
        self.screen.blit(self.background, (0,0))
        self.buttons.draw()

    def handle_click(self, mouse_pos, game):
        clicked = self.buttons.handle_click(mouse_pos)
        if clicked == "RESTART":
            game.load_resources()
            game.reset_game()
        elif clicked == "MAIN MENU":
            # Detener todos los sonidos de zombies
            if hasattr(game, "zombies"):
                for z in game.zombies:
                    if hasattr(z, "sound") and z.sound:
                        z.sound.stop()

            # Cerrar el lose menu
            game.lose_menu = None
            game.paused = False

            # Cambiar resolución a la del main menu
            screen_width, screen_height = 700, 700
            game.screen = pygame.display.set_mode((screen_width, screen_height), pygame.NOFRAME)
            pygame.display.set_caption("Zombie Survival: Endless Apocalypse")

            # Reiniciar el cursor al menú
            game.current_cursor = game.cursor_menu

            # Marcar para volver al main menu
            game.return_to_main_menu = True

            # Iniciar música del menú
            load_music("ambient.mp3", volume=0.6, loop=-1)

        elif clicked == "EXIT":
            # Detener todos los sonidos de zombies antes de salir
            if hasattr(game, "zombies"):
                for z in game.zombies:
                    if hasattr(z, "sound") and z.sound:
                        z.sound.stop()
            pygame.quit()
            sys.exit()
