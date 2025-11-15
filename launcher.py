# launcher.py
from ui.main_menu import main_menu
from core.game import Game

if __name__ == "__main__":
    main_menu()     # mostrar menú
    game = Game()   # lanzar juego principal
    game.run()
