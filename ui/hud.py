import pygame
import math
import time
from ui.map import MiniMap
from entities.zombie import ZombieStats
from settings import *
from colors import *


# ============================================================
# HEALTH BAR (SEPARADA)
# ============================================================
class HealthBarHUD:
    def __init__(self, font=None):
        self.font = font if font else pygame.font.Font(None, 28)
        self.hp_display = 100
        self.pulse_timer = 0

    def _draw_rounded_rect(self, surface, color, rect, radius=8):
        pygame.draw.rect(surface, color, rect, border_radius=radius)

    def _draw_gradient_bar(self, surface, rect, color_start, color_end):
        if rect.width <= 0:
            return

        temp = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)

        for x in range(rect.width):
            t = x / max(1, rect.width)
            r = int(color_start[0] + (color_end[0] - color_start[0]) * t)
            g = int(color_start[1] + (color_end[1] - color_start[1]) * t)
            b = int(color_start[2] + (color_end[2] - color_start[2]) * t)
            pygame.draw.line(temp, (r, g, b), (x, 0), (x, rect.height))

        surface.blit(temp, rect.topleft)

    def draw(self, surface, player, x=30, y=30):
        self.pulse_timer += 0.05

        # -----------------------------------------------
        # ✔ VIDA REAL LEÍDA DE player.stats (fix real)
        # -----------------------------------------------
        stats = player.stats
        max_hp = max(1, stats.max_health)
        current_hp = max(0, stats.health)

        # animación suave
        self.hp_display += (current_hp - self.hp_display) * 0.15

        bar_width = 250
        bar_height = 20
        shadow = 4

        hp_ratio = max(0, min(1, current_hp / max_hp))

        # sombra
        self._draw_rounded_rect(surface, BLACK + (120,), (x + shadow, y + shadow, bar_width, bar_height), 10)

        # fondo
        self._draw_rounded_rect(surface, DARK_BG, (x, y, bar_width, bar_height), 10)

        # borde
        pygame.draw.rect(surface, BORDER_GREY + (200,), (x, y, bar_width, bar_height), width=2, border_radius=10)

        # barra HP
        if hp_ratio > 0:
            hp_rect = pygame.Rect(x + 2, y + 2, int((bar_width - 4) * hp_ratio), bar_height - 4)

            if hp_ratio < 0.3:
                c1, c2 = HP_RED_DARK, HP_RED_LIGHT
            elif hp_ratio < 0.6:
                c1, c2 = (255, 140, 30), (255, 180, 50)
            else:
                c1, c2 = GREEN, (60, 220, 90)

            self._draw_gradient_bar(surface, hp_rect, c1, c2)

        # texto
        txt = f"HP {int(current_hp)}/{int(max_hp)}"
        text = self.font.render(txt, True, HP_LABEL)
        surface.blit(text, (x + bar_width + 12, y - 2))


# ============================================================
# SHIELD BAR (SEPARADA)
# ============================================================
class ShieldBarHUD:
    def __init__(self, font=None):
        self.font = font if font else pygame.font.Font(None, 28)
        self.shield_display = 0
        self.pulse_timer = 0

    def _draw_rounded_rect(self, surface, color, rect, radius=8):
        pygame.draw.rect(surface, color, rect, border_radius=radius)

    def _draw_gradient_bar(self, surface, rect, c1, c2):
        if rect.width <= 0:
            return

        temp = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)

        for x in range(rect.width):
            t = x / max(1, rect.width)
            r = int(c1[0] + (c2[0] - c1[0]) * t)
            g = int(c1[1] + (c2[1] - c1[1]) * t)
            b = int(c1[2] + (c2[2] - c1[2]) * t)
            pygame.draw.line(temp, (r, g, b), (x, 0), (x, rect.height))

        surface.blit(temp, rect.topleft)

    def draw(self, surface, player, x=30, y=64):
        self.pulse_timer += 0.05
        pulse = abs(math.sin(self.pulse_timer)) * 0.3 + 0.7

        # -----------------------------------------------
        # ✔ ESCUDO REAL LEÍDO DE player.stats (fix real)
        # -----------------------------------------------
        stats = player.stats
        max_shield = max(1, stats.max_shield)
        current_shield = max(0, stats.shield)

        self.shield_display += (current_shield - self.shield_display) * 0.15

        bar_width = 250
        bar_height = 20
        shadow = 4

        shield_ratio = max(0, min(1, current_shield / max_shield))

        # sombra
        self._draw_rounded_rect(surface, BLACK + (120,), (x + shadow, y + shadow, bar_width, bar_height), 10)

        # fondo
        self._draw_rounded_rect(surface, DARK_BG, (x, y, bar_width, bar_height), 10)

        # borde
        pygame.draw.rect(surface, BORDER_GREY + (200,), (x, y, bar_width, bar_height), width=2, border_radius=10)

        # barra escudo
        if shield_ratio > 0:
            sr = pygame.Rect(x + 2, y + 2, int((bar_width - 4) * shield_ratio), bar_height - 4)
            self._draw_gradient_bar(surface, sr, SHIELD_BLUE_DARK, SHIELD_BLUE_LIGHT)

            # efecto pulse
            if shield_ratio > 0.7:
                alpha = int(pulse * 60)
                pulse_surf = pygame.Surface((sr.width, sr.height), pygame.SRCALPHA)
                pulse_surf.fill(SHIELD_PULSE + (alpha,))
                surface.blit(pulse_surf, sr.topleft)

        # texto corregido
        txt_s = f"SHIELD {int(current_shield)}/{int(max_shield)}"
        text_s = self.font.render(txt_s, True, SHIELD_LABEL)
        surface.blit(text_s, (x + bar_width + 12, y))


