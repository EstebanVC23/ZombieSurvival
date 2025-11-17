# core/rarity.py
import random
from typing import List, Tuple
from settings import (
    ZOMBIE_RARITY_CHANCE,
    ZOMBIE_RARITY_MULT,
    ZOMBIE_RARITY_UPGRADE_COUNT,
    ZOMBIE_RARITY_SCORE_MULT,
    ZOMBIE_RARITY_DROP_BONUS,
)

# Rarity helpers that centralize behavior and keep settings as single source of truth.

RARITY_TABLE: List[Tuple[str, float]] = [
    ("common", ZOMBIE_RARITY_CHANCE["common"]),
    ("uncommon", ZOMBIE_RARITY_CHANCE["uncommon"]),
    ("rare", ZOMBIE_RARITY_CHANCE["rare"]),
    ("epic", ZOMBIE_RARITY_CHANCE["epic"]),
    ("legendary", ZOMBIE_RARITY_CHANCE["legendary"]),
]


def roll_rarity() -> str:
    """Tira la rareza usando ZOMBIE_RARITY_CHANCE desde settings."""
    r = random.random() * 100
    cumulative = 0.0
    for name, chance in RARITY_TABLE:
        cumulative += chance
        if r <= cumulative:
            return name
    return "common"


def get_rarity_multiplier(rarity: str) -> float:
    """Retorna el multiplicador de stat para una rareza (ZOMBIE_RARITY_MULT)."""
    return float(ZOMBIE_RARITY_MULT.get(rarity, 1.0))


def get_upgrade_count(rarity: str) -> int:
    return int(ZOMBIE_RARITY_UPGRADE_COUNT.get(rarity, 0))


def get_score_mult(rarity: str) -> float:
    return float(ZOMBIE_RARITY_SCORE_MULT.get(rarity, 1.0))


def get_drop_bonus(rarity: str) -> float:
    return float(ZOMBIE_RARITY_DROP_BONUS.get(rarity, 0.0))
