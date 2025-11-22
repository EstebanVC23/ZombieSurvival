import pygame
from ui.lose_menu import LoseMenu


class Updater:
    """Actualiza todas las entidades del juego."""

    def __init__(self, game):
        self.game = game

    def update(self, dt):
        # ================================
        # Player
        # ================================
        self.game.player.update(dt, self.game)

        # Muere → menú de muerte
        if self.game.player.health <= 0 and self.game.lose_menu is None:
            self.game.paused = True
            self.game.current_cursor = self.game.cursor_menu

            # PASAR DATOS AL MENÚ DE DERROTA
            player_name = self.game.player.player_name
            player_score = self.game.player.score
            wave_reached = self.game.spawner.max_wave_completed

            self.game.lose_menu = LoseMenu(
                self.game.screen,
                self.game.screen_width,
                self.game.screen_height,
                player_name=player_name,
                player_score=player_score,
                wave_reached=wave_reached
            )

        # ================================
        # ENTIDADES (zombies, balas, upgrades, efectos)
        # ================================
        for group in [self.game.bullets, self.game.zombies, self.game.upgrades, self.game.effects]:
            for entity in list(group):
                if hasattr(entity, "update"):
                    try:
                        entity.update(dt, self.game)
                    except TypeError:
                        entity.update(dt)

        # ================================
        # 🚫 COLISIONES PLAYER vs OBJETOS
        # ================================
        if hasattr(self.game, "object_map") and self.game.object_map:
            try:
                self.game.object_map.resolve_collision(self.game.player)
            except Exception as e:
                print("[ERROR] Resolviendo colisión PLAYER con ObjectMap:", e)

        # ================================
        # 🚫 COLISIONES ZOMBIES vs OBJETOS
        # ================================
        for z in self.game.zombies:
            if hasattr(self.game, "object_map") and self.game.object_map:
                try:
                    self.game.object_map.resolve_collision(z)
                except Exception as e:
                    print("[ERROR] Resolviendo colisión ZOMBIE con ObjectMap:", e)

        # ================================
        # RECOGER UPGRADES
        # ================================
        picked = pygame.sprite.spritecollide(self.game.player, self.game.upgrades, dokill=True)
        for up in picked:
            print(f"[INFO] Player picked up upgrade '{up.type}'")
            self.game.player.apply_upgrade(up.type)

        # ================================
        # Cámara
        # ================================
        self.game.camera.update(self.game.player, self.game.screen_width, self.game.screen_height)

        # ================================
        # Spawner
        # ================================
        self.game.spawner.update(dt)