# ============================================================
# AMMO HUD (SIN CAMBIOS)
# ============================================================
class AmmoHUD:
    def __init__(self, font):
        self.font = font

    def draw(self, surface, player):
        sw, sh = surface.get_size()
        ammo_x, ammo_y = 30, sh - 60
        circle_center = (ammo_x + 24, ammo_y + 6)
        circle_radius = 18

        pygame.draw.circle(surface, BLACK + (100,), (circle_center[0] + 2, circle_center[1] + 2), circle_radius)
        pygame.draw.circle(surface, DARK_GREY, circle_center, circle_radius, 3)
        pygame.draw.circle(surface, LIGHT_GREY, circle_center, circle_radius - 1, 1)

        if getattr(player, "weapon", None) and player.weapon.is_reloading:
            progress = max(0.0, min(1.0, player.weapon.reload_timer / max(0.0001, player.weapon.reload_time)))
            start_angle = -math.pi / 2
            end_angle = start_angle + progress * 2 * math.pi
            rect = pygame.Rect(circle_center[0] - circle_radius, circle_center[1] - circle_radius,
                               circle_radius * 2, circle_radius * 2)
            pygame.draw.arc(surface, STAT_AMMO, rect, start_angle, end_angle, 7)
        else:
            pygame.draw.circle(surface, STAT_HP, circle_center, 7)
            pygame.draw.circle(surface, STAT_SHIELD, circle_center, 5)
            pygame.draw.circle(surface, GREEN, circle_center, 3)

        if getattr(player, "weapon", None):
            ammo_panel = pygame.Surface((320, 40), pygame.SRCALPHA)
            ammo_panel.fill(DARK_PANEL + (200,))
            pygame.draw.rect(ammo_panel, BORDER_GREY + (150,), (0, 0, 320, 40), width=2, border_radius=8)
            surface.blit(ammo_panel, (ammo_x + 55, ammo_y - 12))

            ammo_text = self.font.render(
                f"AMMO: {player.weapon.current_ammo}/{player.weapon.max_ammo} | {player.weapon.reserve_ammo}",
                True, WHITE
            )
            surface.blit(ammo_text, (ammo_x + 60, ammo_y - 4))

            if player.weapon.is_reloading:
                reload_text = self.font.render("RELOADING...", True, STAT_AMMO)
                surface.blit(reload_text, (ammo_x + 110, ammo_y - 30))


# ============================================================
# INFO PANEL (Score, Wave, Zombies Left) — SIN CAMBIOS
# ============================================================
class InfoPanelHUD:
    def __init__(self, font):
        self.font = font
        self.pulse_timer = 0

    def draw(self, surface, player, wave_manager):
        self.pulse_timer += 0.05
        pulse = abs(math.sin(self.pulse_timer)) * 0.3 + 0.7
        info_y_start = 100

        score_text = self.font.render(f"SCORE: {player.score}", True, YELLOW)
        surface.blit(score_text, (30, info_y_start))

        wave_color = (255, int(240 * pulse), 100)
        wave_text = self.font.render(f"WAVE: {wave_manager.current_wave}", True, wave_color)
        surface.blit(wave_text, (30, info_y_start + 40))

        alive = sum(1 for z in wave_manager.game.zombies if not getattr(z, "dead", False))
        total_left = wave_manager.enemies_to_spawn + alive

        zombie_text = self.font.render(f"ZOMBIES LEFT: {total_left}", True, RED)
        surface.blit(zombie_text, (30, info_y_start + 80))


