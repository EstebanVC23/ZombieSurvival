import pygame

class EventHandler:
    """Maneja eventos de pygame."""

    def __init__(self, game):
        self.game = game

    def handle_events(self):
        keys = pygame.key.get_pressed()
        self.game.ui_manager.visible = keys[pygame.K_e]

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game.running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.toggle_pause()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.handle_mouse_click(pygame.mouse.get_pos())

    def toggle_pause(self):
        self.game.paused = not self.game.paused
        self.game.current_cursor = self.game.cursor_menu if self.game.paused else self.game.cursor_game
        for z in self.game.zombies:
            try:
                z.pause_sound() if self.game.paused else z.resume_sound()
            except Exception:
                pass

    def handle_mouse_click(self, pos):
        if self.game.lose_menu:
            self.game.lose_menu.handle_click(pos, self.game)
        elif self.game.paused:
            self.game.pause_menu.handle_click(pos, self.game)
        else:
            self.game.player.shoot(pos, self.game)
