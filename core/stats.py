# core/stats.py
from typing import Dict
from core.particles import get_rarity_multiplier


class StatBlock:
    """
    Contenedor reutilizable para estadísticas (hp, damage, speed, radius, etc.)
    - Permite aplicar multiplicadores por rareza.
    - Permite aplicar incrementos por nivel.
    """

    def __init__(self, base: Dict[str, float], rarity: str = "common"):
        # base: dict con keys como "hp","damage","speed","radius"
        self.base = base.copy()
        self.rarity = rarity
        self.effective = base.copy()
        self.apply_rarity(rarity)

    def apply_rarity(self, rarity: str):
        mult = get_rarity_multiplier(rarity)
        # Solo aplica a stats relevantes (hp,damage,speed) - si no existen, se ignoran
        for k, v in self.base.items():
            if k in ("hp", "damage", "speed"):
                self.effective[k] = v * mult
            else:
                self.effective[k] = v

    def apply_level_increase(self, level_increase: Dict[str, float], level: int):
        """Aplica incremento por (level - 1) según un dict de incrementos por nivel."""
        if level <= 1:
            return
        levels = level - 1
        for stat, inc in level_increase.items():
            if stat in self.effective:
                self.effective[stat] = self.effective[stat] + inc * levels

    def get(self, stat_name: str, fallback=0.0):
        return float(self.effective.get(stat_name, fallback))

    def set(self, stat_name: str, value: float):
        self.effective[stat_name] = value
