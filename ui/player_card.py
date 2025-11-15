import pygame
from utils.helpers import load_image_safe

class UIManager:
    """Controla las tarjetas de estadísticas del jugador (HUD extendido con imagen y barras)."""

    def __init__(self, player):
        self.player = player
        self.visible = False  # Visibilidad de la tarjeta

        # Cargar fondo de tarjeta
        self.card_bg = load_image_safe("ui/card_bg.png")
        if self.card_bg:
            self.card_bg = pygame.transform.scale(self.card_bg, (780, 420))
        else:
            print("[WARN] Fondo de card no encontrado, usando superficie básica.")
            self.card_bg = pygame.Surface((780, 420), pygame.SRCALPHA)
            self.card_bg.fill((25, 25, 25, 230))

        # Cargar imagen del jugador
        self.player_image = load_image_safe("player/player_static.png")
        if self.player_image:
            self.player_image = pygame.transform.smoothscale(self.player_image, (180, 320))
            self._clear_white_background()
        else:
            print("[WARN] Imagen del jugador no encontrada en UIManager.")
            self.player_image = pygame.Surface((120, 240), pygame.SRCALPHA)
            self.player_image.fill((255, 0, 0, 120))

    def _clear_white_background(self):
        """Quita los pixeles blancos claros de la imagen del jugador."""
        img = self.player_image
        img.lock()
        for x in range(img.get_width()):
            for y in range(img.get_height()):
                r, g, b, a = img.get_at((x, y))
                if (r + g + b) / 3 > 200 and a > 0:
                    img.set_at((x, y), (0, 0, 0, 0))
        img.unlock()
        self.player_image = img

    # ==================================================
    # Mostrar / ocultar tarjeta
    # ==================================================
    def toggle(self):
        self.visible = not self.visible

    # ==================================================
    # Dibuja un rectángulo con borde redondeado y doble contorno
    # ==================================================
    def draw_rounded_rect_with_border(self, surface, rect, color_bg, color_border, radius, border_thickness=3, separation=2):
        x, y, w, h = rect
        pygame.draw.rect(surface, color_bg, rect, border_radius=radius)
        pygame.draw.rect(surface, color_border, rect, border_radius=radius, width=border_thickness)
        inner_rect = pygame.Rect(x + separation, y + separation, w - 2 * separation, h - 2 * separation)
        pygame.draw.rect(surface, color_border, inner_rect, border_radius=radius - 2, width=border_thickness)

    # ==================================================
    # Dibuja la tarjeta del jugador
    # ==================================================
    def draw_player_card(self, screen, font, screen_width, screen_height):
        if not self.visible or not self.player:
            return

        # Fondo translúcido
        overlay = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 140))
        screen.blit(overlay, (0, 0))

        # Fondo de la tarjeta
        card_rect = self.card_bg.get_rect(center=(screen_width // 2, screen_height // 2))
        self.draw_rounded_rect_with_border(screen, card_rect, (20, 20, 20, 220), (200, 30, 30), radius=30, border_thickness=3)

        # Imagen del jugador
        player_rect = self.player_image.get_rect(midleft=(card_rect.left + 120, card_rect.centery))
        screen.blit(self.player_image, player_rect)

        # Línea divisoria
        line_x = player_rect.right + 25
        pygame.draw.line(screen, (200, 30, 30), (line_x, card_rect.top + 40), (line_x, card_rect.bottom - 40), 3)

        # Texto y estadísticas
        stats_x = line_x + 35
        stats_y = card_rect.top + 40
        spacing = 38

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

        stats = [
            ("Vida", f"{hp} / {max_hp}"),
            ("Armadura", f"{armor}"),
            ("Escudo", f"{shield} / {max_shield}"),
            ("Velocidad", f"{speed}"),
            ("Daño", f"{damage}"),
            ("Cadencia (RPM)", f"{rpm}"),
            ("Cargador", f"{current_ammo} / {max_ammo}"),
            ("Balas (reserva)", f"{reserve}")
        ]

        for i, (label, value) in enumerate(stats):
            text = font.render(f"{label}: {value}", True, (255, 255, 255))
            screen.blit(text, (stats_x, stats_y + i * spacing))

        # Barras de vida y escudo
        bar_width = 260
        bar_height = 18
        bar_y_offset = stats_y + spacing * len(stats) + 15
        pygame.draw.rect(screen, (60, 60, 60), (stats_x, bar_y_offset, bar_width, bar_height), border_radius=10)
        pygame.draw.rect(screen, (60, 60, 60), (stats_x, bar_y_offset + 25, bar_width, bar_height), border_radius=10)

        health_ratio = hp / max(1, max_hp)
        pygame.draw.rect(screen, (255, 60, 60), (stats_x, bar_y_offset, int(bar_width * health_ratio), bar_height), border_radius=10)

        shield_ratio = shield / max(1, max_shield)
        pygame.draw.rect(screen, (100, 180, 255), (stats_x, bar_y_offset + 25, int(bar_width * shield_ratio), bar_height), border_radius=10)

        hp_text = font.render("VIDA", True, (255, 255, 255))
        shield_text = font.render("ESCUDO", True, (180, 220, 255))
        screen.blit(hp_text, (stats_x + bar_width + 20, bar_y_offset - 2))
        screen.blit(shield_text, (stats_x + bar_width + 20, bar_y_offset + 25))
