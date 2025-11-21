# ===================================================
# CONFIGURACIÓN GLOBAL DEL PROYECTO
# ===================================================

# ===================================================
# PANTALLA Y RENDIMIENTO
# ===================================================

# Resolución de la ventana del juego (usado en modo ventana)
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

# Frames por segundo (rendimiento del juego)
FPS = 60

# ===================================================
# MUNDO
# ===================================================

# Dimensiones del mundo (mayor que la pantalla para permitir scroll)
WORLD_WIDTH = 4000
WORLD_HEIGHT = 4000

# ===================================================
# JUGADOR (PLAYER)
# ===================================================

# --- Movimiento ---
PLAYER_SPEED = 500  # Velocidad de movimiento en píxeles/segundo

# --- Apariencia ---
PLAYER_SIZE = 100  # Tamaño del sprite del jugador

# --- Salud y Defensa ---
PLAYER_BASE_HEALTH = 100      # Salud inicial del jugador
PLAYER_BASE_ARMOR = 0         # Armadura inicial
PLAYER_MAX_ARMOR = 100        # Capacidad máxima de armadura

# --- Colisiones ---
PLAYER_MIN_DISTANCE_TO_ZOMBIE = 5  # Distancia mínima que el player debe mantener con los zombies

# ===================================================
# ARMAS Y BALAS
# ===================================================

# --- Estadísticas base del arma ---
WEAPON_BASE_DAMAGE = 10000         # Daño por bala
WEAPON_BASE_RPM = 1000             # Disparos por minuto
WEAPON_BASE_MAGAZINE = 12          # Capacidad del cargador
WEAPON_BASE_RESERVE_AMMO = 100     # Munición de reserva
WEAPON_BASE_RELOAD_TIME = 2.0      # Tiempo de recarga en segundos
SPRITE_ANGLE_OFFSET = 45.0         # Offset para rotar sprites de armas y balas

# --- Proyectiles ---
WEAPON_BULLET_SPEED = 1300         # Velocidad de las balas en píxeles/segundo
BULLET_BASE_LIFETIME = 1.0         # Tiempo de vida de cada bala en segundos

# ===================================================
# SPAWNER - CONTROL DE OLAS Y GENERACIÓN DE ZOMBIES
# ===================================================

SPAWNER_TIME_BETWEEN_WAVES = 3.0          # Tiempo entre olas
SPAWNER_SPAWN_INTERVAL = 0.5              # Intervalo entre spawn de zombies
SPAWNER_MIN_DISTANCE_TO_PLAYER = 450      # Distancia mínima de spawn respecto al jugador
MAX_ZOMBIES_ON_MAP = 100                  # Máximo de zombies simultáneos en el mapa

# Multiplicadores para olas múltiplo de 10 (boss, fast, tank, common)
SPAWNER_MULTIPLIER_WAVE_10 = {
    "boss": 5.5,    # +150% sobre la chance base
    "fast": 1.8,    # +50%
    "tank": 1.0,    # +50%
    "common": 0.5   # disminuye la chance de comunes
}

# Probabilidades de spawn de zombies por tipo y ola
ZOMBIE_SPAWN_CHANCE_BY_WAVE = {
    "1-5":   {"common": 1.0,   "fast": 0.0,   "tank": 0.0,   "boss": 0.0},
    "6-7":   {"common": 0.7,   "fast": 0.3,   "tank": 0.0,   "boss": 0.0},
    "8-9":   {"common": 0.6,   "fast": 0.3,   "tank": 0.1,   "boss": 0.0},
    "10+":   {"common": 0.45,  "fast": 0.3,   "tank": 0.2,   "boss": 0.05}
}

# ===================================================
# ZOMBIES - ESTADÍSTICAS BASE POR TIPO
# ===================================================

# Zombie Común
ZOMBIE_COMMON_SPEED = 80
ZOMBIE_COMMON_SIZE = 100
ZOMBIE_COMMON_HP = 40
ZOMBIE_COMMON_DAMAGE = 8

# Zombie Rápido
ZOMBIE_FAST_SPEED = 200
ZOMBIE_FAST_SIZE = 70
ZOMBIE_FAST_HP = 25
ZOMBIE_FAST_DAMAGE = 12

# Zombie Tanque
ZOMBIE_TANK_SPEED = 50
ZOMBIE_TANK_SIZE = 180
ZOMBIE_TANK_HP = 150
ZOMBIE_TANK_DAMAGE = 25

# Zombie Jefe (Boss)
ZOMBIE_BOSS_SPEED = 70
ZOMBIE_BOSS_SIZE = 300
ZOMBIE_BOSS_HP = 400
ZOMBIE_BOSS_DAMAGE = 40

# ===================================================
# SISTEMA DE NIVELES DE ZOMBIES (PROGRESIÓN POR OLA)
# ===================================================

ZOMBIE_LEVEL_BASE_PER_WAVE = 1
ZOMBIE_LEVEL_INCREMENT_PER_WAVE = 0.4
ZOMBIE_LEVEL_MIN_VARIATION = -1
ZOMBIE_LEVEL_MAX_VARIATION = 2

# ===================================================
# SISTEMA DE DETECCIÓN Y MOVIMIENTO
# ===================================================

ZOMBIE_DETECTION_RADIUS = 800        # Radio de detección del jugador
ZOMBIE_ALERT_RADIUS = 400            # Radio de alerta para otros zombies
ZOMBIE_WANDER_CHANGE_DIR_CHANCE = 0.01
ZOMBIE_WANDER_SPEED_MULT = 0.8
ZOMBIE_REPULSION_RADIUS = 30
ZOMBIE_REPULSION_FORCE = 20
ZOMBIE_MIN_DISTANCE_TO_PLAYER = 30   # Distancia mínima que un zombie mantiene respecto al jugador

