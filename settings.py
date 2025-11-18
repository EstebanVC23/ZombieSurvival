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
PLAYER_SPEED = 250  # Velocidad de movimiento en píxeles/segundo

# --- Apariencia ---
PLAYER_SIZE = 100  # Tamaño del sprite del jugador

# --- Salud y Defensa ---
PLAYER_BASE_HEALTH = 110      # Salud inicial del jugador
PLAYER_BASE_ARMOR = 0         # Armadura inicial
PLAYER_MAX_ARMOR = 100        # Capacidad máxima de armadura

# ===================================================
# ARMAS Y BALAS
# ===================================================

# --- Estadísticas base del arma ---
WEAPON_BASE_DAMAGE = 20           # Daño por bala
WEAPON_BASE_RPM = 600             # Disparos por minuto
WEAPON_BASE_MAGAZINE = 30         # Capacidad del cargador
WEAPON_BASE_RESERVE_AMMO = 120    # Munición de reserva
WEAPON_BASE_RELOAD_TIME = 1.5     # Tiempo de recarga en segundos
SPRITE_ANGLE_OFFSET = 45.0        # Offset para rotar sprites de armas y balas

# --- Proyectiles ---
WEAPON_BULLET_SPEED = 1200        # Velocidad de las balas en píxeles/segundo
BULLET_BASE_LIFETIME = 2.0        # Tiempo de vida de cada bala en segundos

# ===================================================
# SPAWNER - CONTROL DE OLAS Y GENERACIÓN DE ZOMBIES
# ===================================================

SPAWNER_TIME_BETWEEN_WAVES = 3.0
SPAWNER_SPAWN_INTERVAL = 0.5
SPAWNER_MIN_DISTANCE_TO_PLAYER = 450

# ===================================================
# ZOMBIES - ESTADÍSTICAS BASE POR TIPO
# ===================================================

# --- Zombie Común (Basic enemy) ---
ZOMBIE_COMMON_SPEED = 80          # Velocidad moderada
ZOMBIE_COMMON_SIZE = 100          # Tamaño estándar
ZOMBIE_COMMON_HP = 40             # Vida base (2-3 balas para matar)
ZOMBIE_COMMON_DAMAGE = 8          # Daño por segundo al jugador

# --- Zombie Rápido (Fast & Dangerous) ---
ZOMBIE_FAST_SPEED = 200           # Muy rápido
ZOMBIE_FAST_SIZE = 70             # Más pequeño
ZOMBIE_FAST_HP = 25               # Vida baja (1-2 balas)
ZOMBIE_FAST_DAMAGE = 12           # Daño medio-alto

# --- Zombie Tanque (Tank) ---
ZOMBIE_TANK_SPEED = 50            # Muy lento
ZOMBIE_TANK_SIZE = 180            # Muy grande
ZOMBIE_TANK_HP = 120              # Vida muy alta (6-7 balas)
ZOMBIE_TANK_DAMAGE = 25           # Daño alto

# --- Zombie Jefe (Boss) ---
ZOMBIE_BOSS_SPEED = 70            # Lento pero constante
ZOMBIE_BOSS_SIZE = 300            # Enorme
ZOMBIE_BOSS_HP = 400              # Vida extrema (20+ balas)
ZOMBIE_BOSS_DAMAGE = 40           # Daño devastador

# ===================================================
# SISTEMA DE NIVELES DE ZOMBIES (PROGRESIÓN POR OLA)
# ===================================================

# Nivel base de zombies en la primera ola
ZOMBIE_LEVEL_BASE_PER_WAVE = 1

# Incremento de nivel por cada ola completada
ZOMBIE_LEVEL_INCREMENT_PER_WAVE = 0.4  # Progresión gradual

# Variación aleatoria del nivel (para diversidad)
ZOMBIE_LEVEL_MIN_VARIATION = -1   # Puede ser 1 nivel menor
ZOMBIE_LEVEL_MAX_VARIATION = 2    # Puede ser hasta 2 niveles mayor

# ===================================================
# SISTEMA DE DETECCIÓN Y MOVIMIENTO
# ===================================================

# Radio de acción del zombie (para detectar al jugador)
ZOMBIE_DETECTION_RADIUS = 700  # píxeles

# Cooldown entre ataques (tiempo que tarda en infligir daño)
ZOMBIE_ATTACK_COOLDOWN = {
    "common": 1.0,
    "fast":   0.8,
    "tank":   1.5,
    "boss":   2.0
}

# Radio para alertar a otros zombies cercanos
ZOMBIE_ALERT_RADIUS = 300  # píxeles

# Vagabundeo aleatorio
ZOMBIE_WANDER_CHANGE_DIR_CHANCE = 0.01  # probabilidad de cambiar dirección por frame
ZOMBIE_WANDER_SPEED_MULT = 0.8         # multiplicador de velocidad al vagar

