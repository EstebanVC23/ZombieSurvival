import pygame
import math

class ButtonWithBackground:
    """Botón con fondo coloreable y borde mejorado con efectos visuales."""
    def __init__(self, text, rect, font_path, base_size=20, hover_size=24,
                 color=(50,50,50), hover_color=(70,70,70),
                 text_color=(255,255,255), border_color=(200,200,200)):
        self.text = text
        self.rect = rect
        self.font_path = font_path
        self.base_size = base_size
        self.hover_size = hover_size
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color
        self.border_color = border_color
        self.hover_time = 0

    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()
        hovered = self.rect.collidepoint(mouse_pos)
        
        # Animación de hover
        if hovered:
            self.hover_time = min(self.hover_time + 0.15, 1.0)
        else:
            self.hover_time = max(self.hover_time - 0.15, 0.0)
        
        # Interpolación de color de fondo
        bg_color = self._interpolate_color(self.color, self.hover_color, self.hover_time)
        
        # Sombra del botón
        shadow_rect = self.rect.copy()
        shadow_rect.x += 4
        shadow_rect.y += 4
        shadow_surf = pygame.Surface(shadow_rect.size, pygame.SRCALPHA)
        shadow_surf.fill((0, 0, 0, 100))
        screen.blit(shadow_surf, shadow_rect.topleft)
        
        # Fondo del botón con bordes redondeados
        pygame.draw.rect(screen, bg_color, self.rect, border_radius=8)
        
        # Efecto de brillo en hover
        if hovered:
            pulse = abs(math.sin(pygame.time.get_ticks() / 300))
            glow_surf = pygame.Surface(self.rect.size, pygame.SRCALPHA)
            glow_color = (*self.border_color, int(50 + pulse * 50))
            pygame.draw.rect(glow_surf, glow_color, glow_surf.get_rect(), border_radius=8)
            screen.blit(glow_surf, self.rect.topleft)
        
        # Borde animado
        border_thickness = 3 if not hovered else int(3 + math.sin(pygame.time.get_ticks() / 200) * 1)
        pygame.draw.rect(screen, self.border_color, self.rect, border_thickness, border_radius=8)
        
        # Esquinas decorativas
        if hovered:
            corner_size = 8
            corners_color = self.border_color
            # Esquina superior izquierda
            pygame.draw.line(screen, corners_color, 
                           (self.rect.left, self.rect.top + corner_size),
                           (self.rect.left, self.rect.top), 2)
            pygame.draw.line(screen, corners_color,
                           (self.rect.left, self.rect.top),
                           (self.rect.left + corner_size, self.rect.top), 2)
            # Esquina superior derecha
            pygame.draw.line(screen, corners_color,
                           (self.rect.right - corner_size, self.rect.top),
                           (self.rect.right, self.rect.top), 2)
            pygame.draw.line(screen, corners_color,
                           (self.rect.right, self.rect.top),
                           (self.rect.right, self.rect.top + corner_size), 2)
            # Esquina inferior izquierda
            pygame.draw.line(screen, corners_color,
                           (self.rect.left, self.rect.bottom - corner_size),
                           (self.rect.left, self.rect.bottom), 2)
            pygame.draw.line(screen, corners_color,
                           (self.rect.left, self.rect.bottom),
                           (self.rect.left + corner_size, self.rect.bottom), 2)
            # Esquina inferior derecha
            pygame.draw.line(screen, corners_color,
                           (self.rect.right - corner_size, self.rect.bottom),
                           (self.rect.right, self.rect.bottom), 2)
            pygame.draw.line(screen, corners_color,
                           (self.rect.right, self.rect.bottom),
                           (self.rect.right, self.rect.bottom - corner_size), 2)
        
        # Texto con interpolación de tamaño
        font_size = int(self.base_size + (self.hover_size - self.base_size) * self.hover_time)
        font = pygame.font.Font(self.font_path, font_size)
        
        # Sombra del texto
        shadow_label = font.render(self.text, True, (0, 0, 0))
        shadow_rect = shadow_label.get_rect(center=(self.rect.centerx + 2, self.rect.centery + 2))
        screen.blit(shadow_label, shadow_rect)
        
        # Texto principal
        label = font.render(self.text, True, self.text_color)
        screen.blit(label, label.get_rect(center=self.rect.center))

    def is_clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)
    
    def _interpolate_color(self, color1, color2, t):
        """Interpola entre dos colores."""
        return tuple(int(color1[i] + (color2[i] - color1[i]) * t) for i in range(3))


