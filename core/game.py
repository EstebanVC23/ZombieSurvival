import pygame
import random
import sys
from settings import *
from entities.player import Player
from entities.zombie import Zombie
from core.camera import Camera
from entities.spawner import WaveManager
from ui.hud import HUD
from ui.pause_menu import PauseMenu
from ui.player_card import UIManager
from ui.lose_menu import LoseMenu
from utils.helpers import load_font, load_cursor, load_music

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

        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        info = pygame.display.Info()
        self.screen_width, self.screen_height = info.current_w, info.current_h
        pygame.display.set_caption("Zombie Survival: Endless Apocalypse")

        self.clock = pygame.time.Clock()
        self.font = load_font("PressStart2P-Regular.ttf", 18)

        self.running = True
        self.paused = False
        self.return_to_main_menu = False
        self.lose_menu = None

        self.cursor_game = load_cursor("ui/cursor_game.png", (32, 32))
        self.cursor_menu = load_cursor("ui/cursor_menu.png", (20, 20))
        self.current_cursor = self.cursor_game
        self.cursor_offset = pygame.Vector2(16, 16)

        self.initialize_game_state()

        load_music("ambient.mp3", volume=0.6, loop=-1)

    def initialize_game_state(self):
        """Inicializa o reinicia todos los componentes del juego."""
        self.player = Player((WORLD_WIDTH / 2, WORLD_HEIGHT / 2))
        self.zombies = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.upgrades = pygame.sprite.Group()
        self.effects = pygame.sprite.Group()
        self.camera = Camera(WORLD_WIDTH, WORLD_HEIGHT)
        self.wave_manager = WaveManager(self)
        self.hud = HUD(self.font)  # Reinicia HUD y minimapa
        self.pause_menu = PauseMenu(self.screen, self.screen_width, self.screen_height)
        self.ui_manager = UIManager(self.player)

        for _ in range(8):
            pos = (random.randint(0, WORLD_WIDTH), random.randint(0, WORLD_HEIGHT))
            self.zombies.add(Zombie(pos, "common"))

    def run(self):
        print("[INFO] Iniciando el juego...")
        while self.running:
            dt = self.clock.tick(FPS) / 1000
            self.handle_events()

            if self.return_to_main_menu:
                return  # Salir del bucle para volver al menú principal

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

    def update(self, dt):
        self.player.update(dt, self)

        if self.player.health <= 0 and self.lose_menu is None:
            self.paused = True
            self.current_cursor = self.cursor_menu
            self.lose_menu = LoseMenu(self.screen, self.screen_width, self.screen_height)

        for b in list(self.bullets): b.update(dt, self)
        for z in list(self.zombies): z.update(dt, self)
        for u in list(self.upgrades): u.update(dt)
        for e in list(self.effects): e.update(dt)

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

        for z in self.zombies: self.screen.blit(z.image, self.camera.apply(z.rect))
        for b in self.bullets: self.screen.blit(b.image, self.camera.apply(b.rect))
        for u in self.upgrades: self.screen.blit(u.image, self.camera.apply(u.rect))
        for e in self.effects: self.screen.blit(e.image, self.camera.apply(e.rect))
        self.screen.blit(self.player.image, self.camera.apply(self.player.rect))

        self.hud.draw(self.screen, self.player, self.wave_manager)

        if self.paused:
            self.pause_menu.draw()

        if self.lose_menu:
            self.lose_menu.draw()

        if self.ui_manager.visible:
            self.ui_manager.draw_player_card(self.screen, self.font, self.screen_width, self.screen_height)

        if self.current_cursor:
            mouse_pos = pygame.mouse.get_pos()
            cursor_rect = self.current_cursor.get_rect(center=mouse_pos)
            self.screen.blit(self.current_cursor, cursor_rect.topleft)

        pygame.display.flip()

    def reset_game(self):
        """Reinicia completamente el estado del juego como si se iniciara desde el menú principal."""
        self.lose_menu = None
        self.paused = False
        self.return_to_main_menu = False
        self.current_cursor = self.cursor_game

        # Reiniciar entidades y lógica
        self.player = Player((WORLD_WIDTH / 2, WORLD_HEIGHT / 2))
        self.zombies.empty()
        self.bullets.empty()
        self.upgrades.empty()
        self.effects.empty()

        # Reiniciar lógica de oleadas y HUD
        self.wave_manager = WaveManager(self)
        self.hud = HUD(self.font)
        self.camera = Camera(WORLD_WIDTH, WORLD_HEIGHT)
        self.pause_menu = PauseMenu(self.screen, self.screen_width, self.screen_height)
        self.ui_manager = UIManager(self.player)

        # Zombies iniciales
        for _ in range(8):
            pos = (random.randint(0, WORLD_WIDTH), random.randint(0, WORLD_HEIGHT))
            self.zombies.add(Zombie(pos, "common"))