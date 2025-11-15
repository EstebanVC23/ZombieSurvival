import pygame
import os
from settings import *
from utils.helpers import load_image_safe, clean_image_background, load_sound
from core.upgrade import Upgrade

class Zombie(pygame.sprite.Sprite):
    TYPE_STATS = {
        "common": {"hp": ZOMBIE_COMMON_HP, "speed": ZOMBIE_COMMON_SPEED, "radius": ZOMBIE_COMMON_SIZE // 2, "damage": ZOMBIE_COMMON_DAMAGE},
        "fast":   {"hp": ZOMBIE_FAST_HP, "speed": ZOMBIE_FAST_SPEED, "radius": ZOMBIE_FAST_SIZE // 2, "damage": ZOMBIE_FAST_DAMAGE},
        "tank":   {"hp": ZOMBIE_TANK_HP, "speed": ZOMBIE_TANK_SPEED, "radius": ZOMBIE_TANK_SIZE // 2, "damage": ZOMBIE_TANK_DAMAGE},
        "boss":   {"hp": ZOMBIE_BOSS_HP, "speed": ZOMBIE_BOSS_SPEED, "radius": ZOMBIE_BOSS_SIZE // 2, "damage": ZOMBIE_BOSS_DAMAGE},
    }

    def __init__(self, pos, ztype="common"):
        super().__init__()
        stats = self.TYPE_STATS.get(ztype, self.TYPE_STATS["common"])
        self.type = ztype
        self.hp = stats["hp"]
        self.speed = stats["speed"]
        self.radius = stats["radius"]
        self.damage = stats["damage"]
        self.direction = "front"
        self.pos = pygame.Vector2(pos)
        self.dead = False
        self.dead_timer = 0.0
        self.fade = 0.0
        self.dead_image = None

        # Imagen base placeholder
        self.image = pygame.Surface((self.radius*2, self.radius*2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (150,180,40), (self.radius,self.radius), self.radius)
        self.rect = self.image.get_rect(center=(round(self.pos.x), round(self.pos.y)))

        # Sprites vivo
        base = os.path.join("zombie","common")
        f = load_image_safe(os.path.join(base, "common_frente.png"))
        b = load_image_safe(os.path.join(base, "common_espalda.png"))
        s = load_image_safe(os.path.join(base, "common_lateral.png"))
        self.frames = {}
        if f and b and s:
            self.frames["front"] = clean_image_background(pygame.transform.scale(f,(self.radius*2,self.radius*2)))
            self.frames["back"] = clean_image_background(pygame.transform.scale(b,(self.radius*2,self.radius*2)))
            self.frames["left"] = clean_image_background(pygame.transform.scale(s,(self.radius*2,self.radius*2)))
            self.frames["right"] = pygame.transform.flip(self.frames["left"], True, False)
            self.image = self.frames["front"]

        # Sprite de muerte
        raw_dead = load_image_safe(os.path.join(base,"dead.png"))
        self.dead_sprite = clean_image_background(pygame.transform.scale(raw_dead,(self.radius*2,self.radius*2))) if raw_dead else None

        # Sonido
        self.sound = load_sound("zombie_common.mp3", volume=0.0)
        if self.sound: self.sound.play(loops=-1)
        self.max_sound_distance = max(600,(WORLD_WIDTH+WORLD_HEIGHT)/10)

    @property
    def x(self): return self.pos.x
    @property
    def y(self): return self.pos.y

    def update(self, dt, game):
        if self.dead:
            self.dead_timer += dt
            self._show_death_sprite(dt)
            if self.sound:
                self.sound.set_volume(0.0)
            if self.dead_timer >= 4.0:
                self.kill()
            return
        if not game.player: return
        if getattr(game,"paused",False):
            if self.sound: self.sound.stop()
            return
        if self.sound and self.sound.get_num_channels() == 0:
            self.sound.play(loops=-1)

        # Movimiento hacia jugador
        dir_vec = game.player.pos - self.pos
        if dir_vec.length_squared() > 0:
            d = dir_vec.normalize()
            self.pos += d*self.speed*dt
            self.rect.center = (round(self.pos.x), round(self.pos.y))
            self._set_dir(d)
        if self.frames:
            self.image = self.frames[self.direction]

        # Colisión jugador
        try:
            if pygame.sprite.collide_circle(self, game.player):
                game.player.take_damage(self.damage*dt)
        except Exception: pass

        # Volumen por proximidad
        if self.sound:
            dist = self.pos.distance_to(game.player.pos)
            vol = max(0.0, min(1.0,(1-(dist/self.max_sound_distance))**2)) if dist<self.max_sound_distance else 0.0
            try: self.sound.set_volume(vol)
            except Exception: pass

    def take_damage(self, dmg, game=None):
        if self.dead: return
        self.hp -= dmg
        if self.hp>0: return
        if self.sound:
            try: self.sound.stop()
            except Exception: pass
        if game:
            try: Upgrade.spawn_from_zombie(game.upgrades,self)
            except Exception: pass
        self.dead=True
        self.dead_timer=0.0
        self.fade=0.0
        if self.dead_sprite:
            if self.direction=="front": rotated=self.dead_sprite
            elif self.direction=="back": rotated=pygame.transform.rotate(self.dead_sprite,180)
            elif self.direction=="left": rotated=pygame.transform.rotate(self.dead_sprite,-90)
            elif self.direction=="right": rotated=pygame.transform.rotate(self.dead_sprite,90)
            else: rotated=self.dead_sprite
        else: rotated=self.image.copy()
        self.dead_image=rotated
        self.radius=1
        self.damage=0

    # Métodos auxiliares
    def _set_dir(self,v):
        dx,dy=v.x,v.y
        if abs(dx)>abs(dy): self.direction="right" if dx>0 else "left"
        else: self.direction="front" if dy>0 else "back"

    def _show_death_sprite(self, dt):
        if not self.dead_image: return
        if self.fade<255: self.fade += 400*dt
        if self.fade>255: self.fade=255
        corpse=self.dead_image.copy()
        corpse.set_alpha(int(self.fade))
        self.image=corpse
        self.rect=self.image.get_rect(center=(round(self.pos.x), round(self.pos.y)))