# ============================================================
# ENEMY HEALTH HUD — SIN CAMBIOS
# ============================================================
class EnemyHealthHUD:
    def __init__(self, font):
        self.font = font

    def draw(self, surface, wave_manager):
        camera = getattr(wave_manager.game, "camera", None)
        screen_rect = surface.get_rect()

        for z in wave_manager.game.zombies:
            if getattr(z, "dead", False):
                continue
            if not hasattr(z, "hp") or not hasattr(z, "rect"):
                continue

            try:
                z_screen_rect = camera.apply(z.rect) if camera else z.rect
            except Exception:
                z_screen_rect = z.rect

            if not screen_rect.colliderect(z_screen_rect):
                continue

            zx, zy = z_screen_rect.centerx, z_screen_rect.bottom + 4
            max_z_hp = ZombieStats.TYPE_STATS.get(z.type, {}).get("hp", getattr(z, "hp", 1))
            hp_ratio = max(0.0, min(1.0, (z.hp / max_z_hp) if max_z_hp else 0.0))
            bar_w = max(24, z_screen_rect.width // 2)
            bar_h = 6

            shadow_rect = pygame.Rect(zx - bar_w // 2 + 1, zy + 1, bar_w, bar_h)
            pygame.draw.rect(surface, BLACK + (120,), shadow_rect, border_radius=3)

            bg_rect = pygame.Rect(zx - bar_w // 2 - 1, zy - 1, bar_w + 2, bar_h + 2)
            pygame.draw.rect(surface, DARK_BG, bg_rect, border_radius=3)

            pygame.draw.rect(surface, BORDER_GREY, (zx - bar_w // 2, zy, bar_w, bar_h), border_radius=2)

            if hp_ratio > 0:
                filled_w = int(bar_w * hp_ratio)
                hp_rect = pygame.Rect(zx - bar_w // 2, zy, filled_w, bar_h)
                color = RED if hp_ratio < 0.3 else YELLOW if hp_ratio < 0.6 else GREEN
                pygame.draw.rect(surface, color, hp_rect, border_radius=2)

                highlight_rect = pygame.Rect(zx - bar_w // 2, zy, filled_w, bar_h // 2)
                highlight_surf = pygame.Surface((filled_w, bar_h // 2), pygame.SRCALPHA)
                highlight_surf.fill((255, 255, 255, 50))
                surface.blit(highlight_surf, highlight_rect.topleft)

            level_text = f"Lv {getattr(z, 'level', 1)}"
            rarity_color_map = {
                "common": WHITE,
                "uncommon": GREEN,
                "rare": BLUE,
                "epic": (200, 80, 255),
                "legendary": YELLOW
            }
            txt_color = rarity_color_map.get(getattr(z, 'rarity', 'common'), WHITE)
            txt_surf = self.font.render(level_text, True, txt_color)
            txt_rect = txt_surf.get_rect(center=(z_screen_rect.centerx, z_screen_rect.top - 10))

            bg_padding = 4
            level_bg = pygame.Surface((txt_rect.width + bg_padding * 2, txt_rect.height + bg_padding),
                                      pygame.SRCALPHA)
            level_bg.fill(BLACK + (160,))
            pygame.draw.rect(
                level_bg,
                txt_color,
                (0, 0, txt_rect.width + bg_padding * 2, txt_rect.height + bg_padding),
                width=1,
                border_radius=4
            )

            bg_rect = level_bg.get_rect(center=txt_rect.center)
            surface.blit(level_bg, bg_rect)

            shadow_surf = self.font.render(level_text, True, BLACK)
            shadow_rect = shadow_surf.get_rect(center=(txt_rect.centerx + 1, txt_rect.centery + 1))
            surface.blit(shadow_surf, shadow_rect)
            surface.blit(txt_surf, txt_rect)


# ============================================================
# MINIMAP
# ============================================================
class MiniMapHUD:
    def __init__(self):
        self.minimap = None

    def ensure_minimap(self, wave_manager):
        if self.minimap is None:
            game = getattr(wave_manager, "game", None)
            if game:
                self.minimap = MiniMap(
                    game=game, width=180, height=180, margin=8,
                    position="topright", update_interval_ms=100
                )

    def draw(self, surface, wave_manager):
        self.ensure_minimap(wave_manager)
        if self.minimap:
            self.minimap.draw(surface)


# ============================================================
# HUD PRINCIPAL
# ============================================================
class HUD:
    def __init__(self, font):
        self.health_bar = HealthBarHUD(font)
        self.shield_bar = ShieldBarHUD(font)
        self.ammo_hud = AmmoHUD(font)
        self.info_panel = InfoPanelHUD(font)
        self.enemy_health = EnemyHealthHUD(font)
        self.minimap_hud = MiniMapHUD()

    def draw(self, surface, player, wave_manager):
        self.health_bar.draw(surface, player)
        self.shield_bar.draw(surface, player)
        self.ammo_hud.draw(surface, player)
        self.info_panel.draw(surface, player, wave_manager)
        self.enemy_health.draw(surface, wave_manager)
        self.minimap_hud.draw(surface, wave_manager)
