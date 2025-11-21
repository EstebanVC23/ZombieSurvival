import pygame
from ui.buttons import ButtonTextOnly, Buttons
from ui.main_menu import MenuAssets
from colors import WHITE, DARK_BG, DARK_GREY, MENU_GLOW
from ui.main_menu_components.menu_visual_fx import MenuVisualFX


class MenuUI:
    def __init__(self, assets: MenuAssets):
        self.assets = assets
        menu_items = ["START GAME", "HIGH SCORES", "HELP", "EXIT"]
        menu_positions = [
            (assets.SCREEN_WIDTH//2, 400),
            (assets.SCREEN_WIDTH//2, 460),
            (assets.SCREEN_WIDTH//2, 520),
            (assets.SCREEN_WIDTH//2, 580)
        ]
        buttons_list = [
            ButtonTextOnly(text, pos,
                           "assets/fonts/PressStart2P-Regular.ttf",
                           base_size=28,
                           hover_size=32,
                           text_color=WHITE,
                           hover_color=MENU_GLOW)
            for text, pos in zip(menu_items, menu_positions)
        ]
        self.menu_buttons = Buttons(assets.screen, buttons_list)

    def draw(self):
        screen = self.assets.screen
        panel = pygame.Rect(100, 360,
                            self.assets.SCREEN_WIDTH-200, 250)
        panel_surf = pygame.Surface(panel.size, pygame.SRCALPHA)
        panel_surf.fill((*DARK_BG,150))
        screen.blit(panel_surf, panel.topleft)
        MenuVisualFX.draw_animated_border(screen, panel, DARK_GREY, 2, 2)
        self.menu_buttons.draw()