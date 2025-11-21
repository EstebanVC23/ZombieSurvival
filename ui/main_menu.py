# ================================================================
# main_menu.py
# ================================================================

import pygame
import sys
import math

from utils.helpers import load_image_safe, load_music
from core.game import Game
from ui.main_menu_components.menu_assets import MenuAssets
from ui.main_menu_components.menu_ui import MenuUI
from ui.main_menu_components.player_name_input import PlayerNameOverlay
from ui.main_menu_components.top10display import Top10Display

from colors import DARK_GREY, MENU_GLOW

pygame.init()

# ================================================================
# CLASS: MainMenu
# ================================================================
class MainMenu:
    def __init__(self):
        self.assets = MenuAssets()
        self.ui = MenuUI(self.assets)
        self.player_name_overlay = None
        self.waiting_name = False
        self.player_name = None  # Nombre ingresado por el usuario
        self.top10_overlay = Top10Display(self.assets.screen)  # Pre-inicializado

    def main_menu(self):
        if not pygame.mixer.get_init():
            pygame.mixer.init()
        load_music("ambient.mp3", volume=0.6, loop=-1)

        screen = self.assets.screen
        running = True

        while running:
            mouse_pos = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                # ------------------ CLICK EN BOTONES DEL MENU ------------------
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if not self.waiting_name and not self.top10_overlay.active:
                        clicked = self.ui.menu_buttons.handle_click(mouse_pos)
                        if clicked == "START GAME":
                            self.player_name_overlay = PlayerNameOverlay(screen)
                            self.waiting_name = True
                        elif clicked == "HIGH SCORES":
                            self.top10_overlay.show()
                        elif clicked == "EXIT":
                            pygame.quit()
                            sys.exit()

                # ------------------ EVENTOS DEL OVERLAY ------------------
                if self.waiting_name and self.player_name_overlay:
                    result = self.player_name_overlay.run_event(event)
                    if result == "CANCEL":
                        self.waiting_name = False
                        self.player_name_overlay = None
                    elif result:
                        self.player_name = result
                        game = Game(player_name=self.player_name)
                        game.load_resources()
                        game.run()
                        running = False

                # ------------------ EVENTOS DEL TOP10 ------------------
                if self.top10_overlay.active:
                    self.top10_overlay.handle_event(event)

            # ------------------ DIBUJADO ------------------
            screen.blit(self.assets.background, (0, 0))
            self.ui.draw()

            # Líneas decorativas
            line_y_top = 260
            line_y_bottom = 630
            for y in (line_y_top, line_y_bottom):
                pygame.draw.line(screen, DARK_GREY, (150, y), (self.assets.SCREEN_WIDTH - 150, y), 2)
                pulse = abs(math.sin(pygame.time.get_ticks() / 400))
                glow_len = int(50 + pulse * 100)
                cx = self.assets.SCREEN_WIDTH // 2
                pygame.draw.line(screen, MENU_GLOW, (cx - glow_len, y), (cx + glow_len, y), 3)

            # Dibujar overlays si están activos
            if self.waiting_name and self.player_name_overlay:
                self.player_name_overlay.draw()
            if self.top10_overlay.active:
                self.top10_overlay.draw()

            # Cursor personalizado
            if self.assets.cursor_menu:
                screen.blit(self.assets.cursor_menu, (mouse_pos[0] - 8, mouse_pos[1] - 8))

            pygame.display.flip()
            self.assets.clock.tick(self.assets.FPS)


# ================================================================
# EJECUCIÓN DIRECTA
# ================================================================
def main_menu():
    return MainMenu().main_menu()


if __name__ == "__main__":
    main_menu()
