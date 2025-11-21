import pygame
import sys
from utils.helpers import load_image_safe, load_music
from ui.buttons import ButtonWithBackground, Buttons
from utils.score_manager import ScoreManager

class LoseMenu:
    """Menú de derrota con botones y posición real en la tabla de puntuaciones."""

    def __init__(self, screen, screen_width, screen_height,
                 player_name="Player", player_score=0, wave_reached=1,
                 text_color=(255,255,255), hover_text_color=(255,255,255),
                 color=(50,50,50), hover_color=(70,70,70), border_color=(200,200,200)):

        self.screen = screen
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.player_name = player_name

        # ScoreManager y guardado de puntuación
        self.score_manager = ScoreManager()
        self.score_manager.add_score(player_name, player_score, wave_reached)

        # Determinar posición del jugador en la tabla
        top_scores = self.score_manager.get_top_scores()
        self.position = 1
        for entry in top_scores:
            if entry['player'] == player_name and entry['score'] == player_score and entry['wave'] == wave_reached:
                self.position = entry['position']
                break

        # Fondo
        self.background = load_image_safe("menus/lose.png")
        if self.background:
            self.background = pygame.transform.scale(self.background, (screen_width, screen_height))
        else:
            self.background = pygame.Surface((screen_width,screen_height))
            self.background.fill((10,10,10))

        # Botones
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

        # Fuente para mostrar posición
        self.font = pygame.font.Font(font_path, 28)

    def draw(self):
        self.screen.blit(self.background, (0,0))
        self.buttons.draw()

        # Mostrar la posición y el nombre del jugador
        pos_text = f"{self.player_name.upper()} PLACED #{self.position}"
        text_surf = self.font.render(pos_text, True, (255, 215, 0))  # dorado
        text_rect = text_surf.get_rect(center=(self.screen_width//2, 150))
        self.screen.blit(text_surf, text_rect)

    def handle_click(self, mouse_pos, game):
        clicked = self.buttons.handle_click(mouse_pos)
        if clicked == "RESTART":
            game.load_resources()
            game.reset_game()
        elif clicked == "MAIN MENU":
            if hasattr(game, "zombies"):
                for z in game.zombies:
                    if hasattr(z, "sound") and z.sound:
                        z.sound.stop()
            game.lose_menu = None
            game.paused = False
            screen_width, screen_height = 700, 700
            game.screen = pygame.display.set_mode((screen_width, screen_height), pygame.NOFRAME)
            pygame.display.set_caption("Zombie Survival: Endless Apocalypse")
            game.current_cursor = game.cursor_menu
            game.return_to_main_menu = True
            load_music("ambient.mp3", volume=0.6, loop=-1)
        elif clicked == "EXIT":
            if hasattr(game, "zombies"):
                for z in game.zombies:
                    if hasattr(z, "sound") and z.sound:
                        z.sound.stop()
            pygame.quit()
            sys.exit()
