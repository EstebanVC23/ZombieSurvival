import pygame
from utils.helpers import load_image_safe

class MenuAssets:
    SCREEN_WIDTH = 700
    SCREEN_HEIGHT = 700
    FPS = 60

    def __init__(self):
        self.screen = pygame.display.set_mode(
            (self.SCREEN_WIDTH, self.SCREEN_HEIGHT), pygame.NOFRAME
        )
        pygame.display.set_caption("Zombie Survival: Endless Apocalypse")
        self.clock = pygame.time.Clock()
        self.background = self.load_background()
        self.base_font, self.title_font = self.load_fonts()
        pygame.mouse.set_visible(False)
        self.cursor_menu = self.load_cursor("ui/cursor_menu.png", (20, 20))

    def load_background(self):
        bg = load_image_safe("menus/menu_bg.png")
        if bg:
            return pygame.transform.scale(bg, (self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        surf = pygame.Surface((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        surf.fill((10, 10, 10))
        return surf

    def load_fonts(self):
        font_path = "assets/fonts/PressStart2P-Regular.ttf"
        try:
            base = pygame.font.Font(font_path, 28)
            title = pygame.font.Font(font_path, 48)
        except:
            base = pygame.font.Font(None, 28)
            title = pygame.font.Font(None, 48)
        return base, title

    def load_cursor(self, path, size):
        img = load_image_safe(path)
        if not img:
            return None
        img = pygame.transform.scale(img, size)
        img.lock()
        for x in range(img.get_width()):
            for y in range(img.get_height()):
                r, g, b, a = img.get_at((x, y))
                if a > 0 and (r+g+b)/3 > 210:
                    img.set_at((x,y), (0,0,0,0))
        img.unlock()
        return img