# Repulsión entre zombies (para no amontonarse)
ZOMBIE_REPULSION_RADIUS = 30
ZOMBIE_REPULSION_FORCE = 20

# Distancia mínima que un zombie debe mantener respecto al jugador
ZOMBIE_MIN_DISTANCE_TO_PLAYER = 30  # píxeles adicionales al radio del zombie

# Distancia mínima que el player debe mantener con los zombies (para no atravesarlos)
PLAYER_MIN_DISTANCE_TO_ZOMBIE = 5  # píxeles adicionales al radio del zombie

# ===================================================
# SISTEMA DE RAREZAS DE ZOMBIES
# ===================================================

# --- Probabilidades base de rareza (%) ---
# Nota: Estas se ajustan dinámicamente según la ola actual
ZOMBIE_RARITY_CHANCE = {
    "common": 55,      # Común (más frecuente en olas tempranas)
    "uncommon": 25,    # Poco común
    "rare": 12,        # Raro
    "epic": 6,         # Épico
    "legendary": 2     # Legendario (muy raro)
}

# --- Multiplicador de estadísticas según rareza ---
# Aplica a HP, velocidad y/o daño dependiendo del zombie
ZOMBIE_RARITY_MULT = {
    "common": 1.0,      # Sin bonus
    "uncommon": 1.3,    # +30% a stats seleccionados
    "rare": 1.6,        # +60%
    "epic": 2.2,        # +120%
    "legendary": 3.5    # +250% (muy peligrosos)
}

# --- Cantidad de estadísticas mejoradas por rareza ---
ZOMBIE_RARITY_UPGRADE_COUNT = {
    "common": 1,        # Mejora 1 stat
    "uncommon": 1,      # Mejora 1 stat
    "rare": 2,          # Mejora 2 stats
    "epic": 2,          # Mejora 2 stats
    "legendary": 3      # Mejora las 3 stats (HP, velocidad, daño)
}

# --- Multiplicador de puntos según rareza ---
ZOMBIE_RARITY_SCORE_MULT = {
    "common": 1.0,
    "uncommon": 1.5,
    "rare": 2.0,
    "epic": 3.0,
    "legendary": 5.0    # 5x puntos por legendarios
}

# --- Bonus de probabilidad de drop según rareza ---
# Se suma a la probabilidad base de dropear mejoras
ZOMBIE_RARITY_DROP_BONUS = {
    "common": 0,
    "uncommon": 5,      # +5% chance
    "rare": 12,         # +12% chance
    "epic": 25,         # +25% chance
    "legendary": 50     # +50% chance (casi garantizado)
}

ZOMBIE_LEVEL_UP_STATS = {
    "common": {"hp": 3,  "damage": 2,  "speed": 1.5},
    "fast":   {"hp": 2,  "damage": 1,  "speed": 4},
    "tank":   {"hp": 8,  "damage": 4, "speed": 0.8},
    "boss":   {"hp": 20, "damage": 10, "speed": 1},
}

# ===================================================
# cooldown de ataque de zombies
# ===================================================
ZOMBIE_ATTACK_COOLDOWN = {
    "common": 1.0,
    "fast":   0.8,
    "tank":   1.5,
    "boss":   2.0
}# segundos entre ataques


# ===================================================
# PROBABILIDADES DE SPAWN DE ZOMBIES POR TIPO Y OLA
# ===================================================

# Cada subdiccionario representa un rango de olas y las probabilidades base de cada tipo de zombie
ZOMBIE_SPAWN_CHANCE_BY_WAVE = {
    "1-5":   {"common": 1.0,   "fast": 0.0,   "tank": 0.0,   "boss": 0.0},   # solo comunes
    "6-7":   {"common": 0.7,   "fast": 0.3,   "tank": 0.0,   "boss": 0.0},   # agregamos fast
    "8-9":   {"common": 0.6,   "fast": 0.3,   "tank": 0.1,   "boss": 0.0},   # agregamos tank
    "10+":   {"common": 0.45,   "fast": 0.3,   "tank": 0.2,  "boss": 0.05}    # olas ≥10, multiplicador aplicado luego
}

# Multiplicadores para olas múltiplo de 10 (aumenta chance de bosses, tanks y fast)
SPAWNER_MULTIPLIER_WAVE_10 = {
    "boss": 5.5,    # +150% sobre la chance base
    "fast": 1.8,    # +50%
    "tank": 1.0,    # +50%
    "common": 0.5   # disminuye la chance de comunes
}


# ===================================================
# SISTEMA UNIFICADO DE DROPS DE MEJORAS
# ===================================================

# Sistema que determina:
# 1. Probabilidad de que dropee AL MENOS una carta
# 2. Cantidad mínima y máxima de cartas
# 3. Probabilidad de obtener cartas adicionales

