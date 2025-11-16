# ===================================================
# Configuración global del proyecto
# ===================================================

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60

# ===================================================
# Mundo
# ===================================================

WORLD_WIDTH = 4000
WORLD_HEIGHT = 4000

# ===================================================
# Player
# ===================================================

PLAYER_SPEED = 250
PLAYER_SIZE = 100

PLAYER_BASE_HEALTH = 100
PLAYER_BASE_ARMOR = 0
PLAYER_MAX_ARMOR = 100

PLAYER_BASE_FIRE_RATE = 1000  # disparos por minuto
PLAYER_BASE_MAGAZINE = 12
PLAYER_BASE_RESERVE_AMMO = 60

# ===================================================
# Armas
# ===================================================

WEAPON_BASE_DAMAGE = 14
WEAPON_BASE_RPM = 10
WEAPON_BASE_MAGAZINE = 10
WEAPON_BASE_RESERVE_AMMO = 60
WEAPON_BASE_RELOAD_TIME = 0.5
WEAPON_BULLET_SPEED = 900
BULLET_BASE_LIFETIME = 1.0

# ===================================================
# Zombies
# ===================================================

ZOMBIE_COMMON_SPEED = 70
ZOMBIE_COMMON_SIZE = 100
ZOMBIE_COMMON_HP = 25
ZOMBIE_COMMON_DAMAGE = 100

ZOMBIE_FAST_SPEED = 180
ZOMBIE_FAST_SIZE = 70
ZOMBIE_FAST_HP = 18
ZOMBIE_FAST_DAMAGE = 10

ZOMBIE_TANK_SPEED = 40
ZOMBIE_TANK_SIZE = 180
ZOMBIE_TANK_HP = 80
ZOMBIE_TANK_DAMAGE = 30

ZOMBIE_BOSS_SPEED = 55
ZOMBIE_BOSS_SIZE = 300
ZOMBIE_BOSS_HP = 300
ZOMBIE_BOSS_DAMAGE = 60

# ===================================================
# Niveles de zombies
# ===================================================

ZOMBIE_LEVEL_MIN_VARIATION = -2   # mínimo ajuste de nivel respecto al base
ZOMBIE_LEVEL_MAX_VARIATION = 3    # máximo ajuste de nivel respecto al base

# ===================================================
# Rareza y multiplicadores (necesarios para Zombies)
# ===================================================

ZOMBIE_RARITY_CHANCE = {
    "common": 50,
    "uncommon": 25,
    "rare": 15,
    "epic": 7,
    "legendary": 3
}

ZOMBIE_RARITY_MULT = {
    "common": 1.0,
    "uncommon": 1.2,
    "rare": 1.5,
    "epic": 2.0,
    "legendary": 3.0
}

ZOMBIE_RARITY_UPGRADE_COUNT = {
    "common": 1,
    "uncommon": 1,
    "rare": 2,
    "epic": 2,
    "legendary": 3
}

ZOMBIE_RARITY_SCORE_MULT = {
    "common": 1.0,
    "uncommon": 1.2,
    "rare": 1.5,
    "epic": 2.0,
    "legendary": 3.0
}

ZOMBIE_RARITY_DROP_BONUS = {
    "common": 0,
    "uncommon": 5,
    "rare": 10,
    "epic": 20,
    "legendary": 40
}

UPGRADE_SPAWN_CHANCE_TOTAL = {
    "common": 20,
    "fast": 25,
    "tank": 35,
    "boss": 50
}

# ===================================================
# Mejoras (Upgrades)
# ===================================================

UPGRADE_ICON_SIZE = 72

UPGRADE_VALUES = {
    "vida": 25,
    "cadencia": 10,
    "velocidad": 5,
    "balas": 20,
    "cargador": 4,
    "armadura": 10
}

UPGRADE_SPAWN_CHANCE = {
    "vida": 10,
    "cadencia": 10,
    "velocidad": 10,
    "balas": 10,
    "cargador": 10,
    "armadura": 10
}

ZOMBIE_UPGRADE_MULTIPLIERS = {
    "common": 0.3,
    "fast": 0.7,
    "tank": 1.0,
    "boss": 3.0
}

UPGRADE_FALL_SPEED = 150.0
UPGRADE_FALL_DECAY = 0.95
UPGRADE_FALL_DURATION = 0.7

# ===================================================
# Puntuación
# ===================================================

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
# Rutas
# ===================================================

ASSETS_IMAGES = "assets/images"
ASSETS_SOUNDS = "assets/sounds"
