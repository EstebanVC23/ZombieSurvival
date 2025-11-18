import pygame
import math
from ui.map import MiniMap
from entities.zombie import ZombieStats
from settings import *
from colors import *  # Importamos todas las constantes de color

# ========================= Subclases del HUD =========================
class HealthBarHUD:
    """Se encarga de dibujar las barras de HP y Shield."""

    def __init__(self, font):
        self.font = font
        self.hp_display = 100
        self.shield_display = 0
        self.pulse_timer = 0

    def _draw_rounded_rect(self, surface, color, rect, radius=8):
        pygame.draw.rect(surface, color, rect, border_radius=radius)

    def _draw_gradient_bar(self, surface, rect, color_start, color_end, ratio):
        if ratio <= 0:
            return
        filled_width = int(rect.width * ratio)
        if filled_width <= 0:
            return
        temp_surf = pygame.Surface((filled_width, rect.height), pygame.SRCALPHA)
        for i in range(filled_width):
            progress = i / max(1, filled_width)
            r = int(color_start[0] + (color_end[0] - color_start[0]) * progress)
            g = int(color_start[1] + (color_end[1] - color_start[1]) * progress)
            b = int(color_start[2] + (color_end[2] - color_start[2]) * progress)
            temp_surf.set_at((i, 0), (r, g, b))
            pygame.draw.line(temp_surf, (r, g, b), (i, 0), (i, rect.height))
        surface.blit(temp_surf, rect.topleft)

    def draw(self, surface, player):
        self.pulse_timer += 0.05
        pulse = abs(math.sin(self.pulse_timer)) * 0.3 + 0.7

        self.hp_display += (player.health - self.hp_display) * 0.15
        self.shield_display += (player.shield - self.shield_display) * 0.15

        x, y, bar_width, bar_height = 30, 30, 250, 18
        shadow_offset = 4

        # ==== HP BAR ====
        max_hp = getattr(player, "max_health", 100)
        hp_ratio = max(0, player.health / max_hp)

        # Sombra
        self._draw_rounded_rect(surface, BLACK + (100,), (x+shadow_offset, y+shadow_offset, bar_width, bar_height), 10)
        # Fondo y borde
        self._draw_rounded_rect(surface, DARK_GREY, (x-2, y-2, bar_width+4, bar_height+4), 10)
        self._draw_rounded_rect(surface, DARK_BG, (x, y, bar_width, bar_height), 8)
        pygame.draw.rect(surface, BORDER_GREY + (150,), (x+1, y+1, bar_width-2, bar_height-2), width=1, border_radius=8)

        # Barra de HP
        if hp_ratio > 0:
            hp_rect = pygame.Rect(x+2, y+2, int((bar_width-4)*hp_ratio), bar_height-4)
            if hp_ratio < 0.3:
                color_start, color_end = HP_RED_DARK, HP_RED_LIGHT
            elif hp_ratio < 0.6:
                color_start, color_end = (255, 140, 30), (255, 180, 50)
            else:
                color_start, color_end = GREEN, (60, 220, 90)
            self._draw_gradient_bar(surface, hp_rect, color_start, color_end, 1.0)
            highlight = pygame.Surface((hp_rect.width, hp_rect.height//3), pygame.SRCALPHA)
            highlight.fill((255, 255, 255, 40))
            surface.blit(highlight, (hp_rect.x, hp_rect.y))

        # Texto HP
        hp_text = self.font.render(f"HP {int(self.hp_display)}/{int(max_hp)}", True, HP_LABEL)
        shadow = self.font.render(f"HP {int(self.hp_display)}/{int(max_hp)}", True, BLACK)
        surface.blit(shadow, (x + 262, y))
        surface.blit(hp_text, (x + 260, y-2))

        # ==== SHIELD BAR ====
        max_shield = getattr(player, "max_shield", 0)
        if max_shield > 0:
            shield_ratio = max(0, player.shield / max_shield)
            shield_y = y + 32
            self._draw_rounded_rect(surface, BLACK + (100,), (x+shadow_offset, shield_y+shadow_offset, bar_width, bar_height), 10)
            self._draw_rounded_rect(surface, DARK_GREY, (x-2, shield_y-2, bar_width+4, bar_height+4), 10)
            self._draw_rounded_rect(surface, DARK_BG, (x, shield_y, bar_width, bar_height), 8)
            pygame.draw.rect(surface, BORDER_GREY + (150,), (x+1, shield_y+1, bar_width-2, bar_height-2), width=1, border_radius=8)

            if shield_ratio > 0:
                shield_rect = pygame.Rect(x+2, shield_y+2, int((bar_width-4)*shield_ratio), bar_height-4)
                self._draw_gradient_bar(surface, shield_rect, SHIELD_BLUE_DARK, SHIELD_BLUE_LIGHT, 1.0)
                highlight = pygame.Surface((shield_rect.width, shield_rect.height//3), pygame.SRCALPHA)
                highlight.fill((255, 255, 255, 50))
                surface.blit(highlight, (shield_rect.x, shield_rect.y))
                if shield_ratio > 0.7:
                    pulse_alpha = int(pulse * 60)
                    pulse_surf = pygame.Surface((shield_rect.width, shield_rect.height), pygame.SRCALPHA)
                    pulse_surf.fill(SHIELD_PULSE + (pulse_alpha,))
                    surface.blit(pulse_surf, (shield_rect.x, shield_rect.y))

            shield_text = self.font.render(f"SHIELD {int(self.shield_display)}/{int(max_shield)}", True, SHIELD_LABEL)
            shadow = self.font.render(f"SHIELD {int(self.shield_display)}/{int(max_shield)}", True, BLACK)
            surface.blit(shadow, (x + 262, shield_y+2))
            surface.blit(shield_text, (x + 260, shield_y))


class AmmoHUD:
    """Muestra munición y recarga."""

    def __init__(self, font):
        self.font = font

    def draw(self, surface, player):
        sw, sh = surface.get_size()
        ammo_x, ammo_y = 30, sh-60
        circle_center = (ammo_x+24, ammo_y+6)
        circle_radius = 18

        # Sombra del círculo
        pygame.draw.circle(surface, BLACK + (100,), (circle_center[0]+2, circle_center[1]+2), circle_radius)
        pygame.draw.circle(surface, DARK_GREY, circle_center, circle_radius, 3)
        pygame.draw.circle(surface, LIGHT_GREY, circle_center, circle_radius-1, 1)

        if getattr(player,"weapon",None) and player.weapon.is_reloading:
            progress = max(0.0, min(1.0, player.weapon.reload_timer/max(0.0001, player.weapon.reload_time)))
            start_angle = -math.pi/2
            end_angle = start_angle + progress*2*math.pi
            rect = pygame.Rect(circle_center[0]-circle_radius, circle_center[1]-circle_radius, circle_radius*2, circle_radius*2)
            pygame.draw.arc(surface, STAT_AMMO, rect, start_angle, end_angle, 7)
        else:
            pygame.draw.circle(surface, STAT_HP, circle_center, 7)
            pygame.draw.circle(surface, STAT_SHIELD, circle_center, 5)
            pygame.draw.circle(surface, GREEN, circle_center, 3)

        if getattr(player,"weapon",None):
            ammo_panel = pygame.Surface((320, 40), pygame.SRCALPHA)
            ammo_panel.fill(DARK_PANEL + (200,))
            pygame.draw.rect(ammo_panel, BORDER_GREY + (150,), (0, 0, 320, 40), width=2, border_radius=8)
            surface.blit(ammo_panel, (ammo_x+55, ammo_y-12))
            ammo_text = self.font.render(f"AMMO: {player.weapon.current_ammo}/{player.weapon.max_ammo} | {player.weapon.reserve_ammo}", True, WHITE)
            surface.blit(ammo_text, (ammo_x+60, ammo_y-4))
            if player.weapon.is_reloading:
                reload_text = self.font.render("RELOADING...", True, STAT_AMMO)
                surface.blit(reload_text, (ammo_x+110, ammo_y-30))


class InfoPanelHUD:
    """Score, Wave, Zombies left."""

    def __init__(self, font):
        self.font = font
        self.pulse_timer = 0

    def draw(self, surface, player, wave_manager):
        self.pulse_timer += 0.05
        pulse = abs(math.sin(self.pulse_timer)) * 0.3 + 0.7
        info_y_start = 100

        # Score
        score_text = self.font.render(f"SCORE: {player.score}", True, YELLOW)
        surface.blit(score_text, (30, info_y_start))

        # Wave
        wave_color = (255, int(240 * pulse), 100)
        wave_text = self.font.render(f"WAVE: {wave_manager.current_wave}", True, wave_color)
        surface.blit(wave_text, (30, info_y_start+40))

        # Zombies left
        alive = sum(1 for z in wave_manager.game.zombies if not getattr(z, "dead", False))
        total_left = wave_manager.enemies_to_spawn + alive
        zombie_text = self.font.render(f"ZOMBIES LEFT: {total_left}", True, RED)
        surface.blit(zombie_text, (30, info_y_start+80))


class EnemyHealthHUD:
    """Barras de vida y nivel de zombies."""

    def __init__(self, font):
        self.font = font

    def draw(self, surface, wave_manager):
        camera = getattr(wave_manager.game,"camera",None)
        screen_rect = surface.get_rect()
        for z in wave_manager.game.zombies:
            if getattr(z,"dead",False): 
                continue
            if not hasattr(z,"hp") or not hasattr(z,"rect"): 
                continue
            try: 
                z_screen_rect = camera.apply(z.rect) if camera else z.rect
            except Exception: 
                z_screen_rect = z.rect
            if not screen_rect.colliderect(z_screen_rect): 
                continue

            # Barra de vida
            zx, zy = z_screen_rect.centerx, z_screen_rect.bottom + 4
            max_z_hp = ZombieStats.TYPE_STATS.get(z.type, {}).get("hp", getattr(z, "hp", 1))
            hp_ratio = max(0.0, min(1.0, (z.hp/max_z_hp) if max_z_hp else 0.0))
            bar_w = max(24, z_screen_rect.width//2)
            bar_h = 6

            shadow_rect = pygame.Rect(zx-bar_w//2+1, zy+1, bar_w, bar_h)
            pygame.draw.rect(surface, BLACK + (120,), shadow_rect, border_radius=3)
            bg_rect = pygame.Rect(zx-bar_w//2-1, zy-1, bar_w+2, bar_h+2)
            pygame.draw.rect(surface, DARK_BG, bg_rect, border_radius=3)
            pygame.draw.rect(surface, BORDER_GREY, (zx-bar_w//2, zy, bar_w, bar_h), border_radius=2)

            if hp_ratio > 0:
                filled_w = int(bar_w * hp_ratio)
                hp_rect = pygame.Rect(zx-bar_w//2, zy, filled_w, bar_h)
                color = RED if hp_ratio < 0.3 else YELLOW if hp_ratio < 0.6 else GREEN
                pygame.draw.rect(surface, color, hp_rect, border_radius=2)
                highlight_rect = pygame.Rect(zx-bar_w//2, zy, filled_w, bar_h//2)
                highlight_surf = pygame.Surface((filled_w, bar_h//2), pygame.SRCALPHA)
                highlight_surf.fill((255, 255, 255, 50))
                surface.blit(highlight_surf, highlight_rect.topleft)

            # Nivel del zombie
            level_text = f"Lv {getattr(z,'level',1)}"
            rarity_color_map = {
                "common": WHITE,
                "uncommon": GREEN,
                "rare": BLUE,
                "epic": (200, 80, 255),
                "legendary": YELLOW
            }
            txt_color = rarity_color_map.get(getattr(z,'rarity','common'), WHITE)
            txt_surf = self.font.render(level_text, True, txt_color)
            txt_rect = txt_surf.get_rect(center=(z_screen_rect.centerx, z_screen_rect.top - 10))
            bg_padding = 4
            level_bg = pygame.Surface((txt_rect.width + bg_padding*2, txt_rect.height + bg_padding), pygame.SRCALPHA)
            level_bg.fill(BLACK + (160,))
            pygame.draw.rect(level_bg, txt_color, 
                           (0, 0, txt_rect.width + bg_padding*2, txt_rect.height + bg_padding), 
                           width=1, border_radius=4)
            bg_rect = level_bg.get_rect(center=txt_rect.center)
            surface.blit(level_bg, bg_rect)
            shadow_surf = self.font.render(level_text, True, BLACK)
            shadow_rect = shadow_surf.get_rect(center=(txt_rect.centerx+1, txt_rect.centery+1))
            surface.blit(shadow_surf, shadow_rect)
            surface.blit(txt_surf, txt_rect)


class MiniMapHUD:
    """Encargado del minimapa."""

    def __init__(self):
        self.minimap = None

    def ensure_minimap(self, wave_manager):
        if self.minimap is None:
            game = getattr(wave_manager, "game", None)
            if game:
                self.minimap = MiniMap(game=game, width=180, height=180, margin=8,
                                       position="topright", update_interval_ms=100)

    def draw(self, surface, wave_manager):
        self.ensure_minimap(wave_manager)
        if self.minimap:
            self.minimap.draw(surface)


# ========================= HUD Principal =========================
class HUD:
    """Coordinador del HUD, delega a subcomponentes."""

    def __init__(self, font):
        self.health_bar = HealthBarHUD(font)
        self.ammo_hud = AmmoHUD(font)
        self.info_panel = InfoPanelHUD(font)
        self.enemy_health = EnemyHealthHUD(font)
        self.minimap_hud = MiniMapHUD()

    def draw(self, surface, player, wave_manager):
        self.health_bar.draw(surface, player)
        self.ammo_hud.draw(surface, player)
        self.info_panel.draw(surface, player, wave_manager)
        self.enemy_health.draw(surface, wave_manager)
        self.minimap_hud.draw(surface, wave_manager)