ZOMBIE_UPGRADE_DROP_SYSTEM = {
    "common": {
        "base_chance": 65,       # 65% de dropear algo (generoso para mantener munición)
        "min_drops": 1,          # Mínimo 1 carta si dropea
        "max_drops": 2,          # Máximo 2 cartas
        "multi_drop_chance": 25  # 25% de que salga la 2da carta
    },
    "fast": {
        "base_chance": 75,       # 75% de drop
        "min_drops": 1,
        "max_drops": 3,
        "multi_drop_chance": 40  # 40% de cartas extra
    },
    "tank": {
        "base_chance": 90,       # 90% de drop (casi siempre)
        "min_drops": 2,          # Mínimo 2 cartas
        "max_drops": 4,
        "multi_drop_chance": 50  # 50% de cartas extra
    },
    "boss": {
        "base_chance": 100,      # 100% siempre dropea
        "min_drops": 5,          # Mínimo 5 cartas (recompensa generosa)
        "max_drops": 10,         # Máximo 10 cartas
        "multi_drop_chance": 70  # 70% de cartas extra
    }
}

# ===================================================
# MEJORAS (UPGRADES) - VALORES Y PROBABILIDADES
# ===================================================

# --- Tamaño visual ---
UPGRADE_ICON_SIZE = 72  # Tamaño del ícono en píxeles

# --- Valores que aporta cada mejora ---
UPGRADE_VALUES = {
    "vida": 25,          # +25 HP instantáneos
    "vida_extra": 15,    # +15 HP máximos (y actuales)
    "armadura": 20,      # +20 armadura
    "daño": 3,           # +3 daño por bala
    "cadencia": 10,      # +10 RPM (más disparos por minuto)
    "velocidad": 15,     # +15 píxeles/segundo de movimiento
    "balas": 25,         # +25 balas de reserva (CRÍTICO - valor alto)
    "cargador": 4        # +4 capacidad del cargador
}

# --- Probabilidad de spawn individual por tipo de upgrade ---
# Nota: Las balas tienen mayor probabilidad porque son CRÍTICAS para sobrevivir
UPGRADE_SPAWN_CHANCE = {
    "vida": 10,          # 10% - Curación inmediata
    "vida_extra": 90,     # 8% - Aumento permanente
    "armadura": 10,      # 10% - Defensa extra
    "daño": 1,          # 12% - Más daño por bala
    "cadencia": 12,      # 12% - Más disparos
    "velocidad": 8,      # 8% - Más movilidad
    "balas": 30,         # 30% - MÁS COMÚN (crítico para sobrevivir)
    "cargador": 10       # 10% - Más capacidad
}
# TOTAL: 100% (perfectamente balanceado)

# --- Física de caída de las mejoras ---
UPGRADE_FALL_SPEED = 150.0      # Velocidad inicial de caída (píxeles/segundo)
UPGRADE_FALL_DECAY = 0.95       # Factor de decaimiento por frame
UPGRADE_FALL_DURATION = 0.7     # Duración total de la animación (segundos)

# ===================================================
# PUNTUACIÓN
# ===================================================

# Puntos base otorgados al eliminar cada tipo de zombie
# (Se multiplica por el multiplicador de rareza)
ZOMBIE_SCORE_VALUES = {
    "common": 10,
    "fast": 20,
    "tank": 50,
    "boss": 300
}

# ===================================================
# RUTAS DE RECURSOS
# ===================================================

# Carpeta principal de imágenes
ASSETS_IMAGES = "assets/images"

# Carpeta principal de sonidos y música
ASSETS_SOUNDS = "assets/sounds"

# ===================================================
# NOTAS DE BALANCEO
# ===================================================

# 🎮 FILOSOFÍA DE DISEÑO:
#
# 1. MUNICIÓN ES CRÍTICA:
#    - Drop rate de "balas" es 30% (el más alto)
#    - Zombies comunes tienen 65% de dropear algo
#    - Reserva inicial: 120 balas + cargador de 30
#
# 2. PROGRESIÓN GRADUAL:
#    - Zombies aumentan ~0.4 niveles por ola
#    - Rarezas más altas aparecen gradualmente
#
# 3. RIESGO/RECOMPENSA:
#    - Zombies difíciles (tank/boss) dan más drops
#    - Rarezas altas tienen +50% chance de drop
#
# 4. BALANCE DE DAÑO:
#    - Zombie común: 40 HP ÷ 20 daño = 2 balas
#    - Zombie tank: 120 HP ÷ 20 daño = 6 balas
#    - Boss: 400 HP ÷ 20 daño = 20 balas
#
# 5. SUPERVIVENCIA:
#    - Player HP: 100
#    - Zombie común: 8 DPS → 12.5 segundos para morir
#    - Con armadura: +100 HP efectivo → 25 segundos