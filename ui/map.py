# ui/map.py
import pygame
import math
from settings import WORLD_WIDTH, WORLD_HEIGHT, TILE_SIZE, MAP_TILE_VISION_RADIUS

# Colores por tipo de terreno (ajusta si quieres otras paletas)
TERRAIN_COLOR = {
    "D": (137, 94, 66),     # dirt
    "F": (34, 88, 34),      # forest_ground
    "G": (95, 160, 60),     # grass
    "I": (180, 220, 240),   # ice
    "M": (90, 70, 40),      # mud
    "R": (120, 120, 120),   # rock
    "S": (212, 185, 140),   # sand
    "N": (230, 230, 250),   # snow
    "W": (60, 100, 180),    # water
    "L": (200, 60, 40),     # lava
    # fallback
    "":  (100, 100, 100),
}

# ========================= Datos del Minimap =========================
class MiniMapData:
    """Gestiona posiciones de jugador, zombies y upgrades y la exploración (fog-of-war)."""

    def __init__(self, game):
        self.game = game
        self._player_pos = (0, 0)
        self._zombie_positions = []
        self._upgrade_positions = []

        # mapa base (lista de listas) y dimensiones en tiles
        self.map_matrix = None
        self.cols = 0
        self.rows = 0

        # grid explored (rows x cols) - False = no explorado, True = explorado
        self.explored = []

        # mantener la correspondencia de world -> tiles
        self.tile_size_world = TILE_SIZE

        # cargar mapa si ya existe o será generado por game (opcional)
        # Nota: El Game normalmente llamará a load_map_file en initialize_game_state.
        # Aquí solo mantenemos referencias si el mapa ya está en game.tilemap.
        if hasattr(game, "tilemap") and game.tilemap:
            # tilemap.matrix puede ser lista de lists o list of strings
            mat = getattr(game.tilemap, "matrix", None)
            if mat:
                # normalizar a lista de listas de strings (1 char each)
                self.map_matrix = [list(r) if isinstance(r, str) else r for r in mat]
                self.cols = game.tilemap.cols
                self.rows = game.tilemap.rows
                self._ensure_explored_size()

    def _ensure_explored_size(self):
        if self.cols <= 0 or self.rows <= 0:
            return
        if not self.explored or len(self.explored) != self.rows or len(self.explored[0]) != self.cols:
            self.explored = [[False for _ in range(self.cols)] for _ in range(self.rows)]

    def set_map(self, matrix):
        """Asignar/actualizar la matriz del mapa (lista de listas)."""
        if matrix is None:
            return
        self.map_matrix = [list(r) if isinstance(r, str) else r for r in matrix]
        self.rows = len(self.map_matrix)
        self.cols = len(self.map_matrix[0]) if self.rows else 0
        self._ensure_explored_size()

    def world_to_map(self, wx: float, wy: float, width: int, height: int, margin: int):
        """
        Convierte coordenadas world (px) a coordenadas de minimapa (px).
        Mantiene escala del mundo completo comprimido dentro del minimapa area (width x height).
        """
        # evitar división por cero
        mx = int(wx * (width / max(1, WORLD_WIDTH))) + margin
        my = int(wy * (height / max(1, WORLD_HEIGHT))) + margin
        mx = max(margin, min(margin + width, mx))
        my = max(margin, min(margin + height, my))
        return mx, my

    def recompute_positions(self, width: int, height: int, margin: int):
        """
        Recalcula posiciones en px para el minimapa de player, zombies y upgrades.
        Los zombies/upgrades solo se incluyen si su tile ya está explorado.
        """
        game = self.game

        # asegurar que map_matrix/explored existen y tienen tamaño correcto
        if not self.map_matrix and hasattr(game, "tilemap") and game.tilemap:
            self.set_map(game.tilemap.matrix)

        # Player
        player = getattr(game, "player", None)
        if player and hasattr(player, "pos"):
            self._player_pos = self.world_to_map(player.pos.x, player.pos.y, width, height, margin)
        else:
            self._player_pos = (margin + width // 2, margin + height // 2)

        # Zombies (solo si tile explorado)
        zs = []
        try:
            for z in getattr(game, "zombies", []):
                if getattr(z, "dead", False):
                    continue
                if hasattr(z, "pos"):
                    tx = int(z.pos.x // self.tile_size_world)
                    ty = int(z.pos.y // self.tile_size_world)
                    if 0 <= ty < self.rows and 0 <= tx < self.cols and self.explored[ty][tx]:
                        zs.append(self.world_to_map(z.pos.x, z.pos.y, width, height, margin))
        except Exception:
            zs = []
        self._zombie_positions = zs

        # Upgrades (solo si tile explorado)
        ups = []
        try:
            for u in getattr(game, "upgrades", []):
                if hasattr(u, "pos"):
                    tx = int(u.pos.x // self.tile_size_world)
                    ty = int(u.pos.y // self.tile_size_world)
                    if 0 <= ty < self.rows and 0 <= tx < self.cols and self.explored[ty][tx]:
                        ups.append(self.world_to_map(u.pos.x, u.pos.y, width, height, margin))
        except Exception:
            ups = []
        self._upgrade_positions = ups


# ========================= Renderizado del Minimap =========================
class MiniMapRenderer:
    """Dibuja el minimapa — incluye terreno (solo tiles explorados), fog (negro) y entidades."""

    def __init__(self, width: int, height: int, margin: int, bg_color, border_color):
        self.width = width
        self.height = height
        self.margin = margin
        self.bg_color = bg_color
        self.border_color = border_color

        # surface total incluye margenes
        self.surface = pygame.Surface((self.width + 2 * self.margin, self.height + 2 * self.margin), pygame.SRCALPHA)
        self._terrain_surf_cache = None  # superficie con colores de terreno (no fog)
        self.pulse_timer = 0
        self.screen_rect = pygame.Rect(0, 0, self.width + 2 * self.margin, self.height + 2 * self.margin)

    def _build_terrain_surface(self, map_matrix, cols, rows):
        """
        Construye (o reconstruye) una superficie con el terreno completo escalado a minimap area.
        NO aplica fog — fog se aplica dinámicamente en draw() usando explored grid.
        """
        if not map_matrix or cols <= 0 or rows <= 0:
            # vacía
            surf = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            surf.fill((0, 0, 0))
            return surf

        tile_w = max(1, self.width / cols)
        tile_h = max(1, self.height / rows)

        surf = pygame.Surface((self.width, self.height))
        surf.fill((0, 0, 0))

        for ty in range(rows):
            for tx in range(cols):
                ch = map_matrix[ty][tx].upper() if ty < len(map_matrix) and tx < len(map_matrix[ty]) else "G"
                color = TERRAIN_COLOR.get(ch, TERRAIN_COLOR.get("", (100,100,100)))
                # rect en float para mejor escalado final
                r = pygame.Rect(int(tx * tile_w), int(ty * tile_h), int(math.ceil(tile_w)), int(math.ceil(tile_h)))
                surf.fill(color, r)

        return surf

    def draw(self, surface, data: MiniMapData, position: str = "topright"):
        # recompute positions done by caller
        self.pulse_timer += 0.1
        pulse = abs(math.sin(self.pulse_timer)) * 0.3 + 0.7

        sw, sh = surface.get_size()
        map_x = sw - (self.width + 2 * self.margin) - 12 if position == "topright" else 12
        map_y = 12

        # reconfirm map_matrix
        if not data.map_matrix or data.cols <= 0 or data.rows <= 0:
            # nothing to draw but background and player
            self.surface.fill((0,0,0,0))
        else:
            # build terrain cache if necessary or if dims changed
            if self._terrain_surf_cache is None or self._terrain_surf_cache.get_width() != self.width or self._terrain_surf_cache.get_height() != self.height:
                try:
                    self._terrain_surf_cache = self._build_terrain_surface(data.map_matrix, data.cols, data.rows)
                except Exception:
                    self._terrain_surf_cache = pygame.Surface((self.width, self.height))
                    self._terrain_surf_cache.fill((0,0,0))

        # limpiar surface
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

        # Dibuja terreno explorado (textura cacheada) y fog encima
        if self._terrain_surf_cache:
            # blit terrain scaled area
            self.surface.blit(self._terrain_surf_cache, (self.margin, self.margin))

            # aplicar fog: dibujar rects negros sobre tiles NO explorados
            tile_w = max(1, self.width / max(1, data.cols))
            tile_h = max(1, self.height / max(1, data.rows))
            fog = pygame.Surface((int(math.ceil(tile_w)), int(math.ceil(tile_h))))
            fog.fill((0, 0, 0))
            fog.set_alpha(255)

            for ty in range(data.rows):
                for tx in range(data.cols):
                    if not data.explored[ty][tx]:
                        rx = int(self.margin + tx * tile_w)
                        ry = int(self.margin + ty * tile_h)
                        self.surface.blit(fog, (rx, ry))

        # Upgrades (solo si su tile explorado)
        for ux, uy in data._upgrade_positions:
            pygame.draw.circle(self.surface, (30, 100, 200, 120), (ux, uy), 5)
            pygame.draw.circle(self.surface, (80, 160, 255), (ux, uy), 3)
            pygame.draw.circle(self.surface, (150, 200, 255), (ux, uy), 1)

        # Zombies (solo si su tile explorado)
        for zx, zy in data._zombie_positions:
            pygame.draw.circle(self.surface, (200, 40, 40, 150), (zx, zy), 4)
            pygame.draw.circle(self.surface, (255, 80, 80), (zx, zy), 2)

        # Jugador (siempre visible)
        px, py = data._player_pos
        pulse_radius = int(7 + pulse * 2)
        pygame.draw.circle(self.surface, (60, 200, 60, int(80 * pulse)), (px, py), pulse_radius)
        pygame.draw.circle(self.surface, (70, 220, 70), (px, py), 5)
        pygame.draw.circle(self.surface, (120, 255, 120), (px, py), 3)
        pygame.draw.line(self.surface, (200, 255, 200), (px - 4, py), (px + 4, py), 2)
        pygame.draw.line(self.surface, (200, 255, 200), (px, py - 4), (px, py + 4), 2)

        # Blit final en la pantalla
        surface.blit(self.surface, (map_x, map_y))
        self.screen_rect = pygame.Rect(map_x, map_y, self.width + 2 * self.margin, self.height + 2 * self.margin)


# ========================= Minimap Principal =========================
class MiniMap:
    """Coordinador de datos, exploration grid y renderizado del minimapa."""

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
        self.game = game
        self.position = position
        self.update_interval_ms = update_interval_ms
        self._last_update_ms = 0

        self.data = MiniMapData(game)
        self.renderer = MiniMapRenderer(width, height, margin, bg_color, border_color)

        # visión en tiles (radio circular)
        try:
            self.vision_radius = int(MAP_TILE_VISION_RADIUS)
        except Exception:
            self.vision_radius = 3

        # Si el juego ya generó tilemap, sincronizamos la matriz
        if hasattr(game, "tilemap") and game.tilemap:
            self.data.set_map(game.tilemap.matrix)
            # inicializar exploración: opcional marcar la posición inicial del player
            self.reveal_around_player(force=True)

    def update_if_needed(self):
        now = pygame.time.get_ticks()
        if now - self._last_update_ms >= self.update_interval_ms:
            self.reveal_around_player()
            self.data.recompute_positions(self.renderer.width, self.renderer.height, self.renderer.margin)
            self._last_update_ms = now

    def reveal_around_player(self, force: bool = False):
        """
        Revela tiles dentro de un círculo de radio self.vision_radius alrededor del jugador.
        Si force=True forzamos la actualización inmediata (útil al iniciar).
        """
        game = self.game
        if not hasattr(game, "player") or not self.data.map_matrix:
            return

        px = game.player.pos.x
        py = game.player.pos.y
        tile_x = int(px // self.data.tile_size_world)
        tile_y = int(py // self.data.tile_size_world)

        if tile_x < 0 or tile_y < 0 or tile_y >= self.data.rows or tile_x >= self.data.cols:
            return

        r = self.vision_radius
        changed = False

        # círculo: usamos distancia euclidiana en coordenadas de tiles
        for dy in range(-r, r+1):
            ty = tile_y + dy
            if ty < 0 or ty >= self.data.rows:
                continue
            for dx in range(-r, r+1):
                tx = tile_x + dx
                if tx < 0 or tx >= self.data.cols:
                    continue
                if math.hypot(dx, dy) <= r:
                    if not self.data.explored[ty][tx]:
                        self.data.explored[ty][tx] = True
                        changed = True

        # Si cambió la exploración, invalidar cache del terrain (no necesario en este impl,
        # porque terrain cache no depende de explored) — pero podríamos usar para efectos
        if changed or force:
            # actualizar posiciones para que zombies/upgrades en tiles recién revelados aparezcan
            self.data.recompute_positions(self.renderer.width, self.renderer.height, self.renderer.margin)

    def draw(self, surface):
        # actualizar si es necesario
        self.update_if_needed()
        # pedir al renderer que dibuje todo
        self.renderer.draw(surface, self.data, self.position)
