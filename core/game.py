import pygame
import random
import sys
import os
from settings import *
from entities.player import Player
from entities.zombie import Zombie
from core.camera import Camera
from entities.spawner import WaveManager
from core.upgrade import Upgrade
from ui.hud import HUD
from ui.pause_menu import PauseMenu
from ui.player_card import UIManager
from utils.helpers import load_image_safe

class Game:
    def __init__(self):
        # Inicializar audio antes si es posible
        try:
            # Pre-initialize audio with sensible defaults
            pygame.mixer.pre_init(44100, -16, 2, 512)
        except Exception:
            pass

        pygame.init()

        # Asegurar que el mixer esté listo y reservar canales
        try:
            if not pygame.mixer.get_init():
                pygame.mixer.init()
            pygame.mixer.set_num_channels(64)
        except Exception:
            pass

        # Pantalla completa
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        info = pygame.display.Info()
        self.screen_width, self.screen_height = info.current_w, info.current_h
        pygame.display.set_caption("Zombie Survival: Endless Apocalypse")

        self.clock = pygame.time.Clock()

        # Fuente
        try:
            self.font = pygame.font.Font("assets/fonts/PressStart2P-Regular.ttf", 18)
        except:
            self.font = pygame.font.SysFont("Arial", 18)
            print("[WARNING] Fuente no encontrada, usando Arial.")

        # Estado del juego
        self.running = True
        self.paused = False

        # Entidades
        self.player = Player((WORLD_WIDTH / 2, WORLD_HEIGHT / 2))
        self.zombies = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.upgrades = pygame.sprite.Group()
        self.effects = pygame.sprite.Group()
        self.camera = Camera(WORLD_WIDTH, WORLD_HEIGHT)
        self.wave_manager = WaveManager(self)

        self.hud = HUD(self.font)
        self.pause_menu = PauseMenu(self.screen, self.font, self.screen_width, self.screen_height)
        self.ui_manager = UIManager(self.player)

        # Cursores
        pygame.mouse.set_visible(False)
        self.cursor_game = self.load_cursor(os.path.join(ASSETS_IMAGES, "ui", "cursor_game.png"), (32, 32))
        self.cursor_menu = self.load_cursor(os.path.join(ASSETS_IMAGES, "ui", "cursor_menu.png"), (20, 20))
        self.current_cursor = self.cursor_game
        self.cursor_offset = pygame.Vector2(16, 16)

        # Zombies iniciales
        for _ in range(8):
            pos = (random.randint(0, WORLD_WIDTH), random.randint(0, WORLD_HEIGHT))
            self.zombies.add(Zombie(pos, "common"))

    # load_cursor igual que el tuyo (no modificado)
    def load_cursor(self, path, size):
        if not os.path.exists(path):
            print(f"[WARNING] Cursor no encontrado: {path}")
            return None
        img = pygame.image.load(path).convert_alpha()
        img = pygame.transform.scale(img, size)
        clean = pygame.Surface(img.get_size(), pygame.SRCALPHA)
        img.lock()
        for x in range(img.get_width()):
            for y in range(img.get_height()):
                r, g, b, a = img.get_at((x, y))
                if (r + g + b) / 3 > 160 or a < 80:
                    img.set_at((x, y), (0, 0, 0, 0))
        img.unlock()
        clean.blit(img, (0, 0))
        return clean

    def run(self):
        print("[INFO] Iniciando el juego...")
        while self.running:
            dt = self.clock.tick(FPS) / 1000
            self.handle_events()
            if not self.paused:
                self.update(dt)
            self.draw()
        print("[INFO] Cerrando juego...")
        pygame.quit()
        sys.exit()

    def handle_events(self):
        keys = pygame.key.get_pressed()
        self.ui_manager.visible = keys[pygame.K_e]

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    # alternar pausa
                    self.paused = not self.paused
                    self.current_cursor = self.cursor_menu if self.paused else self.cursor_game

                    # Pausar/Resumir solo sonidos de zombies
                    if self.paused:
                        for z in self.zombies:
                            try:
                                z.pause_sound()
                            except Exception:
                                pass
                    else:
                        for z in self.zombies:
                            try:
                                z.resume_sound()
                            except Exception:
                                pass

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.paused:
                    self.pause_menu.handle_click(pygame.mouse.get_pos(), self)
                else:
                    self.player.shoot(pygame.mouse.get_pos(), self)

    def update(self, dt):
        self.player.update(dt, self)

        for b in list(self.bullets):
            b.update(dt, self)

        for z in list(self.zombies):
            z.update(dt, self)

        for u in list(self.upgrades):
            u.update(dt)

        for e in list(self.effects):
            e.update(dt)

        # Colisión jugador <-> mejora
        collided_upgrades = pygame.sprite.spritecollide(self.player, self.upgrades, dokill=True)
        for upgrade in collided_upgrades:
            print(f"[INFO] Player picked up upgrade '{upgrade.type}'")
            self.player.apply_upgrade(upgrade.type)

        self.camera.update(self.player, self.screen_width, self.screen_height)
        self.wave_manager.update(dt)

    def draw(self):
        self.screen.fill((30, 30, 30))

        pygame.draw.rect(
            self.screen,
            (60, 60, 60),
            self.camera.apply(pygame.Rect(0, 0, WORLD_WIDTH, WORLD_HEIGHT)),
            4
        )

        # Orden de dibujo
        for z in self.zombies:
            self.screen.blit(z.image, self.camera.apply(z.rect))
        for b in self.bullets:
            self.screen.blit(b.image, self.camera.apply(b.rect))
        for u in self.upgrades:
            self.screen.blit(u.image, self.camera.apply(u.rect))
        for e in self.effects:
            self.screen.blit(e.image, self.camera.apply(e.rect))

        self.screen.blit(self.player.image, self.camera.apply(self.player.rect))

        self.hud.draw(self.screen, self.player, self.wave_manager)

        if self.paused:
            self.pause_menu.draw()

        if self.ui_manager.visible:
            self.ui_manager.draw_player_card(self.screen, self.font, self.screen_width, self.screen_height)

        if self.current_cursor:
            mouse_pos = pygame.mouse.get_pos()
            cursor_rect = self.current_cursor.get_rect(center=mouse_pos)
            self.screen.blit(self.current_cursor, cursor_rect.topleft)

        pygame.display.flip()
