import pygame
import math
from colors import MENU_SHADOW

class MenuVisualFX:
    @staticmethod
    def draw_glowing_title(surface, text, pos, font, base_color, glow_color, time_offset):
        pulse = abs(math.sin(pygame.time.get_ticks()/500 + time_offset))
        for offset in [(4,4),(3,3),(2,2)]:
            shadow = font.render(text, True, MENU_SHADOW)
            rect = shadow.get_rect(center=(pos[0]+offset[0], pos[1]+offset[1]))
            surface.blit(shadow, rect)
        glow_intensity = int(100 + pulse*155)
        color = (glow_color[0], glow_color[1], glow_color[2], glow_intensity)
        for radius in [6,4,2]:
            gl = font.render(text, True, color[:3])
            gl.set_alpha(glow_intensity // (7-radius))
            for angle in range(0,360,45):
                ox = int(math.cos(math.radians(angle))*radius)
                oy = int(math.sin(math.radians(angle))*radius)
                rect = gl.get_rect(center=(pos[0]+ox, pos[1]+oy))
                surface.blit(gl, rect)
        surf = font.render(text, True, base_color)
        rect = surf.get_rect(center=pos)
        surface.blit(surf, rect)

    @staticmethod
    def draw_animated_border(surface, rect, color, thickness, time_offset):
        pulse = abs(math.sin(pygame.time.get_ticks()/300 + time_offset))
        animated_thickness = int(thickness + pulse*2)
        pygame.draw.rect(surface, color, rect, animated_thickness, border_radius=8)
        inner_rect = rect.inflate(-10, -10)
        inner_color = (color[0]//3, color[1]//3, color[2]//3)
        pygame.draw.rect(surface, inner_color, inner_rect, 1, border_radius=6)