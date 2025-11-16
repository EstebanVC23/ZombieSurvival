# core/game.py
import pygame
import random
import sys
from settings import *
from entities.player import Player
from entities.zombie import Zombie
from core.camera import Camera
<<<<<<< HEAD
from entities.spawner import Spawner
=======
from entities.spawner import WaveManager, Spawner
>>>>>>> main
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

<<<<<<< HEAD
        # Pantalla de carga
        self.loading_screen = LoadingScreen(self.screen, self.screen_width, self.screen_height)

        # Mundo
        self.world_width = WORLD_WIDTH
        self.world_height = WORLD_HEIGHT

        # ==== SPAWNER ACTUALIZADO (con rarezas) ====
        self.spawner = Spawner(self)
=======
        # Loading screen
        self.loading_screen = LoadingScreen(self.screen, self.screen_width, self.screen_height)

        # Mundo (usar constantes desde settings)
        self.world_width = WORLD_WIDTH
        self.world_height = WORLD_HEIGHT

        # Spawner reutilizable (Spawner encapsula la lógica de distancias)
        self.spawner = Spawner(self.world_width, self.world_height)
>>>>>>> main

        # Cursores
        self.cursor_game = load_cursor("ui/cursor_game.png", (32, 32))
        self.cursor_menu = load_cursor("ui/cursor_menu.png", (20, 20))
        self.current_cursor = self.cursor_game
        self.cursor_offset = pygame.Vector2(16, 16)

<<<<<<< HEAD
        # Inicializar estado del juego
=======
        # Inicializar estado de juego (player, grupos, camera, waves, etc)
>>>>>>> main
        self.initialize_game_state()

        # Música ambiente
        load_music("ambient.mp3", volume=0.6, loop=-1)

    # ============================================================
    def initialize_game_state(self):
        """Inicializa o reinicia todos los componentes del juego."""
<<<<<<< HEAD

        # Player
        self.player = Player((self.world_width / 2, self.world_height / 2))

        # Entidades
=======
        # Crear player en el centro del mundo
        self.player = Player((self.world_width / 2, self.world_height / 2))

        # Grupos de entidades
>>>>>>> main
        self.zombies = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.upgrades = pygame.sprite.Group()
        self.effects = pygame.sprite.Group()

<<<<<<< HEAD
        # Cámara y HUD
        self.camera = Camera(self.world_width, self.world_height)
=======
        # Cámara y manager de oleadas
        self.camera = Camera(self.world_width, self.world_height)
        self.wave_manager = WaveManager(self)

        # HUD, menús y UI
>>>>>>> main
        self.hud = HUD(self.font)
        self.pause_menu = PauseMenu(self.screen, self.screen_width, self.screen_height)
        self.ui_manager = UIManager(self.player)

<<<<<<< HEAD
        # ==== ZOMBIES INICIALES LEJOS DEL PLAYER ====
        min_distance = max(600, int((self.world_width + self.world_height) / 10))
=======
        # Zombies iniciales: siempre lejos del jugador
        # distancia mínima calculada de forma escalable según el mundo
        min_distance = max(600, int((self.world_width + self.world_height) / 10))
        for _ in range(8):
            pos = self.spawner.spawn_far_from_player(self.player.pos, min_distance=min_distance)
            self.zombies.add(Zombie(pos, "common"))
>>>>>>> main

        for _ in range(8):
            pos = self._spawn_initial_far(min_distance)
            self.zombies.add(Zombie(pos, "common", rarity="common"))

    # ============================================================
    def _spawn_initial_far(self, min_distance):
        """Genera posiciones iniciales lejos del jugador."""
        for _ in range(40):
            x = random.randint(0, self.world_width)
            y = random.randint(0, self.world_height)
            pos = pygame.Vector2(x, y)
            if pos.distance_to(self.player.pos) >= min_distance:
                return pos
        return pygame.Vector2(self.world_width, self.world_height)

    # ============================================================
    def run(self):
        print("[INFO] Iniciando el juego...")
        while self.running:
            dt = self.clock.tick(FPS) / 1000
            self.handle_events()

            if self.return_to_main_menu:
<<<<<<< HEAD
                return
=======
                return  # Volver al menú principal
>>>>>>> main

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

<<<<<<< HEAD
        # Si muere → menú de muerte
=======
        # Si el player murió, abrir lose menu
