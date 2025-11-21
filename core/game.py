import pygame
import sys
import math
import traceback

from settings import *
from entities.player import Player
from entities.spawner import Spawner
from core.camera import Camera
from ui.hud import HUD
from ui.pause_menu import PauseMenu
from ui.player_card import UIManager
from utils.helpers import load_font, load_cursor, load_music
from ui.loading_screen import LoadingScreen

from core.game_component.drawer import Drawer
from core.game_component.event_handler import EventHandler
from core.game_component.updater import Updater

from core.map_loader import load_map_file
from core.terrain import TileMap


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
            traceback.print_exc()
            print("[ERROR] Fallo inicializando pygame.mixer")

        # Pantalla fullscreen inicial
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

        # Inicializar estado del juego
        print("[DEBUG] Inicializando estado del juego...")
        self.initialize_game_state()

        # Música ambiente
        try:
            load_music("ambient.mp3", volume=0.6, loop=-1)
        except Exception:
            traceback.print_exc()
            print("[ERROR] No se pudo cargar la música ambiente")

        # Módulos internos
        self.event_handler = EventHandler(self)
        self.updater = Updater(self)
        self.drawer = Drawer(self)

    # ============================================================
    def initialize_game_state(self):
        print("[DEBUG] initialize_game_state() llamado")

        # Ruta del archivo del mapa — SIEMPRE cargado desde txt
        map_path = "assets/maps/map01.txt"

        # Carga directa SIN generación procedural
        mapa, cols, rows = load_map_file(
            map_path,
            WORLD_WIDTH,
            WORLD_HEIGHT
        )

        print(f"[DEBUG] Mapa cargado desde archivo: {cols}x{rows} tiles")

        # Crear tilemap
        self.tilemap = TileMap(
            mapa,
            tile_size=TERRAIN_TILE_SIZE
        )

        # === 3) Mantener dimensiones del mundo ===
        self.world_width = WORLD_WIDTH
        self.world_height = WORLD_HEIGHT

        # === 4) Inicializar entidades ===
        self.player = Player((self.world_width / 2, self.world_height / 2))
        self.zombies = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.upgrades = pygame.sprite.Group()
        self.effects = pygame.sprite.Group()

        # Cámara y UI
        self.camera = Camera(self.world_width, self.world_height)
        self.hud = HUD(self.font)
        self.pause_menu = PauseMenu(self.screen, self.screen_width, self.screen_height)
        self.ui_manager = UIManager(self.player)

        # Spawner
        self.spawner = Spawner(self)

        print("[DEBUG] Estado del juego listo (player, tilemap, spawner, grupos...)")

    # ============================================================
    # Loop principal
    # ============================================================
    def run(self):
        print("[INFO] Iniciando el juego...")

        while self.running:
            dt = self.clock.tick(FPS) / 1000

            try:
                self.event_handler.handle_events()
            except Exception:
                print("[ERROR] Excepción en event_handler.handle_events()")
                traceback.print_exc()

            if self.return_to_main_menu:
                print("[DEBUG] return_to_main_menu activado, limpiando zombies y saliendo al menú")
                for z in self.zombies:
                    try:
                        if hasattr(z, "sound") and z.sound:
                            z.sound.stop()
                    except Exception:
                        traceback.print_exc()
                        print("[ERROR] No se pudo detener sonido de zombie")
                self.zombies.empty()
                return

            if not self.paused:
                try:
                    self.updater.update(dt)
                except Exception:
                    print("[ERROR] Excepción dentro de updater.update()")
                    traceback.print_exc()

            try:
                self.drawer.draw()
            except Exception:
                print("[ERROR] Excepción dentro de drawer.draw()")
                traceback.print_exc()

        pygame.quit()
        sys.exit()

    # ============================================================
    # Recursos
    # ============================================================
    def load_resources(self):
        print("[DEBUG] Cargando recursos...")

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
            print(f"[DEBUG] Cargando recurso: {r} ({i}/{total})")
            pygame.time.delay(200)
            self.loading_screen.update_progress(i / total)

        if pygame.mixer.get_init():
            pygame.mixer.music.unpause()

        print("[DEBUG] Carga de recursos finalizada")

    # ============================================================
    # Reinicio
    # ============================================================
    def reset_game(self):
        print("[DEBUG] reset_game() llamado")

        self.lose_menu = None
        self.paused = False
        self.return_to_main_menu = False
        self.current_cursor = self.cursor_game

        try:
            self.initialize_game_state()
        except Exception:
            print("[ERROR] Excepción en initialize_game_state durante reset_game()")
            traceback.print_exc()

        print("[DEBUG] Game reset completo")
