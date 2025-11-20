import pygame

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