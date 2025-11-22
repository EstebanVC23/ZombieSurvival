# core/tile.py
import pygame

class DecorTile(pygame.sprite.Sprite):
    def __init__(self, image, x, y, name):
        super().__init__()
        self.image = image
        self.name = name

        self.rect = self.image.get_rect(topleft=(x, y))

        # Objetos atravesables
        self.non_solid_types = ["flower", "bush", "grass_patch" ]

        self.solid = self.name not in self.non_solid_types

        if not self.solid:
            self.hitbox = None
        else:
            self.hitbox = self._generate_hitbox()

    # ============================================================
    # HITBOXES
    # ============================================================
    def _generate_hitbox(self):
        w, h = self.rect.size

        # --- Árboles: cualquier objeto que empiece con "tree_" ---
        if self.name.startswith("tree_"):
            hitbox_height = int(h * 0.30)              # Solo parte inferior (tronco)
            hitbox_width  = int(w * 0.40)              # Más estrecho horizontalmente
            hitbox_x = self.rect.x + (w - hitbox_width) // 2
            hitbox_y = self.rect.y + (h - hitbox_height)
            return pygame.Rect(hitbox_x, hitbox_y, hitbox_width, hitbox_height)

        # --- Cactus ---
        if "cactus" in self.name:
            return self.rect.inflate(-w * 0.20, -h * 0.20)

        # --- Rocas ---
        if "rock" in self.name:
            return self.rect.inflate(-w * 0.35, -h * 0.35)

        # --- Default para otros sólidos ---
        return self.rect.inflate(-w * 0.25, -h * 0.25)


    # ============================================================
    # Mantener la actualización del tronco (solo para árboles)
    # ============================================================
    def update_hitbox(self):
        if self.hitbox:
            if self.name.startswith("tree"):
                w, h = self.rect.size
                hitbox_height = int(h * 0.30)
                hitbox_y = self.rect.y + (h - hitbox_height)

                hitbox_width = int(w * 0.35)
                hitbox_x = self.rect.x + (w - hitbox_width) // 2

                self.hitbox.update(hitbox_x, hitbox_y, hitbox_width, hitbox_height)
            else:
                self.hitbox.topleft = self.rect.topleft
