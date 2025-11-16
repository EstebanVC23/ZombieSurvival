import pygame
import math
from ui.map import MiniMap

class HUD:
    """HUD principal con barra de vida, shield, ammo y minimapa."""

    def __init__(self, font):
        self.font = font
        self.minimap = None

    def _ensure_minimap(self, wave_manager):
        if self.minimap is None:
            game = getattr(wave_manager, "game", None)
            if game:
                self.minimap = MiniMap(game=game, width=180, height=180, margin=8,
                                       position="topright", update_interval_ms=100)

    def draw(self, surface, player, wave_manager):
        # Barra de vida del jugador
        max_hp = getattr(player, "max_health", 100)
        bar_width, bar_height = 250, 18
        x, y = 30, 30
        hp_ratio = max(0, player.health / max_hp)
        pygame.draw.rect(surface, (0, 0, 0), (x-3, y-3, bar_width+6, bar_height+6))
        pygame.draw.rect(surface, (40, 40, 40), (x, y, bar_width, bar_height))
        hp_color = (200, 50, 50) if hp_ratio < 0.3 else (255, 180, 50) if hp_ratio < 0.6 else (50, 200, 80)
        pygame.draw.rect(surface, hp_color, (x, y, int(bar_width*hp_ratio), bar_height))
        hp_text = self.font.render(f"HP {int(player.health)}/{int(max_hp)}", True, (255, 255, 255))
        surface.blit(hp_text, (x + 260, y-2))

        # Barra de shield
        max_shield = getattr(player, "max_shield", 0)
        if max_shield > 0:
            shield_ratio = max(0, player.shield / max_shield)
            shield_y = y + 32
            pygame.draw.rect(surface, (0, 0, 0), (x-3, shield_y-3, bar_width+6, bar_height+6))
            pygame.draw.rect(surface, (40, 40, 60), (x, shield_y, bar_width, bar_height))
            shield_color = (80, 80, 255) if shield_ratio > 0.3 else (120, 120, 255)
            pygame.draw.rect(surface, shield_color, (x, shield_y, int(bar_width*shield_ratio), bar_height))
            shield_text = self.font.render(f"SHIELD {int(player.shield)}/{int(max_shield)}", True, (180, 180, 255))
            surface.blit(shield_text, (x + 260, shield_y))

        # Score, wave y zombies left
        surface.blit(self.font.render(f"SCORE: {player.score}", True, (255,255,255)), (30,100))
        surface.blit(self.font.render(f"WAVE: {wave_manager.current_wave}", True, (255,255,100)), (30,140))
        alive = sum(1 for z in wave_manager.game.zombies if not getattr(z, "dead", False))
        total_left = wave_manager.enemies_to_spawn + alive
        surface.blit(self.font.render(f"ZOMBIES LEFT: {total_left}", True, (255,120,120)), (30,180))

        # Ammo HUD
        sw, sh = surface.get_size()
        ammo_x, ammo_y = 30, sh-60
        circle_center = (ammo_x+24, ammo_y+6)
        circle_radius = 18
        pygame.draw.circle(surface, (30,30,30), circle_center, circle_radius)
        pygame.draw.circle(surface, (0,0,0), circle_center, circle_radius,2)
        if getattr(player,"weapon",None) and player.weapon.is_reloading:
            progress = max(0.0, min(1.0, player.weapon.reload_timer/max(0.0001, player.weapon.reload_time)))
            start_angle = -math.pi/2
            end_angle = start_angle + progress*2*math.pi
            rect = pygame.Rect(circle_center[0]-circle_radius, circle_center[1]-circle_radius, circle_radius*2, circle_radius*2)
            pygame.draw.arc(surface,(200,200,255),rect,start_angle,end_angle,6)
        else:
            pygame.draw.circle(surface,(80,220,80),circle_center,6)

        if getattr(player,"weapon",None):
            ammo_text = self.font.render(f"AMMO: {player.weapon.current_ammo}/{player.weapon.max_ammo} | {player.weapon.reserve_ammo}", True, (255,255,255))
            surface.blit(ammo_text, (ammo_x+60, ammo_y-4))
            if player.weapon.is_reloading:
                reload_text = self.font.render("RELOADING...", True, (200,200,255))
                surface.blit(reload_text, (ammo_x+110, ammo_y-30))

        # ===============================
        # Health bars y nivel de zombies
        # ===============================
        camera = getattr(wave_manager.game,"camera",None)
        screen_rect = surface.get_rect()
        for z in wave_manager.game.zombies:
            if getattr(z,"dead",False): 
                continue
            if not hasattr(z,"hp") or not hasattr(z,"rect"): 
                continue

            try: 
                z_screen_rect = camera.apply(z.rect) if camera else z.rect
            except Exception: 
                z_screen_rect = z.rect

            if not screen_rect.colliderect(z_screen_rect): 
                continue

            # Barra de vida
            zx, zy = z_screen_rect.centerx, z_screen_rect.bottom+4
            max_z_hp = z.TYPE_STATS.get(z.type,{}).get("hp", getattr(z,"hp",1))
            hp_ratio = max(0.0, min(1.0, (z.hp/max_z_hp) if max_z_hp else 0.0))
            bar_w = max(24, z_screen_rect.width//2)
            bar_h = 6
            pygame.draw.rect(surface,(0,0,0),(zx-bar_w//2-1, zy-1, bar_w+2, bar_h+2))
            pygame.draw.rect(surface,(60,60,60),(zx-bar_w//2, zy, bar_w, bar_h))
            col = (220,40,40) if hp_ratio<0.3 else (255,180,40) if hp_ratio<0.6 else (60,220,60)
            pygame.draw.rect(surface,col,(zx-bar_w//2, zy, int(bar_w*hp_ratio), bar_h))

            # Nivel sobre la cabeza
            level_text = f"Lv {getattr(z,'level',1)}"
            rarity_color_map = {
                "common": (255,255,255),
                "uncommon": (50,220,50),
                "rare": (50,150,255),
                "epic": (180,50,255),
                "legendary": (255,180,50)
            }
            txt_color = rarity_color_map.get(getattr(z,'rarity','common'), (255,255,255))
            txt_surf = self.font.render(level_text, True, txt_color)
            txt_rect = txt_surf.get_rect(center=(z_screen_rect.centerx, z_screen_rect.top - 10))
            surface.blit(txt_surf, txt_rect)

        # Minimapa
        self._ensure_minimap(wave_manager)
        if self.minimap: 
            self.minimap.draw(surface)