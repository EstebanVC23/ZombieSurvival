import pygame
import sys
from utils.helpers import load_image_safe
from core.game import Game
from ui.buttons import ButtonTextOnly, Buttons

pygame.init()

# --- Configuración de pantalla ---
SCREEN_WIDTH = 700
SCREEN_HEIGHT = 700
FPS = 60

# --- Colores ---
WHITE = (240, 240, 240)
HIGHLIGHT = (0, 255, 180)

# --- Ventana ---
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Zombie Survival: Endless Apocalypse")
clock = pygame.time.Clock()

# --- Fondo ---
background = load_image_safe("menus/menu_bg.png")
if background:
    background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
else:
    print("[WARN] No se encontró la imagen de fondo, usando fondo negro.")
    background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    background.fill((10, 10, 10))

# --- Fuente ---
font_path = "assets/fonts/PressStart2P-Regular.ttf"
if not pygame.font.get_init():
    pygame.font.init()
try:
    base_font = pygame.font.Font(font_path, 28)
except:
    print("[WARN] No se encontró la fuente Press Start 2P, usando fuente por defecto.")
    base_font = pygame.font.Font(None, 28)

# --- Cursor ---
def load_cursor(path, size=(32, 32)):
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

pygame.mouse.set_visible(False)
cursor_menu = load_cursor("ui/cursor_menu.png", (20, 20))

# --- Botones del menú ---
menu_items = ["START GAME", "SETTINGS", "HIGH SCORES", "EXIT"]
menu_positions = [(SCREEN_WIDTH // 2, 400),
                  (SCREEN_WIDTH // 2, 460),
                  (SCREEN_WIDTH // 2, 520),
                  (SCREEN_WIDTH // 2, 580)]

buttons_list = [
    ButtonTextOnly(text, pos, font_path, base_size=28, hover_size=32, 
                   text_color=WHITE, hover_color=HIGHLIGHT)
    for text, pos in zip(menu_items, menu_positions)
]
menu_buttons = Buttons(screen, buttons_list)

# --- Main Menu ---
def main_menu():
    running = True

    # Música opcional
    sound_path = "sounds/ambient.mp3"
    if pygame.mixer and load_image_safe(sound_path):
        pygame.mixer.init()
        pygame.mixer.music.load(sound_path)
        pygame.mixer.music.set_volume(0.6)
        pygame.mixer.music.play(-1)

    while running:
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                clicked = menu_buttons.handle_click(mouse_pos)
                if clicked == "START GAME":
                    game = Game()
                    game.load_resources()
                    game.run()
                elif clicked == "SETTINGS":
                    print("[INFO] Configuración (pendiente)")
                elif clicked == "HIGH SCORES":
                    print("[INFO] Puntuaciones (pendiente)")
                elif clicked == "EXIT":
                    pygame.quit()
                    sys.exit()

        # --- Dibujar ---
        screen.blit(background, (0, 0))
        menu_buttons.draw()
        if cursor_menu:
            screen.blit(cursor_menu, (mouse_pos[0]-8, mouse_pos[1]-8))

        pygame.display.flip()
        clock.tick(FPS)

# --- Ejecución ---
if __name__ == "__main__":
    main_menu()
