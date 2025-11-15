import pygame

class ButtonWithBackground:
    """Botón con fondo coloreable y borde."""
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

    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()
        hovered = self.rect.collidepoint(mouse_pos)
        bg_color = self.hover_color if hovered else self.color
        pygame.draw.rect(screen, bg_color, self.rect)
        pygame.draw.rect(screen, self.border_color, self.rect, 3)
        font_size = self.hover_size if hovered else self.base_size
        font = pygame.font.Font(self.font_path, font_size)
        label = font.render(self.text, True, self.text_color)
        screen.blit(label, label.get_rect(center=self.rect.center))

    def is_clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)


class ButtonTextOnly:
    """Botón de solo texto, sin fondo, color configurable desde afuera."""
    def __init__(self, text, center_pos, font_path, base_size=18, hover_size=22,
                 text_color=(255,0,0), hover_color=(255,100,100)):
        self.text = text
        self.center_pos = center_pos
        self.font_path = font_path
        self.base_size = base_size
        self.hover_size = hover_size
        self.text_color = text_color
        self.hover_color = hover_color
        self.rect = None  # Se asigna después de renderizar

    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()
        hovered = self.rect.collidepoint(mouse_pos) if self.rect else False
        color = self.hover_color if hovered else self.text_color
        font_size = self.hover_size if hovered else self.base_size
        font = pygame.font.Font(self.font_path, font_size)
        label = font.render(self.text, True, color)
        self.rect = label.get_rect(center=self.center_pos)
        screen.blit(label, self.rect)

    def is_clicked(self, mouse_pos):
        return self.rect and self.rect.collidepoint(mouse_pos)


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
