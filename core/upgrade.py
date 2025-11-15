import pygame, os, random, math
from settings import (
    ASSETS_IMAGES,
    UPGRADE_ICON_SIZE,
    UPGRADE_SPAWN_CHANCE,
    UPGRADE_FALL_SPEED,
    UPGRADE_FALL_DECAY,
    UPGRADE_FALL_DURATION,
    ZOMBIE_UPGRADE_MULTIPLIERS,
)
from utils.helpers import load_image_safe


class Upgrade(pygame.sprite.Sprite):
    def __init__(self, upgrade_type, pos):
        super().__init__()
        self.type = upgrade_type
        self.image = self.load_icon(upgrade_type)
        self.rect = self.image.get_rect(center=pos)
        self.pos = pygame.Vector2(pos)

        # Movimiento de caída (animación física)
        self.fall_timer = 0.0
        self.fall_speed = 0.0
        self.fall_angle = 0.0
        self.fall_distance = 0.0
        self.active_fall = False
    
    @property
    def x(self):
        return self.pos.x

    @property
    def y(self):
        return self.pos.y


    # ==========================================================
    # 🔹 Cargar ícono y limpiar fondo blanco o gris
    # ==========================================================
    def load_icon(self, upgrade_type):
        path = os.path.join("upgrades", f"{upgrade_type}.png")
        img = load_image_safe(path)

        if img:
            img = pygame.transform.scale(img, (UPGRADE_ICON_SIZE, UPGRADE_ICON_SIZE))
            img = self.clean_image(img)  # 🔹 limpiar fondo
            print(f"[DEBUG] Imagen de mejora '{upgrade_type}' cargada y limpiada ({path}).")
            return img
        else:
            print(f"[WARN] Fondo de card no encontrado, usando superficie básica.")
            surf = pygame.Surface((UPGRADE_ICON_SIZE, UPGRADE_ICON_SIZE), pygame.SRCALPHA)
            pygame.draw.rect(surf, (255, 255, 255), surf.get_rect(), border_radius=12)
            return surf

    # ==========================================================
    # 🔹 Limpieza de fondo blanco o gris claro
    # ==========================================================
    def clean_image(self, img):
        """Elimina fondos blancos o grises claros, dejando solo el icono."""
        img = img.convert_alpha()
        clean = pygame.Surface(img.get_size(), pygame.SRCALPHA)
        img.lock()
        for x in range(img.get_width()):
            for y in range(img.get_height()):
                r, g, b, a = img.get_at((x, y))
                brightness = (r + g + b) / 3
                # Quitar blancos o grises claros
                if brightness > 200 or a < 80:
                    img.set_at((x, y), (0, 0, 0, 0))
        img.unlock()
        clean.blit(img, (0, 0))
        return clean

    # ==========================================================
    # 🔹 Iniciar animación de caída
    # ==========================================================
    def start_fall(self, angle_rad, speed, max_distance):
        """Configura la dirección y velocidad de caída visual."""
        self.fall_angle = angle_rad
        self.fall_speed = speed
        self.fall_distance = max_distance
        self.fall_timer = 0.0
        self.active_fall = True

    # ==========================================================
    # 🔹 Actualización general
    # ==========================================================
    def update(self, dt, game=None):
        """Actualiza animación de caída y posición."""
        if self.active_fall:
            self.fall_timer += dt
            if self.fall_timer < UPGRADE_FALL_DURATION:
                decay_factor = math.pow(UPGRADE_FALL_DECAY, self.fall_timer * 60)
                dx = math.cos(self.fall_angle) * self.fall_speed * dt * decay_factor
                dy = math.sin(self.fall_angle) * self.fall_speed * dt * decay_factor
                self.pos.x += dx
                self.pos.y += dy
                self.rect.center = self.pos
            else:
                self.active_fall = False

    # ==========================================================
    # 🔹 Generar upgrade desde un zombie (controlado por settings)
    # ==========================================================
    @staticmethod
    def spawn_from_zombie(group, zombie):
        """
        Genera upgrades al morir un zombie, según las probabilidades definidas:
        - ZOMBIE_UPGRADE_MULTIPLIERS[zombie.type] → probabilidad base de caída.
        - 0.0 = nada, 0.5 = 50%, 1.0 = siempre cae una.
        - >1.0 = garantizadas + probabilidad de más (ej: 2.7 = 2 seguras + 70% de una 3ra).
        """
        multiplier = ZOMBIE_UPGRADE_MULTIPLIERS.get(zombie.type, 0.0)
        if multiplier <= 0.0:
            return

        origin = zombie.rect.center if hasattr(zombie, "rect") else tuple(zombie.pos)

        # 🔹 Determinar cuántas cartas dejará caer
        guaranteed = int(multiplier)
        extra_prob = multiplier - guaranteed
        total_drops = guaranteed + (1 if random.random() < extra_prob else 0)

        # Posibilidad de fallar completamente si <1.0
        if total_drops == 0 and random.random() > multiplier:
            return

        print(f"[DEBUG] {zombie.type} soltará {total_drops} carta(s) (prob={multiplier:.2f})")

        # 🔹 Generar cada carta
        for i in range(total_drops):
            upgrade_type = Upgrade.select_random_upgrade()
            if upgrade_type:
                u = Upgrade(upgrade_type, origin)

                # dispersión visual radial controlada
                angle = random.uniform(0, 2 * math.pi) + (i * (2 * math.pi / max(1, total_drops)))
                speed = random.uniform(UPGRADE_FALL_SPEED * 0.5, UPGRADE_FALL_SPEED * 0.9)
                distance = random.uniform(40, 75)
                u.start_fall(angle_rad=angle, speed=speed, max_distance=distance)

                group.add(u)
                print(f"[DEBUG] Drop '{upgrade_type}' desde {zombie.type}")
        return

    # ==========================================================
    # 🔹 Selección ponderada del tipo de mejora
    # ==========================================================
    @staticmethod
    def select_random_upgrade():
        """Selecciona un tipo de mejora en función de sus probabilidades."""
        total = sum(UPGRADE_SPAWN_CHANCE.values())
        roll = random.uniform(0, total)
        current = 0.0
        for name, chance in UPGRADE_SPAWN_CHANCE.items():
            current += chance
            if roll <= current:
                return name
        return None
