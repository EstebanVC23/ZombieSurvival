
from settings import (PLAYER_BASE_HEALTH, PLAYER_BASE_ARMOR,
                      PLAYER_MAX_ARMOR, UPGRADE_VALUES)

class PlayerStats:
    """Manejo de salud, shield, upgrades y puntuación."""

    def __init__(self):
        self.health = PLAYER_BASE_HEALTH
        self.max_health = PLAYER_BASE_HEALTH
        self.shield = PLAYER_BASE_ARMOR
        self.max_shield = PLAYER_MAX_ARMOR
        self.score = 0

    def take_damage(self, amount):
        if self.shield > 0:
            self.shield -= amount
            if self.shield < 0:
                self.health -= -self.shield
                self.shield = 0
        else:
            self.health -= amount
        self.health = max(0, self.health)

    def apply_upgrade(self, up, weapon):
        val = UPGRADE_VALUES.get(up, 0)
        if up == "vida":
            self.health = min(self.max_health, self.health + val)
        elif up == "vida_extra":
            self.max_health += val
            self.health += val
        elif up == "armadura":
            self.shield = min(self.max_shield, self.shield + val)
        elif up == "velocidad":
            return val
        elif up == "balas":
            weapon.reserve_ammo += val
        elif up == "cargador":
            weapon.max_ammo += val
            weapon.current_ammo = weapon.max_ammo
        elif up == "cadencia":
            weapon.apply_fire_rate_bonus(val)
        elif up == "daño":
            weapon.apply_damage_bonus(val)