import random

from settings import (ZOMBIE_COMMON_DAMAGE, ZOMBIE_COMMON_HP, ZOMBIE_COMMON_SIZE, ZOMBIE_COMMON_SPEED,
                      ZOMBIE_FAST_DAMAGE, ZOMBIE_FAST_HP, ZOMBIE_FAST_SIZE, ZOMBIE_FAST_SPEED,
                      ZOMBIE_TANK_DAMAGE, ZOMBIE_TANK_HP, ZOMBIE_TANK_SIZE, ZOMBIE_TANK_SPEED,
                      ZOMBIE_BOSS_DAMAGE, ZOMBIE_BOSS_HP, ZOMBIE_BOSS_SIZE, ZOMBIE_BOSS_SPEED,
                      ZOMBIE_RARITY_MULT, ZOMBIE_RARITY_UPGRADE_COUNT, ZOMBIE_LEVEL_UP_STATS)

class ZombieStats:
    TYPE_STATS = {
        "common": {"hp": ZOMBIE_COMMON_HP, "speed": ZOMBIE_COMMON_SPEED, "radius": ZOMBIE_COMMON_SIZE//2, "damage": ZOMBIE_COMMON_DAMAGE},
        "fast":   {"hp": ZOMBIE_FAST_HP,   "speed": ZOMBIE_FAST_SPEED,   "radius": ZOMBIE_FAST_SIZE//2,   "damage": ZOMBIE_FAST_DAMAGE},
        "tank":   {"hp": ZOMBIE_TANK_HP,   "speed": ZOMBIE_TANK_SPEED,   "radius": ZOMBIE_TANK_SIZE//2,   "damage": ZOMBIE_TANK_DAMAGE},
        "boss":   {"hp": ZOMBIE_BOSS_HP,   "speed": ZOMBIE_BOSS_SPEED,   "radius": ZOMBIE_BOSS_SIZE//2,   "damage": ZOMBIE_BOSS_DAMAGE},
    }

    @staticmethod
    def build(type_name, level, rarity):
        base = ZombieStats.TYPE_STATS[type_name]
        hp = base["hp"]
        speed = base["speed"]
        dmg = base["damage"]
        radius = base["radius"]

        rarity_mult = ZOMBIE_RARITY_MULT.get(rarity, 1)
        n_upgrades = ZOMBIE_RARITY_UPGRADE_COUNT.get(rarity, 0)
        possible = ["hp","speed","damage"]
        chosen = random.sample(possible, n_upgrades)
        if "hp" in chosen: hp *= rarity_mult
        if "speed" in chosen: speed *= rarity_mult
        if "damage" in chosen: dmg *= rarity_mult

        if level > 1:
            lv = ZOMBIE_LEVEL_UP_STATS[type_name]
            hp += lv["hp"] * (level - 1)
            dmg += lv["damage"] * (level - 1)
            speed += lv["speed"] * (level - 1)

        return {"hp": hp, "speed": speed, "damage": dmg, "radius": radius}