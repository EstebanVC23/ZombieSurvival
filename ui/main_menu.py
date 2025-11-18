# ================================================================
# main_menu.py (MODULARIZADO EN UN SOLO ARCHIVO)
# ================================================================

import pygame
import sys
import math

from utils.helpers import load_image_safe, load_music
from core.game import Game
from ui.buttons import ButtonTextOnly, Buttons

from colors import (
    WHITE, DARK_BG, DARK_GREY,
    MENU_GLOW, MENU_SHADOW
)

pygame.init()


# ================================================================
#  CLASS: MenuAssets  (carga imágenes, fuentes, cursor, pantalla)
# ================================================================
class MenuAssets:
    SCREEN_WIDTH = 700
    SCREEN_HEIGHT = 700
    FPS = 60

    def __init__(self):
        # --- Ventana ---
        self.screen = pygame.display.set_mode(
            (self.SCREEN_WIDTH, self.SCREEN_HEIGHT), pygame.NOFRAME
        )
        pygame.display.set_caption("Zombie Survival: Endless Apocalypse")
        self.clock = pygame.time.Clock()

        # --- Fondo ---
        self.background = self.load_background()

        # --- Fuentes ---
        self.base_font, self.title_font = self.load_fonts()

        # --- Cursor ---
        pygame.mouse.set_visible(False)
        self.cursor_menu = self.load_cursor("ui/cursor_menu.png", (20, 20))

    # ------------------------------------------------------------
    def load_background(self):
        bg = load_image_safe("menus/menu_bg.png")
        if bg:
            return pygame.transform.scale(bg, (self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        print("[WARN] No se encontró la imagen de fondo, usando fondo negro.")
        surf = pygame.Surface((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        surf.fill((10, 10, 10))
        return surf

    # ------------------------------------------------------------
    def load_fonts(self):
        font_path = "assets/fonts/PressStart2P-Regular.ttf"
        try:
            base = pygame.font.Font(font_path, 28)
            title = pygame.font.Font(font_path, 48)
        except:
            print("[WARN] No se encontró la fuente Press Start 2P, usando fuente por defecto.")
            base = pygame.font.Font(None, 28)
            title = pygame.font.Font(None, 48)
        return base, title

    # ------------------------------------------------------------
    def load_cursor(self, path, size):
        img = load_image_safe(path)
        if not img:
            return None
        img = pygame.transform.scale(img, size)
        img.lock()
        for x in range(img.get_width()):
            for y in range(img.get_height()):
                r, g, b, a = img.get_at((x, y))
                if a > 0 and (r + g + b) / 3 > 210:
                    img.set_at((x, y), (0, 0, 0, 0))
        img.unlock()
        return img


# ================================================================
#  CLASS: MenuVisualFX  (efectos: glow, particulas, bordes, etc.)
# ================================================================
class MenuVisualFX:

    @staticmethod
    def draw_glowing_title(surface, text, pos, font, base_color, glow_color, time_offset):
        pulse = abs(math.sin(pygame.time.get_ticks() / 500 + time_offset))

        # Sombras
        for offset in [(4, 4), (3, 3), (2, 2)]:
            shadow = font.render(text, True, MENU_SHADOW)
            rect = shadow.get_rect(center=(pos[0] + offset[0], pos[1] + offset[1]))
            surface.blit(shadow, rect)

        # Glow exterior
        glow_intensity = int(100 + pulse * 155)
        color = (glow_color[0], glow_color[1], glow_color[2], glow_intensity)

        for radius in [6, 4, 2]:
            gl = font.render(text, True, color[:3])
            gl.set_alpha(glow_intensity // (7 - radius))

            for angle in range(0, 360, 45):
                ox = int(math.cos(math.radians(angle)) * radius)
                oy = int(math.sin(math.radians(angle)) * radius)
                rect = gl.get_rect(center=(pos[0] + ox, pos[1] + oy))
                surface.blit(gl, rect)

        # Texto final
        surf = font.render(text, True, base_color)
        rect = surf.get_rect(center=pos)
        surface.blit(surf, rect)

    @staticmethod
    def draw_animated_border(surface, rect, color, thickness, time_offset):
        pulse = abs(math.sin(pygame.time.get_ticks() / 300 + time_offset))
        animated_thickness = int(thickness + pulse * 2)

        pygame.draw.rect(surface, color, rect, animated_thickness, border_radius=8)

        inner_rect = rect.inflate(-10, -10)
        inner_color = (color[0] // 3, color[1] // 3, color[2] // 3)
        pygame.draw.rect(surface, inner_color, inner_rect, 1, border_radius=6)

    @staticmethod
    def draw_particle_effect(surface, center, time_offset, color):
        for i in range(8):
            angle = (pygame.time.get_ticks() / 30 + time_offset + i * 45) % 360
            dist = 80 + math.sin(pygame.time.get_ticks() / 500 + i) * 20

            x = center[0] + math.cos(math.radians(angle)) * dist
            y = center[1] + math.sin(math.radians(angle)) * dist

            alpha = int(100 + math.sin(pygame.time.get_ticks() / 200 + i) * 100)
            size = int(2 + math.sin(pygame.time.get_ticks() / 300 + i) * 1)

            p = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
            pygame.draw.circle(p, (*color, alpha), (size, size), size)
            surface.blit(p, (int(x - size), int(y - size)))


# ================================================================
#  CLASS: MenuUI (botones, panel de botones y manejo de clics)
# ================================================================
class MenuUI:

    def __init__(self, assets: MenuAssets):
        self.assets = assets

        menu_items = ["START GAME", "SETTINGS", "HIGH SCORES", "EXIT"]
        menu_positions = [
            (assets.SCREEN_WIDTH // 2, 400),
            (assets.SCREEN_WIDTH // 2, 460),
            (assets.SCREEN_WIDTH // 2, 520),
            (assets.SCREEN_WIDTH // 2, 580)
        ]

        # Crear botones
        buttons_list = [
            ButtonTextOnly(text, pos,
                           "assets/fonts/PressStart2P-Regular.ttf",
                           base_size=28,
                           hover_size=32,
                           text_color=WHITE,
                           hover_color=MENU_GLOW)
            for text, pos in zip(menu_items, menu_positions)
        ]

        self.menu_buttons = Buttons(assets.screen, buttons_list)

    # Dibujar panel y botones
    def draw(self):
        screen = self.assets.screen

        panel = pygame.Rect(100, 360,
                            self.assets.SCREEN_WIDTH - 200,
                            250)

        panel_surf = pygame.Surface(panel.size, pygame.SRCALPHA)
        panel_surf.fill((*DARK_BG, 150))

        screen.blit(panel_surf, panel.topleft)
        MenuVisualFX.draw_animated_border(screen, panel, DARK_GREY, 2, 2)

        # Botones
        self.menu_buttons.draw()


# ================================================================
#  CLASS: MainMenu  (control principal del menú)
# ================================================================
class MainMenu:

    def __init__(self):
        self.assets = MenuAssets()
        self.ui = MenuUI(self.assets)

    # ------------------------------------------------------------
    def main_menu(self):
        # Música
        if not pygame.mixer.get_init():
            pygame.mixer.init()

        music_ok = load_music("ambient.mp3", volume=0.6, loop=-1)
        if not music_ok:
            print("[WARN] No se pudo iniciar la música de fondo.")

        screen = self.assets.screen
        running = True

        while running:
            mouse_pos = pygame.mouse.get_pos()

            # ------------------ EVENTOS ------------------
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    clicked = self.ui.menu_buttons.handle_click(mouse_pos)

                    if clicked == "START GAME":
                        game = Game()
                        game.load_resources()
                        game.run()
                        running = False

                    elif clicked == "EXIT":
                        pygame.quit()
                        sys.exit()

            # ------------------ DIBUJADO ------------------
            screen.blit(self.assets.background, (0, 0))

            # Panel + Botones
            self.ui.draw()

            # Líneas decorativas
            line_y_top = 260
            line_y_bottom = 630

            for y in (line_y_top, line_y_bottom):
                pygame.draw.line(screen, DARK_GREY,
                                 (150, y),
                                 (self.assets.SCREEN_WIDTH - 150, y), 2)

                pulse = abs(math.sin(pygame.time.get_ticks() / 400))
                glow_len = int(50 + pulse * 100)
                cx = self.assets.SCREEN_WIDTH // 2

                pygame.draw.line(screen, MENU_GLOW,
                                 (cx - glow_len, y),
                                 (cx + glow_len, y), 3)

            # Cursor personalizado
            if self.assets.cursor_menu:
                screen.blit(self.assets.cursor_menu,
                            (mouse_pos[0] - 8, mouse_pos[1] - 8))

            pygame.display.flip()
            self.assets.clock.tick(self.assets.FPS)


# ================================================================
# EJECUCIÓN DIRECTA
# ================================================================
def main_menu():
    return MainMenu().main_menu()


if __name__ == "__main__":
    main_menu()

