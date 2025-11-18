#no influye en nada el funcionamiento del código


import pygame
import random
import math


# ============================================================
#  BASE: PARTICLE
# ============================================================

class Particle(pygame.sprite.Sprite):
    """
    Partícula individual con:
    - posición
    - velocidad
    - gravedad
    - fricción
    - decaimiento alfa
    """

    def __init__(self, pos, vel, radius, color, lifetime, gravity=0, friction=1.0):
        super().__init__()
        self.pos = pygame.Vector2(pos)
        self.vel = pygame.Vector2(vel)
        self.radius = radius
        self.color = color
        self.lifetime = lifetime
        self.gravity = gravity
        self.friction = friction
        self.age = 0

        self.image = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, color, (radius, radius), radius)
        self.rect = self.image.get_rect(center=self.pos)

    def update(self, dt):
        self.age += dt
        if self.age >= self.lifetime:
            self.kill()
            return

        # física
        self.vel.y += self.gravity * dt
        self.vel *= self.friction
        self.pos += self.vel * dt

        # fade-out
        alpha = max(0, 255 * (1 - self.age / self.lifetime))
        self.image.set_alpha(alpha)
        self.rect.center = self.pos


# ============================================================
#  BASE: PARTICLE EMITTER
# ============================================================

class ParticleEmitter(pygame.sprite.Sprite):
    """
    Sistema que genera partículas durante un tiempo.
    Ideal para explosiones, sangre, humo, etc.
    """

    def __init__(self, pos, emit_time=0.1, rate=40, **particle_kwargs):
        super().__init__()
        self.pos = pygame.Vector2(pos)
        self.emit_time = emit_time
        self.rate = rate
        self.timer = 0
        self.alive_timer = 0
        self.kwargs = particle_kwargs

        self.image = pygame.Surface((1,1), pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=self.pos)

    def spawn_particle(self):
        vel = (
            random.uniform(-80, 80),
            random.uniform(-80, 80)
        )

        particle = Particle(
            pos=self.pos,
            vel=vel,
            **self.kwargs
        )
        return particle

    def update(self, dt):
        self.alive_timer += dt

        # Ya dejó de emitir → eliminar
        if self.alive_timer >= self.emit_time:
            self.kill()
            return

        # Emisión constante
        self.timer += dt
        while self.timer >= 1 / self.rate:
            self.timer -= 1 / self.rate
            p = self.spawn_particle()
            if hasattr(self, "group") and self.group:
                self.group.add(p)


# ============================================================
#  EFECTO: SANGRE (partículas redondas)
# ============================================================

class BloodParticle(Particle):
    def __init__(self, pos):
        angle = random.uniform(0, math.tau)
        speed = random.uniform(60, 140)

        vel = (math.cos(angle) * speed, math.sin(angle) * speed)

        color = (180 + random.randint(-20, 20),
                 20 + random.randint(-10, 10),
                 20 + random.randint(-10, 10))

        super().__init__(
            pos=pos,
            vel=vel,
            radius=random.randint(2, 4),
            color=color,
            lifetime=random.uniform(0.4, 0.8),
            gravity=200,
            friction=0.92
        )


class BloodSplash(pygame.sprite.Sprite):
    """Chorro de sangre más fuerte."""
    def __init__(self, pos, count=18):
        super().__init__()
        self.image = pygame.Surface((1,1), pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=pos)
        self.particles = []

        for _ in range(count):
            p = BloodParticle(pos)
            self.particles.append(p)

    def update(self, dt):
        for p in self.particles:
            p.update(dt)
            if not p.alive():
                self.particles.remove(p)

        if not self.particles:
            self.kill()

    def draw(self, surface, camera):
        for p in self.particles:
            surface.blit(p.image, camera.apply(p.rect))


# ============================================================
#  EFECTO: CHISPAS (impacto de bala)
# ============================================================

class HitSpark(Particle):
    def __init__(self, pos, direction):
        angle = math.atan2(direction.y, direction.x)
        angle += random.uniform(-0.5, 0.5)
        speed = random.uniform(150, 260)

        vel = (math.cos(angle) * speed, math.sin(angle) * speed)

        super().__init__(
            pos=pos,
            vel=vel,
            radius=2,
            color=(255, 210, 80),
            lifetime=0.2,
            gravity=0,
            friction=0.85
        )


# ============================================================
#  EFECTO: POLVO / IMPACTO CONTRA PISO
# ============================================================

class DustImpact(Particle):
    def __init__(self, pos):
        angle = random.uniform(0, math.tau)
        speed = random.uniform(30, 80)

        vel = (math.cos(angle) * speed, math.sin(angle) * speed)

        super().__init__(
            pos=pos,
            vel=vel,
            radius=3,
            color=(200, 200, 200),
            lifetime=0.3,
            gravity=30,
            friction=0.88
        )
