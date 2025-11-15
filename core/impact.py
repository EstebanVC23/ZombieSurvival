import pygame
from utils.helpers import load_image_safe, clean_image_background, load_sound

class Impact(pygame.sprite.Sprite):
    def __init__(self,pos,size=(50,50)):
        super().__init__()
        image = load_image_safe("weapons/impact.png")
        if image:
            image = clean_image_background(pygame.transform.scale(image,size))
            self.image=image
        else:
            print("[DEBUG] Placeholder para impacto")
            self.image=pygame.Surface(size,pygame.SRCALPHA)
            pygame.draw.circle(self.image,(255,180,50),(size[0]//2,size[1]//2),size[0]//2)
        self.rect=self.image.get_rect(center=pos)
        self.timer=0.0
        self.duration=0.25
        self.alpha=255

        # Sonido de impacto
        self.sound = load_sound("impact.mp3", volume=0.4)
        if self.sound:
            try:
                ch = pygame.mixer.find_channel(True)
                ch.play(self.sound, maxtime=int(0.5*1000))
            except Exception: pass

    def update(self, dt):
        self.timer+=dt
        if self.timer>self.duration: self.kill()
        else:
            self.alpha=max(0,255*(1-self.timer/self.duration))
            self.image.set_alpha(self.alpha)