# Cooldown de ataque por tipo
ZOMBIE_ATTACK_COOLDOWN = {
    "common": 0.8,
    "fast":   0.4,
    "tank":   1.0,
    "boss":   1.5
}

# ===================================================
# SISTEMA DE RAREZAS DE ZOMBIES
# ===================================================

# Probabilidad base por rareza (%)
ZOMBIE_RARITY_CHANCE = {
    "common": 55,
    "uncommon": 25,
    "rare": 12,
    "epic": 7.5,
    "legendary": 0.5
}

# Multiplicador de estadísticas por rareza
ZOMBIE_RARITY_MULT = {
    "common": 1.0,
    "uncommon": 1.3,
    "rare": 1.5,
    "epic": 1.8,
    "legendary": 2.0
}

# Cantidad de estadísticas mejoradas por rareza
ZOMBIE_RARITY_UPGRADE_COUNT = {
    "common": 1,
    "uncommon": 1,
    "rare": 2,
    "epic": 2,
    "legendary": 3
}

# Multiplicador de puntos por rareza
ZOMBIE_RARITY_SCORE_MULT = {
    "common": 1.0,
    "uncommon": 1.5,
    "rare": 2.0,
    "epic": 3.0,
    "legendary": 5.0
}

# Bonus de probabilidad de drop según rareza
ZOMBIE_RARITY_DROP_BONUS = {
    "common": 0,
    "uncommon": 5,
    "rare": 12,
    "epic": 25,
    "legendary": 50
}

# Incremento de stats por nivel y tipo de zombie
ZOMBIE_LEVEL_UP_STATS = {
    "common": {"hp": 1,  "damage": 1,  "speed": 1},
    "fast":   {"hp": 1,  "damage": 1,  "speed": 3},
    "tank":   {"hp": 8,  "damage": 3, "speed": 0.5},
    "boss":   {"hp": 20, "damage": 10, "speed": 1},
}

# ===================================================
# SISTEMA UNIFICADO DE DROPS DE MEJORAS
# ===================================================

ZOMBIE_UPGRADE_DROP_SYSTEM = {
    "common": {"base_chance": 10, "min_drops": 1, "max_drops": 2, "multi_drop_chance": 5},
    "fast":   {"base_chance": 30, "min_drops": 1, "max_drops": 3, "multi_drop_chance": 20},
    "tank":   {"base_chance": 50, "min_drops": 2, "max_drops": 4, "multi_drop_chance": 20},
    "boss":   {"base_chance": 100,"min_drops": 2, "max_drops": 5, "multi_drop_chance": 10}
}

# ===================================================
# MEJORAS (UPGRADES) - VALORES Y PROBABILIDADES
# ===================================================

UPGRADE_ICON_SIZE = 72  # Tamaño del ícono

UPGRADE_VALUES = {
    "vida": 25,
    "vida_extra": 5,
    "armadura": 10,
    "daño": 1,
    "cadencia": 2,
    "velocidad": 1,
    "balas": 25,
    "cargador": 2
}

UPGRADE_SPAWN_CHANCE = {
    "vida": 10,
    "vida_extra": 10,
    "armadura": 10,
    "daño": 10,
    "cadencia": 10,
    "velocidad": 10,
    "balas": 10,
    "cargador": 10
}

UPGRADE_FALL_SPEED = 150.0
UPGRADE_FALL_DECAY = 0.95
UPGRADE_FALL_DURATION = 0.7

# ===================================================
# PUNTUACIÓN
# ===================================================

ZOMBIE_SCORE_VALUES = {
    "common": 10,
    "fast": 20,
    "tank": 50,
    "boss": 300
}

# ===================================================
# SONIDO DE ZOMBIES
# ===================================================

ZOMBIE_SOUND_DISTANCE = 500
ZOMBIE_SOUND_MIN_INTERVAL = 1.5
ZOMBIE_SOUND_MAX_INTERVAL = 4.0

# ===================================================
# RUTAS DE RECURSOS
# ===================================================

ASSETS_IMAGES = "assets/images"
ASSETS_SOUNDS = "assets/sounds"

# -----------------------------
# Mapa de terreno / objetos
# -----------------------------
TERRAIN_DIR = "terrain"
TERRAIN_TILE_SIZE = 100
TERRAIN_DEFAULT_LETTER = "G"

# El mapa interpreta cada letra como un tile u objeto
# mapa letra -> nombre de fichero (sin extension) (usa solo terrenos)
TERRAIN_LETTER_MAP = {
    "D": "dirt",
    "F": "forest_ground",
    "G": "grass",
    "I": "ice",
    "M": "mud",
    "R": "rock",
    "S": "sand",
    "N": "snow",
    "W": "water",
    "L": "lava",
}

# ===================================================
# TERRENOS PERMITIDOS PARA GENERAR EL MUNDO
# ===================================================
# Si está en None → se generan TODOS los biomas de mapa por defecto.
# Si contiene una lista → solo se generan esos biomas coherentes.
# Tamaño del tile
TILE_SIZE = 100

# Ejemplos:
# WORLD_ALLOWED_TERRAINS = ["G"]                     # solo grass
# WORLD_ALLOWED_TERRAINS = ["G", "F", "M"]           # grass, forest, mud
# WORLD_ALLOWED_TERRAINS = ["W", "S"]                # water + sand
# WORLD_ALLOWED_TERRAINS = ["N", "I"]                # nieve + hielo

# Radio de visión del jugador sobre el mapa (en tiles)
MAP_TILE_VISION_RADIUS = 8


