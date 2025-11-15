# ui/hud.py
import pygame
import math
from ui.map import MiniMap  # clase definida arriba
from settings import UPGRADE_VALUES  # solo si la usas en hud, la dejo por compatibilidad


class HUD:
    """
    HUD principal. Firma pública:
      hud = HUD(font)
      hud.draw(surface, player, wave_manager)

    - Este HUD contiene internamente un MiniMap (creado bajo demanda la primera vez que draw es llamado).
    - El minimapa se actualiza internamente cada 0.1s (100 ms) para no degradar rendimiento.
    """

    def __init__(self, font):
        self.font = font
        self.minimap = None  # se crea la primera vez que tenemos acceso a game en draw()

    def _ensure_minimap(self, wave_manager):
        """Crear minimapa si aún no existe (necesita referencia a game)."""
        if self.minimap is None:
            game = getattr(wave_manager, "game", None)
            if game is not None:
                # tamaño y posición: top-right (pediste top-right)
                self.minimap = MiniMap(game=game, width=180, height=180, margin=8, position="topright", update_interval_ms=100)

    def draw(self, surface, player, wave_manager):
        # ==========================
        # BARRA DE VIDA (PLAYER)
        # ==========================
        max_hp = getattr(player, "max_health", 100)
        bar_width = 250
        bar_height = 18
        x, y = 30, 30
        hp_ratio = max(0, player.health / max_hp)

        # fondo + barra HP
        pygame.draw.rect(surface, (0, 0, 0), (x - 3, y - 3, bar_width + 6, bar_height + 6))
        pygame.draw.rect(surface, (40, 40, 40), (x, y, bar_width, bar_height))
        hp_color = (200, 50, 50) if hp_ratio < 0.3 else (255, 180, 50) if hp_ratio < 0.6 else (50, 200, 80)
        pygame.draw.rect(surface, hp_color, (x, y, int(bar_width * hp_ratio), bar_height))

        hp_text = self.font.render(f"HP {int(player.health)}/{int(max_hp)}", True, (255, 255, 255))
        surface.blit(hp_text, (x + 260, y - 2))

        # ==========================
        # BARRA DE ESCUDO (SHIELD)
        # ==========================
        max_shield = getattr(player, "max_shield", 0)
        if max_shield > 0:
            shield_ratio = max(0, player.shield / max_shield)
            shield_y = y + 32  # debajo de la barra de vida

            pygame.draw.rect(surface, (0, 0, 0), (x - 3, shield_y - 3, bar_width + 6, bar_height + 6))
            pygame.draw.rect(surface, (40, 40, 60), (x, shield_y, bar_width, bar_height))

            shield_color = (80, 80, 255) if shield_ratio > 0.3 else (120, 120, 255)
            pygame.draw.rect(surface, shield_color, (x, shield_y, int(bar_width * shield_ratio), bar_height))

            shield_text = self.font.render(f"SHIELD {int(player.shield)}/{int(max_shield)}", True, (180, 180, 255))
            surface.blit(shield_text, (x + 260, shield_y))

        # ==========================
        # SCORE, WAVE, ZOMBIES LEFT
        # ==========================
        score_text = self.font.render(f"SCORE: {player.score}", True, (255, 255, 255))
        surface.blit(score_text, (30, 100))

        wave_text = self.font.render(f"WAVE: {wave_manager.current_wave}", True, (255, 255, 100))
        surface.blit(wave_text, (30, 140))

        # recalculamos conteo de vivos (excluye zombies.dead == True)
        alive = sum(1 for z in wave_manager.game.zombies if not getattr(z, "dead", False))
        total_left = wave_manager.enemies_to_spawn + alive
        zombies_text = self.font.render(f"ZOMBIES LEFT: {total_left}", True, (255, 120, 120))
        surface.blit(zombies_text, (30, 180))

        # ==========================
        # AMMO HUD (abajo izquierda)
        # ==========================
        sw = surface.get_width()
        sh = surface.get_height()
        ammo_x = 30
        ammo_y = sh - 60

        circle_center = (ammo_x + 24, ammo_y + 6)
        circle_radius = 18

        pygame.draw.circle(surface, (30, 30, 30), circle_center, circle_radius)
        pygame.draw.circle(surface, (0, 0, 0), circle_center, circle_radius, 2)

        if getattr(player, "weapon", None) and player.weapon.is_reloading:
            progress = max(0.0, min(1.0, player.weapon.reload_timer / max(0.0001, player.weapon.reload_time)))
            start_angle = -math.pi / 2
            end_angle = start_angle + progress * (2 * math.pi)
            rect = pygame.Rect(circle_center[0] - circle_radius, circle_center[1] - circle_radius, circle_radius * 2, circle_radius * 2)
            pygame.draw.arc(surface, (200, 200, 255), rect, start_angle, end_angle, 6)
        else:
            pygame.draw.circle(surface, (80, 220, 80), circle_center, 6)

        if getattr(player, "weapon", None):
            ammo_text = self.font.render(f"AMMO: {player.weapon.current_ammo}/{player.weapon.max_ammo} | {player.weapon.reserve_ammo}", True, (255, 255, 255))
            surface.blit(ammo_text, (ammo_x + 60, ammo_y - 4))
            if player.weapon.is_reloading:
                reload_text = self.font.render("RELOADING...", True, (200, 200, 255))
                surface.blit(reload_text, (ammo_x + 110, ammo_y - 30))

        # ==========================
        # BARRA DE VIDA DE ZOMBIES (dibujada debajo en pantalla) - ya la tenías
        # NOTA: esta sección no ha sido tocada funcionalmente, solo la dejo aquí si la quieres.
        # ==========================
        camera = getattr(wave_manager.game, "camera", None)
        screen_rect = surface.get_rect()

        for z in wave_manager.game.zombies:
            # ignorar cadáveres (si quieres que aparezca, quita esta condición)
            if getattr(z, "dead", False):
                continue
            if not hasattr(z, "hp") or not hasattr(z, "rect"):
                continue

            # convertir rect mundo -> pantalla si existe camera; si no, usamos rect
            try:
                z_screen_rect = camera.apply(z.rect) if camera is not None else z.rect
            except Exception:
                z_screen_rect = z.rect

            # si está fuera de pantalla, no dibujar
            if not screen_rect.colliderect(z_screen_rect):
                continue

            zx = z_screen_rect.centerx
            zy = z_screen_rect.bottom + 4

            max_z_hp = z.TYPE_STATS.get(z.type, {}).get("hp", getattr(z, "hp", 1))
            hp_ratio = max(0.0, min(1.0, (z.hp / max_z_hp) if max_z_hp else 0.0))

            bar_w = max(24, z_screen_rect.width // 2)  # ahora 50% del ancho del sprite (según petición)
            bar_h = 6

            pygame.draw.rect(surface, (0, 0, 0), (zx - bar_w // 2 - 1, zy - 1, bar_w + 2, bar_h + 2))
            pygame.draw.rect(surface, (60, 60, 60), (zx - bar_w // 2, zy, bar_w, bar_h))

            if hp_ratio < 0.3:
                col = (220, 40, 40)
            elif hp_ratio < 0.6:
                col = (255, 180, 40)
            else:
                col = (60, 220, 60)

            pygame.draw.rect(surface, col, (zx - bar_w // 2, zy, int(bar_w * hp_ratio), bar_h))

        # ==========================
        # MINIMAP (arriba derecha) - creado bajo demanda
        # ==========================
        self._ensure_minimap(wave_manager)
        if self.minimap:
            # notificar al minimapa que actualice si corresponde (internamente hace throttling)
            self.minimap.draw(surface)
