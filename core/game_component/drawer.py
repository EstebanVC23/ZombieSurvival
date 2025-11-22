import pygame
import traceback

class Drawer:
    """Dibuja todos los elementos en pantalla."""

    def __init__(self, game):
        self.game = game

    def draw(self):
        # Fondo base
        self.game.screen.fill((30, 30, 30))

        # ============================================================
        # 🔹 1. DIBUJAR TERRENO (SIEMPRE AL FONDO)
        # ============================================================
        if hasattr(self.game, "terrain_map") and self.game.terrain_map:
            try:
                self.game.terrain_map.draw(self.game.screen, self.game.camera)
            except Exception:
                print("[ERROR] Excepción dibujando terrain_map")
                traceback.print_exc()

        # ============================================================
        # 🔹 2. DIBUJAR ENTIDADES (ZOMBIES, BALAS, ETC.)
        #    → Estas van DETRÁS de los objetos ahora
        # ============================================================
        self.draw_group(self.game.zombies)
        self.draw_group(self.game.bullets)
        self.draw_group(self.game.upgrades)
        self.draw_group(self.game.effects)

        # ============================================================
        # 🔹 3. DIBUJAR PLAYER (TAMBIÉN DETRÁS DE OBJETOS)
        # ============================================================
        self.game.screen.blit(self.game.player.image, self.game.camera.apply(self.game.player.rect))

        # ============================================================
        # 4. DIBUJAR OBJETOS DEL MAPA CON PROFUNDIDAD
        # ============================================================
        if hasattr(self.game, "object_map") and self.game.object_map:
            try:
                # Mezclar objetos y player, y ordenar por Y (rect.bottom)
                drawables = self.game.object_map.objects + [self.game.player]
                drawables.sort(key=lambda o: o.rect.bottom)

                for obj in drawables:
                    self.game.screen.blit(obj.image, self.game.camera.apply(obj.rect))

            except Exception:
                print("[ERROR] Excepción dibujando object_map ordenado")
                traceback.print_exc()


        # ============================================================
        # Marco mundo (opcional)
        # ============================================================
        pygame.draw.rect(
            self.game.screen,
            (60, 60, 60),
            self.game.camera.apply(pygame.Rect(0, 0, self.game.world_width, self.game.world_height)),
            4
        )

        # ============================================================
        # HUD Y MENÚS
        # ============================================================
        self.game.hud.draw(self.game.screen, self.game.player, self.game.spawner)

        if self.game.paused:
            self.game.pause_menu.draw()

        if self.game.lose_menu:
            self.game.lose_menu.draw()

        if self.game.ui_manager.visible:
            self.game.ui_manager.draw_player_card(
                self.game.screen, self.game.font, self.game.screen_width, self.game.screen_height
            )

        # ============================================================
        # Cursor
        # ============================================================
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
