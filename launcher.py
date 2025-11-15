# launcher.py
'''Falta por:
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
- Pantalla de carga
- Final por completar todos los niveles
- Pantalla de puntuaciones altas
- algunas opciones en el menú (sonido, controles, etc)
- Crear la tabla de puntuaciones altas y guardado en archivo'''
from ui.main_menu import main_menu
from core.game import Game

if __name__ == "__main__":
    main_menu()     # mostrar menú
    game = Game()   # lanzar juego principal
    game.run()
