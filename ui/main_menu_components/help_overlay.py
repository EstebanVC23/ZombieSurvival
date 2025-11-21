# ================================================================
# help_overlay.py - Versión Mejorada Visual v2
# ================================================================

import pygame
import math
from colors import WHITE, DARK_BG, DARK_GREY, MENU_GLOW

class HelpOverlay:
    def __init__(self, screen):
        self.screen = screen
        self.active = False

        # Panel principal más grande para contenido extendido
        # Asegurar que el panel no sea más grande que la pantalla
        max_width = screen.get_width() - 80
        max_height = screen.get_height() - 80
        self.width = min(950, max_width)
        self.height = min(650, max_height)
        self.x = (screen.get_width() - self.width) // 2
        self.y = (screen.get_height() - self.height) // 2
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

        # Botón de cerrar
        self.close_rect = pygame.Rect(self.x + self.width - 55, self.y + 12, 45, 45)

        # Tipos de letra
        self.font_title = pygame.font.Font("assets/fonts/PressStart2P-Regular.ttf", 20)
        self.font_section = pygame.font.Font("assets/fonts/PressStart2P-Regular.ttf", 12)
        self.font_text = pygame.font.Font("assets/fonts/PressStart2P-Regular.ttf", 9)
        self.font_small = pygame.font.Font("assets/fonts/PressStart2P-Regular.ttf", 8)

        # Scroll mejorado
        self.scroll_offset = 0
        self.max_scroll = 0
        self.scroll_speed = 100  # Aumentado para scroll más rápido

        # Colores temáticos mejorados con más contraste
        self.color_control = (80, 180, 255)     # Azul brillante
        self.color_zombie = (255, 80, 80)       # Rojo intenso
        self.color_upgrade = (100, 255, 120)    # Verde neón
        self.color_biome = (255, 180, 60)       # Naranja cálido
        self.color_tip = (255, 240, 80)         # Amarillo brillante
        self.color_score = (180, 120, 255)      # Púrpura
        
        # Colores de fondo para secciones
        self.bg_control = (20, 40, 60, 120)
        self.bg_zombie = (60, 20, 20, 120)
        self.bg_upgrade = (20, 60, 30, 120)
        self.bg_biome = (60, 45, 20, 120)
        self.bg_tip = (60, 60, 20, 120)
        self.bg_score = (45, 30, 60, 120)

        # Animación
        self.anim_time = 0

        # Contenido del help expandido
        self.sections = [
            {
                "title": "CONTROLES",
                "icon": "⌨",
                "color": self.color_control,
                "bg_color": self.bg_control,
                "lines": [
                    ("Flechas direccionales", "Mover al jugador"),
                    ("Click izquierdo", "Disparar"),
                    ("Mouse", "Apuntar direccion"),
                    ("ESC", "Pausar juego"),
                    "",
                    "» Mantén el movimiento fluido y dispara",
                    "  en la direccion del cursor"
                ]
            },
            {
                "title": "TIPOS DE ZOMBIES",
                "icon": "☠",
                "color": self.color_zombie,
                "bg_color": self.bg_zombie,
                "lines": [
                    ("COMUN", "Lentos pero numerosos"),
                    "  • Vida: Baja | Velocidad: Lenta",
                    "  • Aparecen en grandes grupos",
                    "",
                    ("RAPIDO", "Persiguen agresivamente"),
                    "  • Vida: Media | Velocidad: Alta",
                    "  • Peligrosos en espacios cerrados",
                    "",
                    ("TANQUE", "Resistentes al daño"),
                    "  • Vida: Alta | Velocidad: Lenta",
                    "  • Requieren estrategia",
                    "",
                    ("ELITE/BOSS", "Aparecen cada 10 oleadas"),
                    "  • Vida: Muy Alta | Velocidad: Media",
                    "  • Recompensa de puntos x2"
                ]
            },
            {
                "title": "CARTAS DE MEJORA",
                "icon": "⚡",
                "color": self.color_upgrade,
                "bg_color": self.bg_upgrade,
                "lines": [
                    "Aparecen al completar oleadas clave",
                    "",
                    ("⚡ VELOCIDAD +", "Aumenta tu velocidad"),
                    ("💥 DAÑO +", "Disparos mas poderosos"),
                    ("🔫 CADENCIA +", "Dispara mas rapido"),
                    ("❤ VIDA MAX +", "Aumenta puntos de vida"),
                    ("💚 CURACION", "Recupera vida perdida"),
                    "",
                    "» Elige segun tu estilo de juego",
                    "» Las mejoras son permanentes"
                ]
            },
            {
                "title": "BIOMAS Y PELIGROS",
                "icon": "🌍",
                "color": self.color_biome,
                "bg_color": self.bg_biome,
                "lines": [
                    ("Oleadas 1-10", "PRADERAS - Terreno basico"),
                    ("Oleadas 11-20", "DESIERTO - Cactus dañinos"),
                    ("Oleadas 21-30", "BOSQUE - Emboscadas"),
                    ("Oleadas 31-40", "PANTANO - Agua ralentiza"),
                    ("Oleadas 41-50", "MONTAÑA - Rocas bloquean"),
                    ("Oleadas 51-60", "VOLCAN - Lava mortal"),
                    ("Oleadas 61-70", "TUNDRA - Hielo resbaladizo"),
                    ("Oleadas 71-80", "COSTA - Agua profunda"),
                    ("Oleadas 81-90", "UMBRAL - Caos total"),
                    ("Oleadas 91-100", "EPICENTRO - Desafio maximo"),
                    "",
                    "» Cada bioma cambia la estrategia"
                ]
            },
            {
                "title": "TIPS DE SUPERVIVENCIA",
                "icon": "💡",
                "color": self.color_tip,
                "bg_color": self.bg_tip,
                "lines": [
                    "⚠ MOVIMIENTO:",
                    "  • Nunca dejes de moverte",
                    "  • Usa patrones circulares",
                    "  • Evita las esquinas",
                    "",
                    "⚠ COMBATE:",
                    "  • Prioriza zombies rapidos",
                    "  • Dispara mientras retrocedes",
                    "  • Agrupa enemigos antes de disparar",
                    "",
                    "⚠ TERRENO:",
                    "  • La lava mata al instante",
                    "  • El agua te hace vulnerable",
                    "  • Usa obstaculos como barreras",
                    "",
                    "⚠ ESTRATEGIA:",
                    "  • Boss en oleadas 10, 20, 30...",
                    "  • Guarda espacio para huir",
                    "  • Conoce el mapa"
                ]
            },
            {
                "title": "SISTEMA DE PUNTAJE",
                "icon": "🏆",
                "color": self.color_score,
                "bg_color": self.bg_score,
                "lines": [
                    ("Zombie Comun", "10 puntos"),
                    ("Zombie Rapido", "25 puntos"),
                    ("Zombie Tanque", "50 puntos"),
                    ("Zombie Elite", "100 puntos"),
                    "",
                    ("Bonus Oleada x10", "+500 puntos"),
                    ("Bonus Racha", "Multiplicador x1.5"),
                    "",
                    "» Compite en la tabla global",
                    "» Cada muerte cuenta"
                ]
            },
            {
                "title": "OBJETIVO FINAL",
                "icon": "🎯",
                "color": WHITE,
                "bg_color": (30, 30, 30, 120),
                "lines": [
                    "Sobrevive las 100 oleadas atravesando",
                    "todos los biomas del mundo devastado.",
                    "",
                    "Al completar la oleada 100:",
                    "  • Desbloqueas modo INFINITO",
                    "  • Dificultad aumenta sin limite",
                    "  • Tu legado queda registrado",
                    "",
                    "No hay final feliz.",
                    "Solo resistencia.",
                    "",
                    "¿Cuanto tiempo sobreviviras?"
                ]
            }
        ]

        # Calcular altura total del contenido
        self._calculate_content_height()

    def _calculate_content_height(self):
        """Calcula la altura total del contenido para el scroll"""
        total_height = 30  # Margen inicial
        for section in self.sections:
            total_height += 65  # Título con fondo
            total_height += len(section["lines"]) * 15  # Líneas
            total_height += 25  # Espaciado entre secciones
        self.max_scroll = max(0, total_height - (self.height - 90))

    def show(self):
        self.active = True
        self.scroll_offset = 0
        self.anim_time = 0

    def hide(self):
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Click izquierdo
                if self.close_rect.collidepoint(event.pos):
                    self.hide()
            elif event.button == 4:  # Scroll up
                self.scroll_offset = max(0, self.scroll_offset - self.scroll_speed)
            elif event.button == 5:  # Scroll down
                self.scroll_offset = min(self.max_scroll, self.scroll_offset + self.scroll_speed)

    def draw(self):
        if not self.active:
            return

        self.anim_time += 1
        
        # Fondo oscuro semitransparente
        overlay = pygame.Surface((self.screen.get_width(), self.screen.get_height()), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))

        # Panel principal con gradiente
        panel_surf = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        for i in range(self.height):
            alpha = 220 - (i // 10)
            color = (*DARK_BG, max(180, alpha))
            pygame.draw.line(panel_surf, color, (0, i), (self.width, i))
        self.screen.blit(panel_surf, (self.x, self.y))

        # Bordes con efecto neón
        glow_pulse = abs(math.sin(self.anim_time / 30)) * 30 + 200
        glow_color = (int(glow_pulse), int(glow_pulse * 0.7), int(glow_pulse * 0.9))
        pygame.draw.rect(self.screen, glow_color, self.rect, 3, border_radius=10)
        pygame.draw.rect(self.screen, DARK_GREY, self.rect, 2, border_radius=10)

        # Botón de cerrar mejorado
        mouse_pos = pygame.mouse.get_pos()
        is_hover = self.close_rect.collidepoint(mouse_pos)
        close_color = (255, 80, 80) if is_hover else (200, 60, 60)
        
        pygame.draw.rect(self.screen, close_color, self.close_rect, border_radius=8)
        pygame.draw.rect(self.screen, WHITE, self.close_rect, 2, border_radius=8)
        
        # X más grande y centrada
        x_text = self.font_section.render("X", True, WHITE)
        x_rect = x_text.get_rect(center=self.close_rect.center)
        shadow_rect = x_rect.copy()
        shadow_rect.x += 1
        shadow_rect.y += 1
        shadow_text = self.font_section.render("X", True, (0, 0, 0))
        self.screen.blit(shadow_text, shadow_rect)
        self.screen.blit(x_text, x_rect)

        # Título principal con efecto brillante
        title_text = "GUIA DE SUPERVIVENCIA"
        title_surf = self.font_title.render(title_text, True, WHITE)
        shadow_surf = self.font_title.render(title_text, True, (0, 0, 0))
        
        title_x = self.x + (self.width - title_surf.get_width()) // 2
        self.screen.blit(shadow_surf, (title_x + 2, self.y + 17))
        self.screen.blit(title_surf, (title_x, self.y + 15))
        
        # Línea decorativa bajo el título
        line_y = self.y + 55
        pygame.draw.line(self.screen, MENU_GLOW, (self.x + 50, line_y), (self.x + self.width - 50, line_y), 2)

        # Área de contenido
        content_x = self.x + 15
        content_y = self.y + 70
        content_width = self.width - 30
        content_height = self.height - 85
        
        # Validar límites
        if (content_x < 0 or content_y < 0 or 
            content_x + content_width > self.screen.get_width() or 
            content_y + content_height > self.screen.get_height()):
            content_x = max(0, content_x)
            content_y = max(0, content_y)
            content_width = min(content_width, self.screen.get_width() - content_x)
            content_height = min(content_height, self.screen.get_height() - content_y)
        
        # Superficie temporal para contenido
        temp_surface = pygame.Surface((content_width, content_height), pygame.SRCALPHA)
        
        # Dibujar secciones
        current_y = -self.scroll_offset + 10
        
        for section in self.sections:
            # Fondo de sección con color temático
            section_height = 50 + len(section["lines"]) * 15
            if current_y > -section_height and current_y < content_height:
                section_bg = pygame.Surface((content_width - 20, section_height), pygame.SRCALPHA)
                section_bg.fill(section["bg_color"])
                temp_surface.blit(section_bg, (10, current_y))
                
                # Borde izquierdo colorido
                pygame.draw.rect(temp_surface, section["color"], 
                               (10, current_y, 4, section_height))

            # Icono + Título de sección
            if current_y > -50 and current_y < content_height:
                icon_surf = self.font_title.render(section["icon"], True, section["color"])
                temp_surface.blit(icon_surf, (20, current_y + 8))
                
                title_surf = self.font_section.render(section["title"], True, section["color"])
                temp_surface.blit(title_surf, (55, current_y + 12))
            
            current_y += 50

            # Líneas de contenido
            for line in section["lines"]:
                if line == "":
                    current_y += 8
                    continue
                
                if isinstance(line, tuple):
                    # Formato (título, descripción)
                    key, value = line
                    if current_y > -20 and current_y < content_height:
                        key_surf = self.font_text.render(key, True, section["color"])
                        temp_surface.blit(key_surf, (25, current_y))
                        
                        value_surf = self.font_small.render(value, True, WHITE)
                        temp_surface.blit(value_surf, (25 + key_surf.get_width() + 10, current_y + 2))
                else:
                    # Texto normal
                    is_subtitle = line.startswith("⚠") or line.startswith("»")
                    color = section["color"] if is_subtitle else WHITE
                    indent = 25 if not line.startswith("  ") else 40
                    
                    if current_y > -20 and current_y < content_height:
                        line_surf = self.font_text.render(line, True, color)
                        temp_surface.blit(line_surf, (indent, current_y))
                
                current_y += 15

            current_y += 25  # Espaciado entre secciones

        # Blit superficie a pantalla
        self.screen.blit(temp_surface, (content_x, content_y))

        # Barra de scroll mejorada
        if self.max_scroll > 0:
            # Background de la barra
            scroll_bg_rect = pygame.Rect(self.x + self.width - 18, self.y + 70, 12, self.height - 85)
            pygame.draw.rect(self.screen, (40, 40, 40), scroll_bg_rect, border_radius=6)
            
            # Barra de scroll
            scroll_bar_height = max(30, (self.height - 85) * (self.height - 85) / (self.max_scroll + self.height - 85))
            scroll_bar_y = self.y + 70 + (self.scroll_offset / self.max_scroll) * (self.height - 85 - scroll_bar_height)
            scroll_bar_rect = pygame.Rect(self.x + self.width - 17, scroll_bar_y, 10, scroll_bar_height)
            
            pygame.draw.rect(self.screen, MENU_GLOW, scroll_bar_rect, border_radius=5)
            pygame.draw.rect(self.screen, WHITE, scroll_bar_rect, 1, border_radius=5)

            # Indicadores de flechas animados
            arrow_pulse = abs(math.sin(self.anim_time / 20)) * 50 + 150
            arrow_color = (int(arrow_pulse), int(arrow_pulse), int(arrow_pulse))
            
            if self.scroll_offset > 0:
                arrow_up = self.font_text.render("▲", True, arrow_color)
                self.screen.blit(arrow_up, (self.x + self.width // 2 - 5, self.y + 72))
            
            if self.scroll_offset < self.max_scroll:
                arrow_down = self.font_text.render("▼", True, arrow_color)
                self.screen.blit(arrow_down, (self.x + self.width // 2 - 5, self.y + self.height - 25))