class ButtonTextOnly:
    """Botón de solo texto mejorado con efectos visuales y animaciones."""
    def __init__(self, text, center_pos, font_path, base_size=18, hover_size=22,
                 text_color=(255,0,0), hover_color=(255,100,100)):
        self.text = text
        self.center_pos = center_pos
        self.font_path = font_path
        self.base_size = base_size
        self.hover_size = hover_size
        self.text_color = text_color
        self.hover_color = hover_color
        self.rect = None
        self.hover_time = 0

    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()
        hovered = self.rect.collidepoint(mouse_pos) if self.rect else False
        
        # Animación suave de hover
        if hovered:
            self.hover_time = min(self.hover_time + 0.12, 1.0)
        else:
            self.hover_time = max(self.hover_time - 0.12, 0.0)
        
        # Interpolación de color
        color = self._interpolate_color(self.text_color, self.hover_color, self.hover_time)
        
        # Interpolación de tamaño
        font_size = int(self.base_size + (self.hover_size - self.base_size) * self.hover_time)
        font = pygame.font.Font(self.font_path, font_size)
        
        # Efecto de resplandor cuando está en hover
        if hovered:
            pulse = abs(math.sin(pygame.time.get_ticks() / 400))
            
            # Múltiples capas de resplandor
            for offset in [4, 3, 2]:
                glow_alpha = int((100 - offset * 20) * pulse)
                glow_surf = font.render(self.text, True, self.hover_color)
                glow_surf.set_alpha(glow_alpha)
                
                for angle in range(0, 360, 60):
                    offset_x = int(math.cos(math.radians(angle)) * offset)
                    offset_y = int(math.sin(math.radians(angle)) * offset)
                    glow_rect = glow_surf.get_rect(center=(self.center_pos[0] + offset_x, 
                                                            self.center_pos[1] + offset_y))
                    screen.blit(glow_surf, glow_rect)
        
        # Sombra del texto (más pronunciada en hover)
        shadow_offset = 3 if hovered else 2
        shadow_label = font.render(self.text, True, (0, 0, 0))
        shadow_rect = shadow_label.get_rect(center=(self.center_pos[0] + shadow_offset, 
                                                     self.center_pos[1] + shadow_offset))
        shadow_label.set_alpha(150)
        screen.blit(shadow_label, shadow_rect)
        
        # Texto principal
        label = font.render(self.text, True, color)
        self.rect = label.get_rect(center=self.center_pos)
        screen.blit(label, self.rect)
        
        # Línea decorativa debajo del texto en hover
        if hovered:
            line_width = self.rect.width
            line_progress = pulse if hovered else 0
            current_width = int(line_width * (0.5 + line_progress * 0.5))
            line_start_x = self.rect.centerx - current_width // 2
            line_y = self.rect.bottom + 4
            
            pygame.draw.line(screen, self.hover_color,
                           (line_start_x, line_y),
                           (line_start_x + current_width, line_y), 2)
        
        # Partículas decorativas en hover
        if hovered and self.hover_time > 0.5:
            self._draw_particles(screen)

    def _draw_particles(self, screen):
        """Dibuja pequeñas partículas alrededor del botón."""
        particle_count = 4
        for i in range(particle_count):
            angle = (pygame.time.get_ticks() / 20 + i * 90) % 360
            distance = 30 + math.sin(pygame.time.get_ticks() / 300 + i) * 5
            
            x = self.center_pos[0] + math.cos(math.radians(angle)) * distance
            y = self.center_pos[1] + math.sin(math.radians(angle)) * distance
            
            alpha = int(100 + math.sin(pygame.time.get_ticks() / 200 + i) * 100)
            size = 2
            
            particle_surf = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
            pygame.draw.circle(particle_surf, (*self.hover_color, alpha), (size, size), size)
            screen.blit(particle_surf, (int(x - size), int(y - size)))

    def is_clicked(self, mouse_pos):
        return self.rect and self.rect.collidepoint(mouse_pos)
    
    def _interpolate_color(self, color1, color2, t):
        """Interpola entre dos colores."""
        return tuple(int(color1[i] + (color2[i] - color1[i]) * t) for i in range(3))


class Buttons:
    """Gestión de múltiples botones y su interacción."""
    def __init__(self, screen, buttons_list):
        self.screen = screen
        self.buttons = buttons_list

    def draw(self):
        for btn in self.buttons:
            btn.draw(self.screen)

    def handle_click(self, mouse_pos):
        for btn in self.buttons:
            if btn.is_clicked(mouse_pos):
                return btn.text
        return None