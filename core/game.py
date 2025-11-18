import pygame
import random
import sys
from settings import *
from entities.player import Player
from entities.zombie import Zombie
from core.camera import Camera
from entities.spawner import Spawner
from ui.hud import HUD
from ui.pause_menu import PauseMenu
from ui.player_card import UIManager
from ui.lose_menu import LoseMenu
from utils.helpers import load_font, load_cursor, load_music
from ui.loading_screen import LoadingScreen


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

    # ============================================================
    def initialize_game_state(self):
        """Inicializa o reinicia todos los componentes del juego."""

        # Player
        self.player = Player((self.world_width / 2, self.world_height / 2))

        # Entidades
        self.zombies = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.upgrades = pygame.sprite.Group()
        self.effects = pygame.sprite.Group()

        # Cámara y HUD
        self.camera = Camera(self.world_width, self.world_height)
        self.hud = HUD(self.font)
        self.pause_menu = PauseMenu(self.screen, self.screen_width, self.screen_height)
        self.ui_manager = UIManager(self.player)

        # ==== Spawner completo
        self.spawner = Spawner(self)

    # ============================================================
    def run(self):
        print("[INFO] Iniciando el juego...")
        while self.running:
            dt = self.clock.tick(FPS) / 1000
            self.handle_events()

            if self.return_to_main_menu:
                return

            if not self.paused:
                self.update(dt)

            self.draw()
        pygame.quit()
        sys.exit()

    # ============================================================
    def handle_events(self):
        keys = pygame.key.get_pressed()
        self.ui_manager.visible = keys[pygame.K_e]

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.paused = not self.paused
                    self.current_cursor = self.cursor_menu if self.paused else self.cursor_game

                    for z in self.zombies:
                        try:
                            z.pause_sound() if self.paused else z.resume_sound()
                        except Exception:
                            pass

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.lose_menu:
                    self.lose_menu.handle_click(pygame.mouse.get_pos(), self)
                elif self.paused:
                    self.pause_menu.handle_click(pygame.mouse.get_pos(), self)
                else:
                    self.player.shoot(pygame.mouse.get_pos(), self)

    # ============================================================
    def update(self, dt):
        # Actualizar player
        self.player.update(dt, self)

        # Si muere → menú de muerte
        if self.player.health <= 0 and self.lose_menu is None:
            self.paused = True
            self.current_cursor = self.cursor_menu
            self.lose_menu = LoseMenu(self.screen, self.screen_width, self.screen_height)

        # Actualizar entidades
        for b in list(self.bullets):
            b.update(dt, self)

        for z in list(self.zombies):
            z.update(dt, self)

        for u in list(self.upgrades):
            u.update(dt)

        for e in list(self.effects):
            e.update(dt)

        # Colisiones upgrades
        picked = pygame.sprite.spritecollide(self.player, self.upgrades, dokill=True)
        for up in picked:
            print(f"[INFO] Player picked up upgrade '{up.type}'")
            self.player.apply_upgrade(up.type)

        # Cámara
        self.camera.update(self.player, self.screen_width, self.screen_height)

        # ==== SPAWNER REAL ====
        self.spawner.update(dt)

    # ============================================================
    def draw(self):
        # Fondo
        self.screen.fill((30, 30, 30))

        # Marco mundo
        pygame.draw.rect(
            self.screen,
            (60, 60, 60),
            self.camera.apply(pygame.Rect(0, 0, self.world_width, self.world_height)),
            4
        )

        # Zombies
        for z in self.zombies:
            self.screen.blit(z.image, self.camera.apply(z.rect))

        # Balas
        for b in self.bullets:
            self.screen.blit(b.image, self.camera.apply(b.rect))

        # Upgrades
        for u in self.upgrades:
            self.screen.blit(u.image, self.camera.apply(u.rect))

        # Efectos
        for e in self.effects:
            self.screen.blit(e.image, self.camera.apply(e.rect))

        # Player
        self.screen.blit(self.player.image, self.camera.apply(self.player.rect))

        # HUD
        self.hud.draw(self.screen, self.player, self.spawner)

        # Menús
        if self.paused:
            self.pause_menu.draw()

        if self.lose_menu:
            self.lose_menu.draw()

        # Player Card
        if self.ui_manager.visible:
            self.ui_manager.draw_player_card(self.screen, self.font, self.screen_width, self.screen_height)

        # Cursor
        if self.current_cursor:
            mouse_pos = pygame.mouse.get_pos()
            cursor_rect = self.current_cursor.get_rect(center=mouse_pos)
            self.screen.blit(self.current_cursor, cursor_rect.topleft)

        pygame.display.flip()

    # ============================================================
    
    def load_resources(self):
        """Pantalla de carga bloqueante."""
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

    def reset_game(self):
        """Reinicia el juego completamente."""
        self.lose_menu = None
        self.paused = False
        self.return_to_main_menu = False
        self.current_cursor = self.cursor_game

        # Reset entidades
        self.player = Player((self.world_width / 2, self.world_height / 2))
        self.zombies.empty()
        self.bullets.empty()
        self.upgrades.empty()
        self.effects.empty()

        # Reset HUD / cámara
        self.hud = HUD(self.font)
        self.camera = Camera(self.world_width, self.world_height)
        self.pause_menu = PauseMenu(self.screen, self.screen_width, self.screen_height)
        self.ui_manager = UIManager(self.player)

        # Reset Spawner
        self.spawner = Spawner(self)
