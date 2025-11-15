# ui/map.py
import pygame
from settings import WORLD_WIDTH, WORLD_HEIGHT


class MiniMap:
    """
    Minimap estático (no sigue cámara). Recibe referencia a game para leer:
      - game.player (debe tener .pos: Vector2)
      - game.zombies (iterable de zombies con .pos: Vector2 y .dead flag)
      - game.upgrades (iterable de upgrades con .pos: Vector2)
    Actualiza los arrays de posiciones cada `update_interval_ms` para ahorrar CPU.
    """

    def __init__(
        self,
        game,
        width: int = 180,
        height: int = 180,
        margin: int = 12,
        position: str = "topright",  # 'topleft', 'topright'
        bg_color=(18, 18, 18, 200),
        border_color=(100, 100, 100),
        update_interval_ms: int = 100,
    ):
        self.game = game
        self.width = width
        self.height = height
        self.margin = margin
        self.position = position
        self.bg_color = bg_color
        self.border_color = border_color

        # escala mundo -> minimapa
        self.scale_x = self.width / float(max(1, WORLD_WIDTH))
        self.scale_y = self.height / float(max(1, WORLD_HEIGHT))

        # cache de posiciones (listas de tuplas (x,y) en coordenadas del minimapa)
        self._player_pos = (0, 0)
        self._zombie_positions = []  # lista de (x,y)
        self._upgrade_positions = []

        # temporizador para actualizar caches (ms)
        self.update_interval_ms = int(update_interval_ms)
        self._last_update_ms = 0

        # superficie del minimapa (con alpha)
        self.surface = pygame.Surface((self.width + 2 * self.margin, self.height + 2 * self.margin), pygame.SRCALPHA)

    def world_to_map(self, wx: float, wy: float):
        """Convierte coordenadas del mundo (wx,wy) a coordenadas en la superficie del minimapa."""
        mx = int(wx * self.scale_x) + self.margin
        my = int(wy * self.scale_y) + self.margin
        # clamp por si algo sale del rango
        mx = max(self.margin, min(self.margin + self.width, mx))
        my = max(self.margin, min(self.margin + self.height, my))
        return mx, my

    def _recompute_positions(self):
        """Recalcula y cachea posiciones de player, zombies y upgrades."""
        game = self.game

        # player
        player = getattr(game, "player", None)
        if player is not None and hasattr(player, "pos"):
            self._player_pos = self.world_to_map(player.pos.x, player.pos.y)
        else:
            self._player_pos = (self.margin + self.width // 2, self.margin + self.height // 2)

        # zombies
        zs = []
        try:
            for z in getattr(game, "zombies", []):
                # ignorar si no tiene pos
                if getattr(z, "dead", False):
                    continue
                if hasattr(z, "pos"):
                    zs.append(self.world_to_map(z.pos.x, z.pos.y))
        except Exception:
            zs = []
        self._zombie_positions = zs

        # upgrades (no recogidos)
        ups = []
        try:
            for u in getattr(game, "upgrades", []):
                # asumo que las upgrades en group son las no recogidas
                if hasattr(u, "pos"):
                    ups.append(self.world_to_map(u.pos.x, u.pos.y))
        except Exception:
            ups = []
        self._upgrade_positions = ups

    def update_if_needed(self):
        """Llama a recompute solo si pasó el intervalo."""
        now = pygame.time.get_ticks()
        if now - self._last_update_ms >= self.update_interval_ms:
            self._recompute_positions()
            self._last_update_ms = now

    def draw(self, surface):
        """
        Dibuja el minimapa en la esquina indicada.
        Llama a update_if_needed() internamente.
        """
        self.update_if_needed()

        sw = surface.get_width()
        sh = surface.get_height()

        # coordenadas de la esquina (posición final)
        if self.position == "topright":
            map_x = sw - (self.width + 2 * self.margin) - 12
            map_y = 12
        else:
            # default top-left
            map_x = 12
            map_y = 12

        # limpiar surface local
        self.surface.fill((0, 0, 0, 0))

        # fondo con ligero alpha
        bg_surf = pygame.Surface((self.width + 2 * self.margin, self.height + 2 * self.margin), pygame.SRCALPHA)
        bg_color = self.bg_color
        if len(bg_color) == 4:
            bg_surf.fill(bg_color)
        else:
            bg_surf.fill((*bg_color, 200))
        self.surface.blit(bg_surf, (0, 0))

        # borde
        pygame.draw.rect(
            self.surface,
            self.border_color,
            (0, 0, self.width + 2 * self.margin, self.height + 2 * self.margin),
            width=2,
            border_radius=6,
        )

        # inner rect (donde están los puntos)
        inner_rect = pygame.Rect(self.margin, self.margin, self.width, self.height)
        # opcional borde interior sutil
        pygame.draw.rect(self.surface, (40, 40, 40), inner_rect, width=1)

        # dibujar upgrades (azul pequeños)
        for ux, uy in self._upgrade_positions:
            # pequeños puntos azules
            pygame.draw.circle(self.surface, (60, 140, 255), (ux, uy), 3)

        # dibujar zombies (rojo)
        for zx, zy in self._zombie_positions:
            pygame.draw.circle(self.surface, (220, 50, 50), (zx, zy), 3)

        # dibujar jugador (verde, un poco más grande)
        px, py = self._player_pos
        pygame.draw.circle(self.surface, (80, 220, 80), (px, py), 4)

        # Opcional: pequeña cruz en el jugador
        try:
            pygame.draw.line(self.surface, (0, 0, 0), (px - 3, py), (px + 3, py), 1)
            pygame.draw.line(self.surface, (0, 0, 0), (px, py - 3), (px, py + 3), 1)
        except Exception:
            pass

        # Blit final en la pantalla
        surface.blit(self.surface, (map_x, map_y))

        # guardar último rect si es necesario para debugging o clicks
        self.screen_rect = pygame.Rect(map_x, map_y, self.width + 2 * self.margin, self.height + 2 * self.margin)
