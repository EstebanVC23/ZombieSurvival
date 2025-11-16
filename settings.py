# ===================================================
# Configuración global del proyecto
# ===================================================

# Resolución de la ventana del juego
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

# Frames por segundo
FPS = 60

# ===================================================
# Mundo
# ===================================================

# Dimensiones del mundo (puede ser mayor que la pantalla para scroll)
WORLD_WIDTH = 4000
WORLD_HEIGHT = 4000

# ===================================================
# Player
# ===================================================

# Velocidad de movimiento del jugador (pixeles por segundo)
PLAYER_SPEED = 250

# Tamaño del sprite del jugador
PLAYER_SIZE = 100

# Salud base del jugador
PLAYER_BASE_HEALTH = 100

# Armadura inicial y máxima del jugador
PLAYER_BASE_ARMOR = 0
PLAYER_MAX_ARMOR = 100

# Cadencia de disparo: disparos por minuto
PLAYER_BASE_FIRE_RATE = 1000

# Capacidad del cargador y munición de reserva
PLAYER_BASE_MAGAZINE = 12
PLAYER_BASE_RESERVE_AMMO = 60

# ===================================================
# Armas
# ===================================================

# Daño base de las armas
WEAPON_BASE_DAMAGE = 14

# Disparos por minuto de las armas
WEAPON_BASE_RPM = 10

# Capacidad del cargador y munición de reserva de armas
WEAPON_BASE_MAGAZINE = 10
WEAPON_BASE_RESERVE_AMMO = 60

# Tiempo de recarga en segundos
WEAPON_BASE_RELOAD_TIME = 0.5

# Velocidad de las balas en pixeles por segundo
WEAPON_BULLET_SPEED = 900

# Tiempo de vida de cada bala en segundos
BULLET_BASE_LIFETIME = 1.0

# ===================================================
# Zombies
# ===================================================

# --- Zombie común ---
ZOMBIE_COMMON_SPEED = 70         # Velocidad de movimiento
ZOMBIE_COMMON_SIZE = 100         # Tamaño del sprite
ZOMBIE_COMMON_HP = 25            # Vida
ZOMBIE_COMMON_DAMAGE = 10        # Daño al jugador

# --- Zombie rápido ---
ZOMBIE_FAST_SPEED = 180
ZOMBIE_FAST_SIZE = 70
ZOMBIE_FAST_HP = 18
ZOMBIE_FAST_DAMAGE = 10

# --- Zombie tanque ---
ZOMBIE_TANK_SPEED = 40
ZOMBIE_TANK_SIZE = 180
ZOMBIE_TANK_HP = 80
ZOMBIE_TANK_DAMAGE = 30

# --- Zombie jefe (boss) ---
ZOMBIE_BOSS_SPEED = 55
ZOMBIE_BOSS_SIZE = 300
ZOMBIE_BOSS_HP = 300
ZOMBIE_BOSS_DAMAGE = 60

# ===================================================
# Niveles de zombies (progresivos por ola)
# ===================================================

# Nivel base del zombie en la ola 1
ZOMBIE_LEVEL_BASE_PER_WAVE = 1  

# Incremento progresivo de nivel por cada ola
ZOMBIE_LEVEL_INCREMENT_PER_WAVE = 0.5  

# Variación mínima y máxima respecto al nivel base de la ola
ZOMBIE_LEVEL_MIN_VARIATION = 0   
ZOMBIE_LEVEL_MAX_VARIATION = 2   

# ===================================================
# Rareza y multiplicadores
# ===================================================

# Probabilidades base de rareza (serán ajustadas dinámicamente según la ola)
ZOMBIE_RARITY_CHANCE = {
    "common": 50,
    "uncommon": 25,
    "rare": 15,
    "epic": 7,
    "legendary": 3
}

# Multiplicador de estadísticas según rareza
ZOMBIE_RARITY_MULT = {
    "common": 1.0,
    "uncommon": 1.2,
    "rare": 1.5,
    "epic": 2.0,
    "legendary": 3.0
}

# Cantidad de mejoras adicionales según rareza
ZOMBIE_RARITY_UPGRADE_COUNT = {
    "common": 1,
    "uncommon": 1,
    "rare": 2,
    "epic": 2,
    "legendary": 3
}

# Multiplicador de puntos según rareza
ZOMBIE_RARITY_SCORE_MULT = {
    "common": 1.0,
    "uncommon": 1.2,
    "rare": 1.5,
    "epic": 2.0,
    "legendary": 3.0
}

# Bonus de drop según rareza (puntos o mejoras)
ZOMBIE_RARITY_DROP_BONUS = {
    "common": 0,
    "uncommon": 5,
    "rare": 10,
    "epic": 20,
    "legendary": 40
}

# Probabilidad total de que un upgrade aparezca según tipo de zombie
UPGRADE_SPAWN_CHANCE_TOTAL = {
    "common": 20,
    "fast": 25,
    "tank": 35,
    "boss": 50
}

# ===================================================
# Mejoras (Upgrades)
# ===================================================

# Tamaño del ícono de la mejora
UPGRADE_ICON_SIZE = 72

# Valores que aporta cada mejora
UPGRADE_VALUES = {
    "vida": 25,        # Suma de vida al jugador
    "cadencia": 10,    # Incremento de cadencia de disparo
    "velocidad": 5,    # Incremento de velocidad de movimiento
    "balas": 20,       # Munición extra
    "cargador": 4,     # Capacidad adicional de cargador
    "armadura": 10     # Armadura extra
}

# Probabilidad de spawn individual por tipo de upgrade
UPGRADE_SPAWN_CHANCE = {
    "vida": 10,
    "cadencia": 10,
    "velocidad": 10,
    "balas": 20,
    "cargador": 20,
    "armadura": 10
}

# Multiplicador de mejoras según tipo de zombie
ZOMBIE_UPGRADE_MULTIPLIERS = {
    "common": 0.3,
    "fast": 0.7,
    "tank": 1.0,
    "boss": 3.0
}

# Física de caída de las mejoras
UPGRADE_FALL_SPEED = 150.0      # Velocidad inicial de caída
UPGRADE_FALL_DECAY = 0.95       # Decaimiento de velocidad por frame
UPGRADE_FALL_DURATION = 0.7     # Duración total de la caída en segundos

# ===================================================
# Puntuación
# ===================================================

# Puntos otorgados al matar cada tipo de zombie
ZOMBIE_SCORE_VALUES = {
    "common": 10,
    "fast": 15,
    "tank": 40,
    "boss": 200
}

# ===================================================
# Colores
# ===================================================

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (200, 30, 30)
GREEN = (30, 200, 30)
BLUE = (30, 30, 200)
YELLOW = (240, 220, 60)
GREY = (100, 100, 100)

# ===================================================
# Rutas de recursos
# ===================================================

# Carpeta de imágenes
ASSETS_IMAGES = "assets/images"

# Carpeta de sonidos y música
ASSETS_SOUNDS = "assets/sounds"
