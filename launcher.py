# launcher.py
'''Falta por:
- agregar card de mejora de cantidad de vida y aumento de daño de arma
- Ajustar daños y vida de zombies (settings.py)
- Ajustar puntos por matar zombies (settings.py)
- Generar mundos por cada narrativa en el juego(niveles)
- Crear la narrativa del juego (textos, diálogos, etc)
- faltan sprites de algunos zombies
- Ajustar spawn de mejoras (upgrades) y su balance
- Ajustar sonidos (volúmenes, efectos, etc)
- Testeo general y pulido final
- Optimización si es necesaria
- Empaquetado final del juego
- Final por completar todos los niveles
- Pantalla de puntuaciones altas
- algunas opciones en el menú (sonido, controles, etc)
- Crear la tabla de puntuaciones altas y guardado en archivo'''
import pygame, sys
from ui.main_menu import main_menu
from core.game import Game

if __name__ == "__main__":
    pygame.init()

    while True:
        # Mostrar menú principal
        option = main_menu()  # Devuelve "START_GAME" o "EXIT"

        if option == "EXIT":
            pygame.quit()
            sys.exit()
        elif option == "START_GAME":
            # Crear instancia de juego
            game = Game()
            game.load_resources()
            game.run()

            # Si no se quiere volver al menú principal, salir del launcher
            if not game.return_to_main_menu:
                break
