import math
import random
import pygame
from settings import (
    WORLD_WIDTH,
    WORLD_HEIGHT,
    ZOMBIE_MIN_DISTANCE_TO_PLAYER,
    ZOMBIE_REPULSION_RADIUS,
    ZOMBIE_REPULSION_FORCE,
    ZOMBIE_WANDER_CHANGE_DIR_CHANCE,
    ZOMBIE_WANDER_SPEED_MULT)

class ZombieAI:

    # ================================
    # Elegir dirección (como siempre)
    # ================================
    @staticmethod
    def choose_direction_from_vector(vec):
        if vec.length() == 0:
            return "front"

        angle = math.degrees(math.atan2(vec.y, vec.x))

        if -45 <= angle < 45:
            return "right"     # mirando a la derecha
        elif 45 <= angle < 135:
            return "down"      # mirando abajo (front)
        elif -135 <= angle < -45:
            return "up"        # mirando arriba (back)
        else:
            return "left"      # mirando izquierda

    # ======================================================
    # ANTI-CAMPING
    # Si el jugador está quieto frente al zombie → flanqueo
    # ======================================================
    @staticmethod
    def apply_anti_camping(zombie, move_dir, player):
        if not hasattr(player, "vel"):
            return move_dir

        # si jugador casi no se mueve → está campeando
        if player.vel.length() < 0.2:

            # zombie flanquea lateralmente según su dirección actual
            perp = pygame.Vector2(-move_dir.y, move_dir.x)
            strength = 0.35  # ajuste suave
            return (move_dir + perp * strength).normalize()

        return move_dir

    # ======================================================
    # ANTI-KITE
    # Si el jugador está retrocediendo mientras dispara
    # ======================================================
    @staticmethod
    def apply_anti_kite(zombie, move_dir, player):
        if not hasattr(player, "vel"):
            return move_dir

        # si el jugador se mueve en dirección opuesta al zombie → kite
        to_player = (player.pos - zombie.pos).normalize()
        player_dir = player.vel.normalize() if player.vel.length() > 0 else pygame.Vector2()

        dot = to_player.dot(player_dir)

        if dot < -0.6:   # jugador se mueve hacia atrás
            # zombie intenta cerrar ángulo
            side = pygame.Vector2(-to_player.y, to_player.x)
            return (move_dir + side * 0.25).normalize()

        return move_dir

    # ======================================================
    # COORDINACIÓN MÍNIMA
    # Zombies cercanos ajustan su ángulo común
    # ======================================================
    @staticmethod
    def apply_min_coordination(zombie, move_dir, all_zombies):
        if not all_zombies:
            return move_dir

        avg = pygame.Vector2()
        count = 0

        for other in all_zombies:
            if other == zombie or other.dead:
                continue
            if zombie.pos.distance_to(other.pos) < 220:
                avg += (other.pos - zombie.pos).normalize()
                count += 1

        if count == 0:
            return move_dir

        avg /= count
        return (move_dir * 0.7 + avg * 0.3).normalize()

    # ======================================================
    # PERSECUCIÓN PRINCIPAL (simple pero difícil)
    # ======================================================
    @staticmethod
    def move_towards(zombie, target_pos, dt, all_zombies=None):
        move_vec = target_pos - zombie.pos
        dist_to_player = move_vec.length()

        # distancia mínima para no atravesar
        min_dist = zombie.radius + ZOMBIE_MIN_DISTANCE_TO_PLAYER
        if hasattr(zombie, 'target_player') and zombie.target_player:
            min_dist += zombie.target_player.radius

        # si muy cerca → no avanzar
        if dist_to_player <= min_dist:
            return

        # dirección cruda hacia el jugador
        move_dir = move_vec.normalize()

        # ==========================
        # ANTI-CAMPING
        # ==========================
        move_dir = ZombieAI.apply_anti_camping(zombie, move_dir, zombie.target_player)

        # ==========================
        # ANTI-KITE
        # ==========================
        move_dir = ZombieAI.apply_anti_kite(zombie, move_dir, zombie.target_player)

        # ==========================
        # REPULSIONES
        # ==========================
        if all_zombies:
            for other in all_zombies:
                if other == zombie or other.dead:
                    continue

                diff = zombie.pos - other.pos
                d = diff.length()

                if 0 < d < ZOMBIE_REPULSION_RADIUS:
                    move_dir += diff.normalize() * (ZOMBIE_REPULSION_FORCE / d)

        # ==========================
        # COORDINACIÓN DE HORDAS
        # ==========================
        move_dir = ZombieAI.apply_min_coordination(zombie, move_dir, all_zombies)

        move_dir = move_dir.normalize()

        # ==========================
        # MOVER
        # ==========================
        zombie.pos += move_dir * zombie.speed * dt
        zombie.rect.center = (round(zombie.pos.x), round(zombie.pos.y))

        # ==========================
        # DIRECCIÓN / ANIMACIÓN
        # ==========================
        dir_key = ZombieAI.choose_direction_from_vector(move_vec)
        zombie.direction = {
            "up": "back",
            "down": "front",
            "left": "left",
            "right": "right"
        }.get(dir_key, "front")

        zombie.image = zombie.sprites.get_frame(zombie.direction)

    # ======================================================
    # WANDER (más lento, delimitado por bordes)
    # ======================================================
    @staticmethod
    def wander(zombie, dt):

        if (not hasattr(zombie, "_wander_dir")
            or random.random() < ZOMBIE_WANDER_CHANGE_DIR_CHANCE):

            angle = random.uniform(0, 2 * math.pi)
            zombie._wander_dir = pygame.Vector2(math.cos(angle), math.sin(angle))

        # velocidad reducida (ya usas constante)
        zombie.pos += zombie._wander_dir * zombie.speed * dt * ZOMBIE_WANDER_SPEED_MULT

        # bordes
        bounced = False

        if zombie.pos.x < 0:
            zombie.pos.x = 0
            bounced = True
        elif zombie.pos.x > WORLD_WIDTH:
            zombie.pos.x = WORLD_WIDTH
            bounced = True

        if zombie.pos.y < 0:
            zombie.pos.y = 0
            bounced = True
        elif zombie.pos.y > WORLD_HEIGHT:
            zombie.pos.y = WORLD_HEIGHT
            bounced = True

        if bounced:
            angle = random.uniform(0, 2 * math.pi)
            zombie._wander_dir = pygame.Vector2(math.cos(angle), math.sin(angle))

        zombie.rect.center = (round(zombie.pos.x), round(zombie.pos.y))

        dir_key = ZombieAI.choose_direction_from_vector(zombie._wander_dir)
        zombie.direction = {
            "up": "back",
            "down": "front",
            "left": "left",
            "right": "right"
        }.get(dir_key, "front")

        zombie.image = zombie.sprites.get_frame(zombie.direction)
