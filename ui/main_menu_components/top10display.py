# ================================================================
# top10_display.py
# ================================================================

import pygame
from utils.score_manager import ScoreManager
from colors import (WHITE, MENU_GLOW, DARK_PANEL, DARK_GREY, DARK_BG,
                     LIGHT_GREY, MENU_ACCENT, MENU_SHADOW, BORDER_GREY,
                     YELLOW, SHIELD_BLUE_LIGHT)

class Top10Display:
    """Overlay que muestra la clasificación completa de jugadores con scroll."""

    WIDTH = 600
    HEIGHT = 680
    LINE_HEIGHT = 48
    PADDING = 40
    SCROLL_SPEED = 30

    def __init__(self, parent_screen):
        self.screen = parent_screen
        self.font = pygame.font.Font(None, 26)
        self.font_bold = pygame.font.Font(None, 28)
        self.title_font = pygame.font.Font(None, 48)
        self.subtitle_font = pygame.font.Font(None, 22)
        self.score_manager = ScoreManager()
        self.active = False
        self.scroll_offset = 0
        self.max_scroll = 0

    def draw(self):
        if not self.active:
            return

        screen = self.screen
        top_scores = self.score_manager.get_top_scores()

        # Ordenar por score descendente y luego por wave descendente
        top_scores.sort(key=lambda e: (-e.get("score",0), -e.get("wave",0)))

        # Fondo semi-transparente con efecto de desenfoque visual
        overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        screen.blit(overlay, (0, 0))

        # Panel principal con sombra
        panel_rect = pygame.Rect(
            (screen.get_width() - self.WIDTH) // 2,
            (screen.get_height() - self.HEIGHT) // 2,
            self.WIDTH,
            self.HEIGHT
        )
        
        # Sombra del panel
        shadow_rect = panel_rect.copy()
        shadow_rect.x += 5
        shadow_rect.y += 5
        shadow_surface = pygame.Surface((shadow_rect.width, shadow_rect.height), pygame.SRCALPHA)
        pygame.draw.rect(shadow_surface, (*MENU_SHADOW, 120), shadow_surface.get_rect(), border_radius=16)
        screen.blit(shadow_surface, shadow_rect)

        # Panel principal con gradiente simulado
        pygame.draw.rect(screen, DARK_BG, panel_rect, border_radius=16)
        pygame.draw.rect(screen, MENU_GLOW, panel_rect, 3, border_radius=16)
        
        # Borde interno sutil
        inner_rect = panel_rect.inflate(-6, -6)
        pygame.draw.rect(screen, BORDER_GREY, inner_rect, 1, border_radius=14)

        # Encabezado con fondo destacado
        header_rect = pygame.Rect(
            panel_rect.left + 20,
            panel_rect.top + 20,
            panel_rect.width - 40,
            70
        )
        pygame.draw.rect(screen, DARK_PANEL, header_rect, border_radius=12)
        pygame.draw.rect(screen, MENU_ACCENT, header_rect, 2, border_radius=12)

        # Título
        title_surf = self.title_font.render("CLASIFICACIÓN", True, MENU_GLOW)
        title_rect = title_surf.get_rect(center=(panel_rect.centerx, panel_rect.top + 45))
        screen.blit(title_surf, title_rect)

        # Subtítulo con información
        subtitle_text = f"Todos los Jugadores ({len(top_scores)})"
        subtitle_surf = self.subtitle_font.render(subtitle_text, True, LIGHT_GREY)
        subtitle_rect = subtitle_surf.get_rect(center=(panel_rect.centerx, panel_rect.top + 72))
        screen.blit(subtitle_surf, subtitle_rect)

        # Área de contenido con scroll
        content_y_start = panel_rect.top + 110
        content_height = panel_rect.height - 180  # Espacio para header y footer
        
        # Calcular altura total necesaria
        total_content_height = len(top_scores) * self.LINE_HEIGHT + 20
        
        # Crear superficie de scroll con altura total
        scroll_surface = pygame.Surface((panel_rect.width - 60, total_content_height), pygame.SRCALPHA)
        
        if not top_scores:
            # Mensaje cuando no hay puntuaciones
            no_scores_rect = pygame.Rect(
                10,
                content_height // 2 - 40,
                scroll_surface.get_width() - 20,
                80
            )
            pygame.draw.rect(scroll_surface, DARK_PANEL, no_scores_rect, border_radius=10)
            
            text_surf = self.font.render("No hay puntuaciones aún.", True, LIGHT_GREY)
            text_rect = text_surf.get_rect(center=(no_scores_rect.centerx, no_scores_rect.centery - 10))
            scroll_surface.blit(text_surf, text_rect)
            
            subtext_surf = self.subtitle_font.render("¡Sé el primero en jugar!", True, MENU_ACCENT)
            subtext_rect = subtext_surf.get_rect(center=(no_scores_rect.centerx, no_scores_rect.centery + 15))
            scroll_surface.blit(subtext_surf, subtext_rect)
        else:
            y = 10  # Empezar desde arriba de la superficie
            position = 1
            last_score = None
            last_wave = None
            
            for idx, entry in enumerate(top_scores):
                player = entry.get("player", "Player")
                score = entry.get("score", 0)
                wave = entry.get("wave", 0)

                # Determinar posición (empate si score y wave iguales)
                if last_score is not None and (score != last_score or wave != last_wave):
                    position += 1
                
                # Fila con fondo alternado
                row_rect = pygame.Rect(
                    10,
                    y - 5,
                    scroll_surface.get_width() - 20,
                    self.LINE_HEIGHT - 4
                )
                
                # Color especial para top 3 (basado en posición, no en índice)
                if position == 1:
                    row_color = (*YELLOW[:3], 40)  # Dorado con transparencia
                    position_color = YELLOW
                    glow_color = YELLOW
                elif position == 2:
                    row_color = (*LIGHT_GREY[:3], 40)  # Plateado con transparencia
                    position_color = LIGHT_GREY
                    glow_color = LIGHT_GREY
                elif position == 3:
                    row_color = (139, 90, 43, 40)  # Bronce con transparencia
                    position_color = (205, 127, 50)  # Color bronce
                    glow_color = (205, 127, 50)
                else:
                    row_color = (30, 30, 40, 60) if idx % 2 == 0 else (25, 25, 35, 40)
                    position_color = MENU_ACCENT
                    glow_color = MENU_ACCENT

                # Dibujar fondo de fila
                row_surface = pygame.Surface((row_rect.width, row_rect.height), pygame.SRCALPHA)
                pygame.draw.rect(row_surface, row_color, row_surface.get_rect(), border_radius=8)
                scroll_surface.blit(row_surface, row_rect)
                
                # Borde sutil para top 3
                if position <= 3:
                    pygame.draw.rect(scroll_surface, glow_color, row_rect, 1, border_radius=8)

                # Posición con círculo decorativo
                pos_x = 30
                pos_y = y + self.LINE_HEIGHT // 2
                
                # Círculo para la posición
                pygame.draw.circle(scroll_surface, position_color, (pos_x, pos_y), 16)
                pygame.draw.circle(scroll_surface, DARK_PANEL, (pos_x, pos_y), 14)
                pos_text = str(position)
                pos_surf = self.font_bold.render(pos_text, True, position_color)
                pos_rect = pos_surf.get_rect(center=(pos_x, pos_y))
                scroll_surface.blit(pos_surf, pos_rect)

                # Nombre del jugador
                player_surf = self.font_bold.render(player, True, WHITE)
                scroll_surface.blit(player_surf, (pos_x + 30, y + 5))

                # Score y Wave en columnas
                score_text = f"{score} pts"
                score_surf = self.font.render(score_text, True, MENU_ACCENT)
                score_rect = score_surf.get_rect(right=scroll_surface.get_width() - 120, centery=pos_y)
                scroll_surface.blit(score_surf, score_rect)

                wave_text = f"Wave {wave}"
                wave_surf = self.subtitle_font.render(wave_text, True, SHIELD_BLUE_LIGHT)
                wave_rect = wave_surf.get_rect(right=scroll_surface.get_width() - 20, centery=pos_y)
                scroll_surface.blit(wave_surf, wave_rect)

                y += self.LINE_HEIGHT
                last_score = score
                last_wave = wave
            
            # Calcular scroll máximo
            self.max_scroll = max(0, total_content_height - content_height)

        # Crear una superficie recortada para el área visible
        visible_surface = pygame.Surface((scroll_surface.get_width(), content_height), pygame.SRCALPHA)
        
        # Copiar solo la parte visible de scroll_surface
        visible_surface.blit(scroll_surface, (0, -self.scroll_offset))
        
        # Dibujar la superficie visible en el panel
        screen.blit(visible_surface, (panel_rect.left + 30, content_y_start))
        
        # Dibujar barra de scroll si es necesario
        if self.max_scroll > 0:
            scrollbar_x = panel_rect.right - 25
            scrollbar_y = content_y_start
            scrollbar_height = content_height
            scrollbar_width = 8
            
            # Fondo de la barra
            pygame.draw.rect(screen, DARK_PANEL, 
                           (scrollbar_x, scrollbar_y, scrollbar_width, scrollbar_height),
                           border_radius=4)
            
            # Tamaño y posición del thumb
            thumb_height = max(30, (content_height / (self.max_scroll + content_height)) * scrollbar_height)
            thumb_y = scrollbar_y + (self.scroll_offset / self.max_scroll) * (scrollbar_height - thumb_height)
            
            # Dibujar thumb
            pygame.draw.rect(screen, MENU_GLOW,
                           (scrollbar_x, thumb_y, scrollbar_width, thumb_height),
                           border_radius=4)

        # Footer con instrucciones
        footer_y = panel_rect.bottom - 45
        if self.max_scroll > 0:
            footer_text = "Usa la rueda del mouse para desplazar | ESC o clic fuera para cerrar"
        else:
            footer_text = "Presiona ESC o haz clic fuera para cerrar"
        footer_surf = self.subtitle_font.render(footer_text, True, LIGHT_GREY)
        footer_rect = footer_surf.get_rect(center=(panel_rect.centerx, footer_y))
        screen.blit(footer_surf, footer_rect)

    def handle_event(self, event):
        """Cerrar overlay con ESC o click fuera del panel, scroll con rueda del mouse"""
        if not self.active:
            return

        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.active = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            panel_rect = pygame.Rect(
                (self.screen.get_width() - self.WIDTH) // 2,
                (self.screen.get_height() - self.HEIGHT) // 2,
                self.WIDTH,
                self.HEIGHT
            )
            
            if event.button == 1:  # Click izquierdo
                if not panel_rect.collidepoint(pygame.mouse.get_pos()):
                    self.active = False
            elif event.button == 4:  # Rueda arriba
                self.scroll_offset = max(0, self.scroll_offset - self.SCROLL_SPEED)
            elif event.button == 5:  # Rueda abajo
                self.scroll_offset = min(self.max_scroll, self.scroll_offset + self.SCROLL_SPEED)

    def show(self):
        self.active = True
        self.scroll_offset = 0  # Reset scroll al abrir