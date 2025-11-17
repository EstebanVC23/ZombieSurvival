# entities/health.py
"""
HealthComponent compatible con el HUD y con el código refactorizado.
Provee:
 - current_health, max_health (floats)
 - take_damage(amount) -> bool (retorna True si murió por ese daño)
 - heal(amount)
 - is_dead() -> bool
 - percent() -> float  (0.0 - 1.0)
 - get_health_percent() -> float  (alias, compatibilidad)
"""

from __future__ import annotations


class HealthComponent:
    def __init__(self, max_health: float):
        self.max_health = float(max_health)
        self.current_health = float(max_health)
        self.dead = False

    # -----------------------
    # Daño / curación
    # -----------------------
    def take_damage(self, amount: float) -> bool:
        """
        Resta vida y retorna True si la entidad murió por este daño.
        Si ya estaba muerta retorna False.
        """
        if self.dead:
            return False

        try:
            amt = float(amount)
        except Exception:
            amt = 0.0

        self.current_health -= amt
        if self.current_health <= 0.0:
            self.current_health = 0.0
            self.dead = True
            return True
        return False

    def heal(self, amount: float):
        """
        Suma vida sin pasar el máximo. No revive si está dead.
        """
        if self.dead:
            return
        try:
            amt = float(amount)
        except Exception:
            return
        self.current_health = min(self.max_health, self.current_health + amt)

    # -----------------------
    # Consultas
    # -----------------------
    def is_dead(self) -> bool:
        return bool(self.dead)

    def percent(self) -> float:
        """
        Retorna el porcentaje de vida actual (0.0 - 1.0).
        """
        if self.max_health <= 0:
            return 0.0
        return max(0.0, min(1.0, self.current_health / self.max_health))

    # -----------------------
    # Compatibilidad con HUD
    # -----------------------
    def get_health_percent(self) -> float:
        """
        Alias para compatibilidad (el HUD usa este nombre).
        """
        return self.percent()

    # -----------------------
    # Representación (útil para debug)
    # -----------------------
    def __repr__(self):
        return f"<HealthComponent {self.current_health:.1f}/{self.max_health:.1f} dead={self.dead}>"
