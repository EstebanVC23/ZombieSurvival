# ui/map.py
import pygame
import math
from settings import WORLD_WIDTH, WORLD_HEIGHT

# ========================= Datos del Minimap =========================
class MiniMapData:
    """Gestiona posiciones de jugador, zombies y upgrades."""

    def __init__(self, game):
        self.game = game
        self._player_pos = (0, 0)
        self._zombie_positions = []
        self._upgrade_positions = []

    def world_to_map(self, wx: float, wy: float, width: int, height: int, margin: int):
        mx = int(wx * (width / max(1, WORLD_WIDTH))) + margin
        my = int(wy * (height / max(1, WORLD_HEIGHT))) + margin
        mx = max(margin, min(margin + width, mx))
        my = max(margin, min(margin + height, my))
        return mx, my

    def recompute_positions(self, width: int, height: int, margin: int):
        game = self.game
        player = getattr(game, "player", None)
        if player and hasattr(player, "pos"):
            self._player_pos = self.world_to_map(player.pos.x, player.pos.y, width, height, margin)
        else:
            self._player_pos = (margin + width // 2, margin + height // 2)

        # Zombies
        zs = []
        try:
            for z in getattr(game, "zombies", []):
                if getattr(z, "dead", False): 
                    continue
                if hasattr(z, "pos"):
                    zs.append(self.world_to_map(z.pos.x, z.pos.y, width, height, margin))
        except Exception:
            zs = []
        self._zombie_positions = zs

        # Upgrades
        ups = []
        try:
            for u in getattr(game, "upgrades", []):
                if hasattr(u, "pos"):
                    ups.append(self.world_to_map(u.pos.x, u.pos.y, width, height, margin))
        except Exception:
            ups = []
        self._upgrade_positions = ups

# ========================= Renderizado del Minimap =========================
class MiniMapRenderer:
    """Se encarga de dibujar el minimapa y todos sus elementos."""

    def __init__(self, width: int, height: int, margin: int, bg_color, border_color):
        self.width = width
        self.height = height
        self.margin = margin
        self.bg_color = bg_color
        self.border_color = border_color
        self.surface = pygame.Surface((self.width + 2 * self.margin, self.height + 2 * self.margin), pygame.SRCALPHA)
        self.pulse_timer = 0
        self.screen_rect = pygame.Rect(0, 0, self.width + 2 * self.margin, self.height + 2 * self.margin)

    def draw(self, surface, data: MiniMapData, position: str = "topright"):
        data.recompute_positions(self.width, self.height, self.margin)
        self.pulse_timer += 0.1
        pulse = abs(math.sin(self.pulse_timer)) * 0.3 + 0.7

        sw, sh = surface.get_size()
        map_x = sw - (self.width + 2 * self.margin) - 12 if position == "topright" else 12
        map_y = 12

        self.surface.fill((0, 0, 0, 0))

        # Sombra
        shadow = pygame.Surface((self.width + 2 * self.margin, self.height + 2 * self.margin), pygame.SRCALPHA)
        shadow.fill((0, 0, 0, 80))
        surface.blit(shadow, (map_x + 3, map_y + 3))

        # Fondo
        bg_surf = pygame.Surface((self.width + 2 * self.margin, self.height + 2 * self.margin), pygame.SRCALPHA)
        bg_surf.fill(self.bg_color)
        self.surface.blit(bg_surf, (0, 0))

        # Bordes
        pygame.draw.rect(self.surface, (70, 80, 100), (0, 0, self.width + 2 * self.margin, self.height + 2 * self.margin), width=2, border_radius=8)
        pygame.draw.rect(self.surface, (40, 45, 55), (self.margin, self.margin, self.width, self.height), width=1, border_radius=4)

        # Upgrades
        for ux, uy in data._upgrade_positions:
            pygame.draw.circle(self.surface, (30, 100, 200, 120), (ux, uy), 5)
            pygame.draw.circle(self.surface, (80, 160, 255), (ux, uy), 3)
            pygame.draw.circle(self.surface, (150, 200, 255), (ux, uy), 1)

        # Zombies
        for zx, zy in data._zombie_positions:
            pygame.draw.circle(self.surface, (200, 40, 40, 150), (zx, zy), 4)
            pygame.draw.circle(self.surface, (255, 80, 80), (zx, zy), 2)

        # Jugador
        px, py = data._player_pos
        pulse_radius = int(7 + pulse * 2)
        pygame.draw.circle(self.surface, (60, 200, 60, int(80 * pulse)), (px, py), pulse_radius)
        pygame.draw.circle(self.surface, (70, 220, 70), (px, py), 5)
        pygame.draw.circle(self.surface, (120, 255, 120), (px, py), 3)
        pygame.draw.line(self.surface, (200, 255, 200), (px - 4, py), (px + 4, py), 2)
        pygame.draw.line(self.surface, (200, 255, 200), (px, py - 4), (px, py + 4), 2)

        # Blit final
        surface.blit(self.surface, (map_x, map_y))
        self.screen_rect = pygame.Rect(map_x, map_y, self.width + 2 * self.margin, self.height + 2 * self.margin)

# ========================= Minimap Principal =========================
class MiniMap:
    """Coordinador de datos y renderizado del minimapa."""

    def __init__(
        self,
        game,
        width: int = 180,
        height: int = 180,
        margin: int = 12,
        position: str = "topright",
        bg_color=(15, 15, 20, 230),
        border_color=(80, 90, 110),
        update_interval_ms: int = 100
    ):
        self.position = position
        self.update_interval_ms = update_interval_ms
        self._last_update_ms = 0

        self.data = MiniMapData(game)
        self.renderer = MiniMapRenderer(width, height, margin, bg_color, border_color)

    def update_if_needed(self):
        now = pygame.time.get_ticks()
        if now - self._last_update_ms >= self.update_interval_ms:
            self.data.recompute_positions(self.renderer.width, self.renderer.height, self.renderer.margin)
            self._last_update_ms = now

    def draw(self, surface):
        self.update_if_needed()
        self.renderer.draw(surface, self.data, self.position)
