import pygame
import sys
from settings import *
from entities.player import Player
from entities.spawner import Spawner
from core.camera import Camera
from ui.hud import HUD
from ui.pause_menu import PauseMenu
from ui.player_card import UIManager
from ui.lose_menu import LoseMenu
from utils.helpers import load_font, load_cursor, load_music
from ui.loading_screen import LoadingScreen


class EventHandler:
    """Maneja los eventos de pygame."""

    def __init__(self, game):
        self.game = game

    def handle_events(self):
        keys = pygame.key.get_pressed()
        self.game.ui_manager.visible = keys[pygame.K_e]

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game.running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.toggle_pause()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.handle_mouse_click(pygame.mouse.get_pos())

    def toggle_pause(self):
        self.game.paused = not self.game.paused
        self.game.current_cursor = self.game.cursor_menu if self.game.paused else self.game.cursor_game
        for z in self.game.zombies:
            try:
                z.pause_sound() if self.game.paused else z.resume_sound()
            except Exception:
                pass

    def handle_mouse_click(self, pos):
        if self.game.lose_menu:
            self.game.lose_menu.handle_click(pos, self.game)
        elif self.game.paused:
            self.game.pause_menu.handle_click(pos, self.game)
        else:
            self.game.player.shoot(pos, self.game)


class Updater:
    """Actualiza todas las entidades del juego."""

    def __init__(self, game):
        self.game = game

    def update(self, dt):
        # Player
        self.game.player.update(dt, self.game)

        # Muere → menú de muerte
        if self.game.player.health <= 0 and self.game.lose_menu is None:
            self.game.paused = True
            self.game.current_cursor = self.game.cursor_menu
            self.game.lose_menu = LoseMenu(self.game.screen, self.game.screen_width, self.game.screen_height)

        # Entidades
        for group in [self.game.bullets, self.game.zombies, self.game.upgrades, self.game.effects]:
            for entity in list(group):
                if hasattr(entity, "update"):
                    try:
                        entity.update(dt, self.game)  # Intenta pasar dt y game
                    except TypeError:
                        entity.update(dt)  # Si falla, pasa solo dt

        # Colisiones upgrades
        picked = pygame.sprite.spritecollide(self.game.player, self.game.upgrades, dokill=True)
        for up in picked:
            print(f"[INFO] Player picked up upgrade '{up.type}'")
            self.game.player.apply_upgrade(up.type)

        # Cámara
        self.game.camera.update(self.game.player, self.game.screen_width, self.game.screen_height)

        # Spawner
        self.game.spawner.update(dt)


class Drawer:
    """Dibuja todos los elementos en pantalla."""

    def __init__(self, game):
        self.game = game

    def draw(self):
        # Fondo
        self.game.screen.fill((30, 30, 30))

        # Marco mundo
        pygame.draw.rect(
            self.game.screen,
            (60, 60, 60),
            self.game.camera.apply(pygame.Rect(0, 0, self.game.world_width, self.game.world_height)),
            4
        )

        # Entidades
        self.draw_group(self.game.zombies)
        self.draw_group(self.game.bullets)
        self.draw_group(self.game.upgrades)
        self.draw_group(self.game.effects)

        # Player
        self.game.screen.blit(self.game.player.image, self.game.camera.apply(self.game.player.rect))

        # HUD
        self.game.hud.draw(self.game.screen, self.game.player, self.game.spawner)

        # Menús
        if self.game.paused:
            self.game.pause_menu.draw()
        if self.game.lose_menu:
            self.game.lose_menu.draw()

        # Player Card
        if self.game.ui_manager.visible:
            self.game.ui_manager.draw_player_card(
                self.game.screen, self.game.font, self.game.screen_width, self.game.screen_height
            )

        # Cursor
        self.draw_cursor()

        pygame.display.flip()

    def draw_group(self, group):
        for entity in group:
            self.game.screen.blit(entity.image, self.game.camera.apply(entity.rect))

    def draw_cursor(self):
        if self.game.current_cursor:
            mouse_pos = pygame.mouse.get_pos()
            cursor_rect = self.game.current_cursor.get_rect(center=mouse_pos)
            self.game.screen.blit(self.game.current_cursor, cursor_rect.topleft)


class Game:
    """Clase principal del juego."""

    def __init__(self):
        pygame.init()
        try:
            pygame.mixer.pre_init(44100, -16, 2, 512)
            if not pygame.mixer.get_init():
                pygame.mixer.init()
            pygame.mixer.set_num_channels(64)
        except Exception:
            pass

        # Pantalla fullscreen
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        info = pygame.display.Info()
        self.screen_width, self.screen_height = info.current_w, info.current_h
        pygame.display.set_caption("Zombie Survival: Endless Apocalypse")

        # Reloj / Fuente
        self.clock = pygame.time.Clock()
        self.font = load_font("PressStart2P-Regular.ttf", 18)

        # Estado
        self.running = True
        self.paused = False
        self.return_to_main_menu = False
        self.lose_menu = None

        # Pantalla de carga
        self.loading_screen = LoadingScreen(self.screen, self.screen_width, self.screen_height)

        # Mundo
        self.world_width = WORLD_WIDTH
        self.world_height = WORLD_HEIGHT

        # Cursores
        self.cursor_game = load_cursor("ui/cursor_game.png", (32, 32))
        self.cursor_menu = load_cursor("ui/cursor_menu.png", (20, 20))
        self.current_cursor = self.cursor_game
        self.cursor_offset = pygame.Vector2(16, 16)

        # Inicializar estado del juego
        self.initialize_game_state()

        # Música ambiente
        load_music("ambient.mp3", volume=0.6, loop=-1)

        # Módulos internos
        self.event_handler = EventHandler(self)
        self.updater = Updater(self)
        self.drawer = Drawer(self)

    # ============================================================
    def initialize_game_state(self):
        """Inicializa o reinicia todos los componentes del juego."""
        self.player = Player((self.world_width / 2, self.world_height / 2))
        self.zombies = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.upgrades = pygame.sprite.Group()
        self.effects = pygame.sprite.Group()
        self.camera = Camera(self.world_width, self.world_height)
        self.hud = HUD(self.font)
        self.pause_menu = PauseMenu(self.screen, self.screen_width, self.screen_height)
        self.ui_manager = UIManager(self.player)
        self.spawner = Spawner(self)

    # ============================================================
    # Loop principal
    # ============================================================
    def run(self):
        print("[INFO] Iniciando el juego...")
        while self.running:
            dt = self.clock.tick(FPS) / 1000
            self.event_handler.handle_events()
            if self.return_to_main_menu:
                return
            if not self.paused:
                self.updater.update(dt)
            self.drawer.draw()
        pygame.quit()
        sys.exit()

    # ============================================================
    # Recursos
    # ============================================================
    def load_resources(self):
        if pygame.mixer.get_init() and pygame.mixer.music.get_busy():
            pygame.mixer.music.pause()

        self.loading_screen.draw()
        pygame.display.flip()

        resources = [
            "textures", "player", "zombies", "bullets",
            "upgrades", "effects", "hud", "sounds", "map"
        ]
        total = len(resources)
        for i, r in enumerate(resources, 1):
            pygame.time.delay(200)
            self.loading_screen.update_progress(i / total)

        if pygame.mixer.get_init():
            pygame.mixer.music.unpause()

    # ============================================================
    # Reinicio
    # ============================================================
    def reset_game(self):
        self.lose_menu = None
        self.paused = False
        self.return_to_main_menu = False
        self.current_cursor = self.cursor_game
        self.initialize_game_state()
