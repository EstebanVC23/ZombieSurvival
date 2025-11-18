import pygame
import math
from utils.helpers import load_image_safe
from colors import (
    BLACK, WHITE,
    DARK_BG, DARK_PANEL, LIGHT_GREY, DARK_GREY,
    HP_RED_DARK, HP_RED_LIGHT, HP_LABEL,
    SHIELD_BLUE_DARK, SHIELD_BLUE_LIGHT, SHIELD_LABEL, SHIELD_PULSE,
    STAT_HP, STAT_ARMOR, STAT_SHIELD, STAT_SPEED, STAT_DAMAGE, STAT_RPM, STAT_AMMO, STAT_RESERVE,
    BORDER_RED, BORDER_RED_INNER, BORDER_GREY, BORDER_HIGHLIGHT
)

class UIManager:
    """Controla la tarjeta HUD extendida del jugador con barras, stats y efectos."""

    CARD_SIZE = (780, 420)
    PLAYER_PANEL_SIZE = (240, CARD_SIZE[1] - 40)
    BAR_SIZE = (260, 20)

    def __init__(self, player):
        self.player = player
        self.visible = False
        self.pulse_timer = 0

        self.card_bg = self._load_card_bg()
        self.player_image = self._load_player_image()

    # -------------------- CARGA DE RECURSOS --------------------
    def _load_card_bg(self):
        bg = load_image_safe("ui/card_bg.png")
        if bg:
            return pygame.transform.scale(bg, self.CARD_SIZE)
        else:
            print("[WARN] Fondo de card no encontrado, usando superficie básica.")
            surf = pygame.Surface(self.CARD_SIZE, pygame.SRCALPHA)
            surf.fill((*DARK_BG, 230))
            return surf

    def _load_player_image(self):
        img = load_image_safe("player/player_static.png")
        if img:
            img = pygame.transform.smoothscale(img, (180, 320))
            return self._clear_white_background(img)
        else:
            print("[WARN] Imagen del jugador no encontrada en UIManager.")
            surf = pygame.Surface((120, 240), pygame.SRCALPHA)
            surf.fill((255, 0, 0, 120))
            return surf

    def _clear_white_background(self, img):
        """Quita los pixeles blancos claros de la imagen del jugador."""
        img.lock()
        for x in range(img.get_width()):
            for y in range(img.get_height()):
                r, g, b, a = img.get_at((x, y))
                if (r + g + b) / 3 > 200 and a > 0:
                    img.set_at((x, y), (0, 0, 0, 0))
        img.unlock()
        return img

    # -------------------- INTERACCIÓN --------------------
    def toggle(self):
        self.visible = not self.visible

    # -------------------- UTILIDADES --------------------
    def _draw_gradient_bar(self, surface, rect, color_start, color_end, ratio):
        if ratio <= 0:
            return
        filled_width = max(1, int(rect.width * ratio))
        for i in range(filled_width):
            progress = i / filled_width
            r = min(max(0, int(color_start[0] + (color_end[0] - color_start[0]) * progress)), 255)
            g = min(max(0, int(color_start[1] + (color_end[1] - color_start[1]) * progress)), 255)
            b = min(max(0, int(color_start[2] + (color_end[2] - color_start[2]) * progress)), 255)
            pygame.draw.line(surface, (r, g, b), (rect.x + i, rect.y), (rect.x + i, rect.y + rect.height))

    # -------------------- DIBUJOS --------------------
    def draw_player_card(self, screen, font, screen_width, screen_height):
        if not self.visible or not self.player:
            return
        self.pulse_timer += 0.05
        pulse = abs(math.sin(self.pulse_timer)) * 0.2 + 0.8

        card_x, card_y = self._draw_overlay(screen, screen_width, screen_height)
        self._draw_card_background(screen, card_x, card_y)
        self._draw_card_borders(screen, card_x, card_y)
        player_panel_rect = self._draw_player_panel(screen, card_x, card_y)
        self._draw_player_image(screen, player_panel_rect)
        line_x = self._draw_divider(screen, player_panel_rect, card_y)
        stats_x, stats_y = line_x + 30, card_y + 50
        stats = self._get_player_stats()
        self._draw_stats(screen, font, stats, stats_x, stats_y)
        self._draw_bars(screen, font, stats_x, stats_y + len(stats) * 36 + 20, pulse)

    def _draw_overlay(self, screen, width, height):
        overlay = pygame.Surface((width, height), pygame.SRCALPHA)
        overlay.fill((*BLACK, 160))
        screen.blit(overlay, (0, 0))
        card_x = (width - self.CARD_SIZE[0]) // 2
        card_y = (height - self.CARD_SIZE[1]) // 2
        return card_x, card_y

    def _draw_card_background(self, screen, x, y):
        card_surf = pygame.Surface(self.CARD_SIZE, pygame.SRCALPHA)
        for i in range(self.CARD_SIZE[1]):
            brightness = min(255, max(0, DARK_BG[0] + int((i / self.CARD_SIZE[1]) * 15)))
            pygame.draw.line(card_surf, (brightness, brightness, min(255, brightness + 5), 240),
                             (0, i), (self.CARD_SIZE[0], i))
        screen.blit(card_surf, (x, y))
        # Sombra
        shadow_surf = pygame.Surface((self.CARD_SIZE[0] + 10, self.CARD_SIZE[1] + 10), pygame.SRCALPHA)
        shadow_surf.fill((*BLACK, 100))
        screen.blit(shadow_surf, (x + 5, y + 5))

    def _draw_card_borders(self, screen, x, y):
        pygame.draw.rect(screen, BORDER_RED, (x, y, *self.CARD_SIZE), width=3, border_radius=15)
        pygame.draw.rect(screen, BORDER_RED_INNER, (x + 4, y + 4, self.CARD_SIZE[0] - 8, self.CARD_SIZE[1] - 8),
                         width=2, border_radius=13)

    def _draw_player_panel(self, screen, card_x, card_y):
        panel_rect = pygame.Rect(card_x + 20, card_y + 20, *self.PLAYER_PANEL_SIZE)
        pygame.draw.rect(screen, (*DARK_PANEL, 200), panel_rect, border_radius=12)
        pygame.draw.rect(screen, BORDER_GREY, panel_rect, width=2, border_radius=12)
        return panel_rect

    def _draw_player_image(self, screen, panel_rect):
        player_rect = self.player_image.get_rect(center=panel_rect.center)
        screen.blit(self.player_image, player_rect)

    def _draw_divider(self, screen, panel_rect, card_y):
        line_x = panel_rect.right + 20
        pygame.draw.line(screen, BORDER_RED, (line_x, card_y + 50), (line_x, card_y + self.CARD_SIZE[1] - 50), 3)
        pygame.draw.line(screen, (*BORDER_HIGHLIGHT, 150),
                         (line_x + 1, card_y + 50), (line_x + 1, card_y + self.CARD_SIZE[1] - 50), 1)
        return line_x

    def _get_player_stats(self):
        hp = int(getattr(self.player, "health", 0))
        max_hp = int(getattr(self.player, "max_health", 100))
        shield = int(getattr(self.player, "shield", 0))
        max_shield = int(getattr(self.player, "max_shield", 100))
        speed = int(getattr(self.player, "speed", 0))
        damage = getattr(self.player.weapon, "damage", 0)
        rpm = getattr(self.player.weapon, "rpm", getattr(self.player.weapon, "cooldown", 0))
        current_ammo = getattr(self.player.weapon, "current_ammo", 0)
        max_ammo = getattr(self.player.weapon, "max_ammo", 0)
        reserve = getattr(self.player.weapon, "reserve_ammo", getattr(self.player.weapon, "reserve", 0))
        armor = int(getattr(self.player, "armor", 0))

        return [
            ("Vida", f"{hp} / {max_hp}", STAT_HP),
            ("Armadura", f"{armor}", STAT_ARMOR),
            ("Escudo", f"{shield} / {max_shield}", STAT_SHIELD),
            ("Velocidad", f"{speed}", STAT_SPEED),
            ("Daño", f"{damage}", STAT_DAMAGE),
            ("Cadencia (RPM)", f"{rpm}", STAT_RPM),
            ("Cargador", f"{current_ammo} / {max_ammo}", STAT_AMMO),
            ("Balas (reserva)", f"{reserve}", STAT_RESERVE)
        ]

    def _draw_stats(self, screen, font, stats, x, y):
        spacing = 36
        for i, (label, value, color) in enumerate(stats):
            y_pos = y + i * spacing
            pygame.draw.circle(screen, color, (x - 12, y_pos + 8), 5)
            pygame.draw.circle(screen, (*WHITE, 100), (x - 12, y_pos + 8), 5, 1)

            label_text = font.render(label + ":", True, LIGHT_GREY)
            screen.blit(font.render(label + ":", True, BLACK), (x + 2, y_pos + 2))
            screen.blit(label_text, (x, y_pos))

            value_text = font.render(value, True, color)
            value_x = x + label_text.get_width() + 10
            screen.blit(font.render(value, True, BLACK), (value_x + 2, y_pos + 2))
            screen.blit(value_text, (value_x, y_pos))

    def _draw_bars(self, screen, font, x, y, pulse):
        bar_width, bar_height = self.BAR_SIZE
        # VIDA
        hp = int(getattr(self.player, "health", 0))
        max_hp = int(getattr(self.player, "max_health", 100))
        hp_ratio = max(0.0, min(1.0, hp / max(1, max_hp)))
        hp_rect = pygame.Rect(x, y, bar_width, bar_height)
        pygame.draw.rect(screen, DARK_PANEL, hp_rect, border_radius=10)
        pygame.draw.rect(screen, DARK_GREY, hp_rect, width=2, border_radius=10)
        if hp_ratio > 0:
            filled = pygame.Rect(x + 2, y + 2, int((bar_width - 4) * hp_ratio), bar_height - 4)
            self._draw_gradient_bar(screen, filled, HP_RED_DARK, HP_RED_LIGHT, 1.0)
            highlight = pygame.Surface((filled.width, bar_height // 3), pygame.SRCALPHA)
            highlight.fill((*WHITE, 40))
            screen.blit(highlight, (filled.x, filled.y))
        screen.blit(font.render("VIDA", True, HP_LABEL), (x + bar_width + 10, y))

        # ESCUDO
        shield = int(getattr(self.player, "shield", 0))
        max_shield = int(getattr(self.player, "max_shield", 100))
        shield_ratio = max(0.0, min(1.0, shield / max(1, max_shield)))
        shield_rect = pygame.Rect(x, y + 30, bar_width, bar_height)
        pygame.draw.rect(screen, DARK_PANEL, shield_rect, border_radius=10)
        pygame.draw.rect(screen, DARK_GREY, shield_rect, width=2, border_radius=10)
        if shield_ratio > 0:
            filled = pygame.Rect(x + 2, y + 32, int((bar_width - 4) * shield_ratio), bar_height - 4)
            self._draw_gradient_bar(screen, filled, SHIELD_BLUE_DARK, SHIELD_BLUE_LIGHT, 1.0)
            highlight = pygame.Surface((filled.width, bar_height // 3), pygame.SRCALPHA)
            highlight.fill((*WHITE, 50))
            screen.blit(highlight, (filled.x, filled.y))
            if shield_ratio > 0.7:
                pulse_alpha = int(pulse * 60)
                pulse_surf = pygame.Surface((filled.width, filled.height), pygame.SRCALPHA)
                pulse_surf.fill((*SHIELD_PULSE, pulse_alpha))
                screen.blit(pulse_surf, (filled.x, filled.y))
        screen.blit(font.render("ESCUDO", True, SHIELD_LABEL), (x + bar_width + 10, y + 30))
