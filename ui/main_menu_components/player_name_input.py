import pygame
from ui.buttons import ButtonWithBackground
from colors import (WHITE, DARK_BG, DARK_PANEL, DARK_GREY, LIGHT_GREY,
                    MENU_GLOW, MENU_ACCENT, BORDER_HIGHLIGHT, 
                    SHIELD_BLUE_LIGHT, HP_RED_LIGHT)
from ui.main_menu_components.menu_visual_fx import MenuVisualFX

class PlayerNameOverlay:
    WIDTH = 600
    HEIGHT = 320

    def __init__(self, parent_screen):
        self.screen = parent_screen
        self.title_font = pygame.font.Font("assets/fonts/PressStart2P-Regular.ttf", 32)
        self.input_font = pygame.font.Font("assets/fonts/PressStart2P-Regular.ttf", 24)
        self.hint_font = pygame.font.Font("assets/fonts/PressStart2P-Regular.ttf", 14)
        
        # Animación
        self.animation_offset = 0
        self.pulse_alpha = 0
        self.pulse_direction = 1
        
        # Input box con más espacio
        self.input_box = pygame.Rect(
            (self.screen.get_width() - self.WIDTH)//2 + 40,
            (self.screen.get_height() - self.HEIGHT)//2 + 120,
            self.WIDTH - 80,
            50
        )
        
        self.color_inactive = DARK_GREY
        self.color_active = MENU_GLOW
        self.color = self.color_active
        self.text = ""
        self.active = True
        self.done = False
        self.cursor_visible = True
        self.cursor_timer = 0

        # Botones mejorados
        centerx = self.screen.get_width() // 2
        top = (self.screen.get_height() - self.HEIGHT) // 2 + 260

        self.confirm_btn = ButtonWithBackground(
            "CONFIRM",
            None,  # Se asignará después
            "assets/fonts/PressStart2P-Regular.ttf",
            18, 20,
            WHITE, MENU_GLOW
        )
        self.cancel_btn = ButtonWithBackground(
            "CANCEL",
            None,  # Se asignará después
            "assets/fonts/PressStart2P-Regular.ttf",
            18, 20,
            WHITE, HP_RED_LIGHT
        )

        # Crear rects con padding adecuado
        button_font = pygame.font.Font("assets/fonts/PressStart2P-Regular.ttf", 18)
        confirm_text = button_font.render("CONFIRM", True, WHITE)
        cancel_text = button_font.render("CANCEL", True, WHITE)
        
        # Añadir padding horizontal y vertical
        padding_x = 30  # Padding horizontal
        padding_y = 15  # Padding vertical
        
        confirm_rect = pygame.Rect(0, 0, 
                                   confirm_text.get_width() + padding_x * 2,
                                   confirm_text.get_height() + padding_y * 2)
        confirm_rect.center = (centerx - 110, top)
        
        cancel_rect = pygame.Rect(0, 0,
                                  cancel_text.get_width() + padding_x * 2,
                                  cancel_text.get_height() + padding_y * 2)
        cancel_rect.center = (centerx + 110, top)
        
        self.confirm_btn.rect = confirm_rect
        self.cancel_btn.rect = cancel_rect

    def update_animations(self):
        """Actualiza las animaciones del overlay"""
        self.animation_offset = (self.animation_offset + 0.5) % 360
        
        # Pulso para el borde del input
        self.pulse_alpha += 3 * self.pulse_direction
        if self.pulse_alpha >= 100:
            self.pulse_direction = -1
        elif self.pulse_alpha <= 0:
            self.pulse_direction = 1
            
        # Cursor parpadeante
        self.cursor_timer += 1
        if self.cursor_timer >= 30:
            self.cursor_visible = not self.cursor_visible
            self.cursor_timer = 0

    def draw_glow_effect(self, surface, rect, color, intensity=50):
        """Dibuja un efecto de brillo alrededor de un rectángulo"""
        glow_surf = pygame.Surface((rect.width + 20, rect.height + 20), pygame.SRCALPHA)
        # Asegurarnos de que color sea RGB (sin alpha)
        base_color = color[:3] if len(color) >= 3 else color
        for i in range(3):
            alpha = max(0, min(255, int(intensity - (i * 15))))
            offset = i * 3
            glow_rect = pygame.Rect(offset, offset, rect.width + (6-offset*2), rect.height + (6-offset*2))
            pygame.draw.rect(glow_surf, (*base_color, alpha), glow_rect, border_radius=8)
        surface.blit(glow_surf, (rect.x - 10, rect.y - 10))

    def draw(self):
        self.update_animations()
        
        # Fondo semi-transparente con gradiente
        overlay = pygame.Surface((self.screen.get_width(), self.screen.get_height()), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))

        # Panel principal
        panel_rect = pygame.Rect(
            (self.screen.get_width() - self.WIDTH)//2,
            (self.screen.get_height() - self.HEIGHT)//2,
            self.WIDTH,
            self.HEIGHT
        )
        
        # Sombra del panel
        shadow_rect = panel_rect.copy()
        shadow_rect.x += 5
        shadow_rect.y += 5
        shadow_surf = pygame.Surface((shadow_rect.width, shadow_rect.height), pygame.SRCALPHA)
        pygame.draw.rect(shadow_surf, (0, 0, 0, 100), shadow_surf.get_rect(), border_radius=15)
        self.screen.blit(shadow_surf, shadow_rect)
        
        # Panel con gradiente
        pygame.draw.rect(self.screen, DARK_PANEL, panel_rect, border_radius=15)
        
        # Borde brillante animado
        MenuVisualFX.draw_animated_border(self.screen, panel_rect, MENU_GLOW, 3, 2)
        
        # Borde interno decorativo
        inner_rect = panel_rect.inflate(-10, -10)
        pygame.draw.rect(self.screen, DARK_GREY, inner_rect, 1, border_radius=12)

        # Título con efecto de brillo
        title = self.title_font.render("PLAYER NAME", True, MENU_ACCENT)
        title_rect = title.get_rect(center=(panel_rect.centerx, panel_rect.top + 45))
        
        # Sombra del título
        title_shadow = self.title_font.render("PLAYER NAME", True, (0, 0, 0, 150))
        self.screen.blit(title_shadow, (title_rect.x + 2, title_rect.y + 2))
        self.screen.blit(title, title_rect)
        
        # Línea decorativa bajo el título
        line_y = panel_rect.top + 75
        pygame.draw.line(self.screen, MENU_GLOW, 
                        (panel_rect.centerx - 150, line_y),
                        (panel_rect.centerx + 150, line_y), 2)

        # Input box con efectos
        # Brillo exterior pulsante
        if self.active:
            self.draw_glow_effect(self.screen, self.input_box, MENU_GLOW, self.pulse_alpha)
        
        # Fondo del input
        input_bg = self.input_box.inflate(4, 4)
        pygame.draw.rect(self.screen, DARK_BG, input_bg, border_radius=8)
        
        # Borde del input
        border_color = self.color_active if self.active else self.color_inactive
        pygame.draw.rect(self.screen, border_color, self.input_box, 3, border_radius=6)
        
        # Texto del input con cursor
        if self.text:
            txt_surface = self.input_font.render(self.text, True, WHITE)
            text_x = self.input_box.x + 15
            text_y = self.input_box.y + (self.input_box.height - txt_surface.get_height()) // 2
            self.screen.blit(txt_surface, (text_x, text_y))
            
            # Cursor parpadeante
            if self.cursor_visible and self.active:
                cursor_x = text_x + txt_surface.get_width() + 5
                cursor_y = self.input_box.y + 10
                pygame.draw.line(self.screen, MENU_ACCENT,
                               (cursor_x, cursor_y),
                               (cursor_x, cursor_y + 30), 3)
        else:
            # Placeholder text
            placeholder = self.input_font.render("Enter name...", True, DARK_GREY)
            placeholder_x = self.input_box.x + 15
            placeholder_y = self.input_box.y + (self.input_box.height - placeholder.get_height()) // 2
            self.screen.blit(placeholder, (placeholder_x, placeholder_y))
            
            # Cursor al inicio si está activo
            if self.cursor_visible and self.active:
                cursor_x = placeholder_x
                cursor_y = self.input_box.y + 10
                pygame.draw.line(self.screen, MENU_ACCENT,
                               (cursor_x, cursor_y),
                               (cursor_x, cursor_y + 30), 3)

        # Hint text
        hint = self.hint_font.render("Max 12 characters", True, LIGHT_GREY)
        hint_rect = hint.get_rect(center=(panel_rect.centerx, self.input_box.bottom + 20))
        self.screen.blit(hint, hint_rect)

        # Botones con estado visual mejorado
        if self.text.strip():
            self.confirm_btn.text_color = WHITE
            self.confirm_btn.border_color = MENU_GLOW
        else:
            self.confirm_btn.text_color = DARK_GREY
            self.confirm_btn.border_color = DARK_GREY
            
        self.confirm_btn.draw(self.screen)
        self.cancel_btn.draw(self.screen)
        
        # Indicador de caracteres
        char_count = f"{len(self.text)}/12"
        count_color = HP_RED_LIGHT if len(self.text) >= 12 else LIGHT_GREY
        count_text = self.hint_font.render(char_count, True, count_color)
        count_rect = count_text.get_rect(bottomright=(self.input_box.right - 10, self.input_box.bottom - 55))
        self.screen.blit(count_text, count_rect)

    def run_event(self, event):
        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_RETURN and self.text.strip():
                self.done = True
                return self.text.strip()
            elif event.key == pygame.K_ESCAPE:
                self.done = False
                return "CANCEL"
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
                self.cursor_timer = 0
                self.cursor_visible = True
            else:
                if len(self.text) < 12 and event.unicode.isprintable():
                    self.text += event.unicode
                    self.cursor_timer = 0
                    self.cursor_visible = True
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()
            if self.confirm_btn.is_clicked(mouse_pos) and self.text.strip():
                self.done = True
                return self.text.strip()
            elif self.cancel_btn.is_clicked(mouse_pos):
                self.done = False
                return "CANCEL"
        return None