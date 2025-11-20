from utils.sound_utils import load_sound, SoundUtils #no deberia importar loud_sound de de sound_utils, es de helpers. arreglalo
from settings import ZOMBIE_DETECTION_RADIUS

class ZombieSound:
    def __init__(self, zombie):
        self.sound = load_sound("zombie_common.mp3", volume=0.0)
        self.zombie = zombie
        self.max_dist = ZOMBIE_DETECTION_RADIUS
        if self.sound:
            try: self.sound.play(loops=-1)
            except: pass

    def update_volume(self, player_pos):
        if not self.sound: return
        dist = self.zombie.pos.distance_to(player_pos)
        SoundUtils.apply_distance_volume(self.sound, dist, self.max_dist)

    def stop(self):
        if self.sound:
            try: self.sound.stop()
            except: pass