>>>>>>> main
        if self.player.health <= 0 and self.lose_menu is None:
            self.paused = True
            self.current_cursor = self.cursor_menu
            self.lose_menu = LoseMenu(self.screen, self.screen_width, self.screen_height)

        # Actualizar entidades
        for b in list(self.bullets):
            b.update(dt, self)
<<<<<<< HEAD

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
=======
        for z in list(self.zombies):
            z.update(dt, self)
        for u in list(self.upgrades):
            u.update(dt)
        for e in list(self.effects):
            e.update(dt)

        # Colisiones upgrades
        collided_upgrades = pygame.sprite.spritecollide(self.player, self.upgrades, dokill=True)
        for upgrade in collided_upgrades:
            print(f"[INFO] Player picked up upgrade '{upgrade.type}'")
            self.player.apply_upgrade(upgrade.type)

        # Actualizar cámara y oleadas
>>>>>>> main
        self.camera.update(self.player, self.screen_width, self.screen_height)

        # ==== SPAWNER REAL ====
        self.spawner.update(dt)

    # ============================================================
    def draw(self):
        # Fondo del mundo
        self.screen.fill((30, 30, 30))

        # Marco del mundo
        pygame.draw.rect(
            self.screen,
            (60, 60, 60),
            self.camera.apply(pygame.Rect(0, 0, self.world_width, self.world_height)),
            4
        )

<<<<<<< HEAD
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
=======
        # Dibujar entidades aplicando cámara
        for z in self.zombies:
            self.screen.blit(z.image, self.camera.apply(z.rect))
        for b in self.bullets:
            self.screen.blit(b.image, self.camera.apply(b.rect))
        for u in self.upgrades:
            self.screen.blit(u.image, self.camera.apply(u.rect))
        for e in self.effects:
            self.screen.blit(e.image, self.camera.apply(e.rect))
        self.screen.blit(self.player.image, self.camera.apply(self.player.rect))

        # HUD
        self.hud.draw(self.screen, self.player, self.wave_manager)

        # Menús overlay
>>>>>>> main
        if self.paused:
            self.pause_menu.draw()

        if self.lose_menu:
            self.lose_menu.draw()

<<<<<<< HEAD
        # Player Card
=======
        # Player card
>>>>>>> main
        if self.ui_manager.visible:
            self.ui_manager.draw_player_card(self.screen, self.font, self.screen_width, self.screen_height)

        # Cursor
        if self.current_cursor:
            mouse_pos = pygame.mouse.get_pos()
            cursor_rect = self.current_cursor.get_rect(center=mouse_pos)
            self.screen.blit(self.current_cursor, cursor_rect.topleft)

        pygame.display.flip()

    # ============================================================
    def reset_game(self):
        """Reinicia el juego completamente."""
        self.lose_menu = None
        self.paused = False
        self.return_to_main_menu = False
        self.current_cursor = self.cursor_game

<<<<<<< HEAD
        # Reset entidades
=======
        # Reiniciar entidades y lógica
>>>>>>> main
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

<<<<<<< HEAD
        # Reset Spawner
        self.spawner = Spawner(self)

        # Zombies iniciales lejos (rareza común)
        min_distance = max(600, int((self.world_width + self.world_height) / 10))
        for _ in range(8):
            pos = self._spawn_initial_far(min_distance)
            self.zombies.add(Zombie(pos, "common", rarity="common"))

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
=======
        # Zombies iniciales: siempre lejos del jugador
        min_distance = max(600, int((self.world_width + self.world_height) / 10))
        for _ in range(8):
            pos = self.spawner.spawn_far_from_player(self.player.pos, min_distance=min_distance)
            self.zombies.add(Zombie(pos, "common"))

    def load_resources(self):
        """Pantalla de carga completamente bloqueante. Nada del juego avanza."""
        # Pausar música si está sonando
        if pygame.mixer.get_init() and pygame.mixer.music.get_busy():
            pygame.mixer.music.pause()

        # Mostrar pantalla de carga y refrescar
        self.loading_screen.draw()
        pygame.display.flip()

        # Simula carga (reemplazar con carga real)
        resources = [
            "textures",
            "player",
            "zombies",
            "bullets",
            "upgrades",
            "effects",
            "hud",
            "sounds",
            "map"
>>>>>>> main
        ]

        total = len(resources)
        for i, r in enumerate(resources, 1):
<<<<<<< HEAD
            pygame.time.delay(200)
=======
            pygame.time.delay(200)   # simula tiempo de carga
>>>>>>> main
            self.loading_screen.update_progress(i / total)

        if pygame.mixer.get_init():
            pygame.mixer.music.unpause()
