# main_menu.py
import pygame
import sys
import os
from core.game import Game  # Importa tu clase principal del juego

pygame.init()

# Configuración de pantalla
SCREEN_WIDTH = 700
SCREEN_HEIGHT = 700
FPS = 60

# Colores
WHITE = (240, 240, 240)
HIGHLIGHT = (0, 255, 180)

# Ventana principal
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Zombie Survival: Endless Apocalypse")
clock = pygame.time.Clock()

# --- Cargar imagen de fondo ---
bg_path = os.path.join("assets", "images", "menus", "menu_bg.png")
if os.path.exists(bg_path):
    background = pygame.image.load(bg_path).convert()
    background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
else:
    print("[WARN] No se encontró la imagen de fondo, usando fondo negro.")
    background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    background.fill((10, 10, 10))

# --- Fuente personalizada (Press Start 2P) ---
pygame.font.init()
font_path = os.path.join("assets", "fonts", "PressStart2P-Regular.ttf")

if os.path.exists(font_path):
    base_font = pygame.font.Font(font_path, 28)
else:
    print("[WARN] No se encontró la fuente Press Start 2P, usando fuente por defecto.")
    base_font = pygame.font.Font(None, 56)

# --- Opciones del menú ---
menu_items = ["START GAME", "SETTINGS", "HIGH SCORES", "EXIT"]

# Posiciones debajo del título
menu_positions = [
    (SCREEN_WIDTH // 2, 400),
    (SCREEN_WIDTH // 2, 460),
    (SCREEN_WIDTH // 2, 520),
    (SCREEN_WIDTH // 2, 580),
]

menu_rects = []


# ============================================================
# 🔹 Función para limpiar y escalar cursor
# ============================================================
def load_cursor(path, size=(32, 32)):
    """Carga un cursor PNG, limpia fondo blanco/gris y escala."""
    if not os.path.exists(path):
        print(f"[WARN] Cursor no encontrado: {path}")
        return None

    img = pygame.image.load(path).convert_alpha()
    img = pygame.transform.scale(img, size)

    clean = pygame.Surface(img.get_size(), pygame.SRCALPHA)
    img.lock()
    for x in range(img.get_width()):
        for y in range(img.get_height()):
            r, g, b, a = img.get_at((x, y))
            # Elimina fondo claro o casi blanco
            if a > 0 and (r + g + b) / 3 > 210:
                img.set_at((x, y), (0, 0, 0, 0))
    img.unlock()
    clean.blit(img, (0, 0))
    return clean


# ============================================================
# 🔹 Cargar cursor del menú
# ============================================================
pygame.mouse.set_visible(False)
cursor_menu_path = os.path.join("assets", "images", "ui", "cursor_menu.png")
cursor_menu = load_cursor(cursor_menu_path, (20, 20))


# ============================================================
# 🔹 Dibujo del menú
# ============================================================
def draw_menu(mouse_pos):
    screen.blit(background, (0, 0))
    menu_rects.clear()

    for i, text in enumerate(menu_items):
        pos = menu_positions[i]
        hovered = abs(mouse_pos[0] - pos[0]) < 150 and abs(mouse_pos[1] - pos[1]) < 25

        color = HIGHLIGHT if hovered else WHITE
        size = 36 if hovered else 28
        font = pygame.font.Font(font_path, size) if os.path.exists(font_path) else pygame.font.Font(None, size)

        label = font.render(text, True, color)
        rect = label.get_rect(center=pos)
        menu_rects.append((rect, text))

        screen.blit(label, rect)


# ============================================================
# 🔹 Bucle principal del menú
# ============================================================
def main_menu():
    running = True
    
    # ============================================================
    # 🔹 Música ambiental del menú
    # ============================================================
    sound_path = os.path.join("assets", "sounds", "ambient.mp3")

    if os.path.exists(sound_path):
        pygame.mixer.init()
        pygame.mixer.music.load(sound_path)
        pygame.mixer.music.set_volume(0.6)  # volumen alto en menú
        pygame.mixer.music.play(-1)  # reproducir en bucle
    else:
        print("[WARN] No se encontró la música ambiental:", sound_path)


    while running:
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for rect, text in menu_rects:
                    if rect.collidepoint(mouse_pos):
                        if text == "START GAME":
                            print("[INFO] Iniciando el juego...")
                            pygame.mixer.music.set_volume(0.2)  # volumen bajo en gameplay
                            game = Game()
                            game.run()
                            pygame.mixer.music.set_volume(0.6)  # restaurar volumen al salir del juego

                        elif text == "SETTINGS":
                            print("[INFO] Configuración (pendiente)")
                        elif text == "HIGH SCORES":
                            print("[INFO] Puntuaciones (pendiente)")
                        elif text == "EXIT":
                            pygame.quit()
                            sys.exit()

        # Dibujar menú y cursor
        draw_menu(mouse_pos)

        # 🔹 Dibujar cursor personalizado
        if cursor_menu:
            screen.blit(cursor_menu, (mouse_pos[0] - 8, mouse_pos[1] - 8))

        pygame.display.flip()
        clock.tick(FPS)


# ============================================================
# 🔹 Ejecución directa
# ============================================================
if __name__ == "__main__":
    main_menu()
