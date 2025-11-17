# core/game_manager.py

class GameManager:
    """
    Sistema global seguro para acceder al estado del juego,
    evitando usar atributos dinámicos dentro de pygame.display.
    """

    instance = None  # referencia global al Game actual

    @staticmethod
    def get():
        """Devuelve la instancia actual del juego o None."""
        return GameManager.instance

    @staticmethod
    def set(game):
        """Registra la instancia actual del juego."""
        GameManager.instance = game

