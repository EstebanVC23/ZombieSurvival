# 🧟‍♂️ Zombie Survival: Endless Apocalypse

<div align="center">

![Python](https://img.shields.io/badge/Python-3.13+-blue.svg)
![Pygame](https://img.shields.io/badge/Pygame-2.6+-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)
![Status](https://img.shields.io/badge/Status-In%20Development-orange.svg)

**Un juego de supervivencia 2D donde cada partida es única**

[Características](#-características) • [Instalación](#-instalación) • [Controles](#-controles) • [Desarrollo](#-estado-del-desarrollo)

</div>

---

## 📖 Descripción

**Zombie Survival: Endless Apocalypse** es un juego 2D de supervivencia desarrollado en **Python** utilizando **Pygame**. El jugador debe resistir oleadas infinitas de zombis en diferentes mapas cada 10 olas hasta la 100, a partir de la ronda 100, el mapa no cambia, donde cada partida ofrece un entorno único y desafiante.

### 🎯 Concepto Principal
- Supervivencia contra oleadas infinitas de zombis
- Mundo que cambia cada 10 olas hasta la 100 con biomas diversos
- Dificultad progresiva y enemigos variados
- Estética pixel art retro con mecánicas modernas

---

## ✨ Características Actuales

### ⚔️ Sistema de Combate
- **Disparo dinámico:** El jugador dispara hacia el centro de una mira personalizada
- **Colisiones realistas:** Sistema de detección preciso entre balas, jugador y enemigos
- **Múltiples armas:** Sistema modular de rareza y niveles diferentes de zombies
- **Feedback visual:** Efectos al impactar y eliminar enemigos

### 🧟‍♂️ Sistema de Enemigos
- **Zombis comunes:** Velocidad y resistencia estándar
- **Zombis rápidos:** Mayor velocidad, menor resistencia
- **Zombis tanque:** Alta resistencia, movimiento lento
- **Zombis jefe:** Aparecen en oleadas especiales con estadísticas superiores
- **Generación por oleadas:** Sistema Wave Manager que aumenta progresivamente la dificultad

### 🎮 Jugabilidad
- **Movimiento fluido:** Desplazamiento en 8 direcciones (WASD + diagonales)
- **Cámara dinámica:** Seguimiento suave del jugador por el mapa
- **Sistema de oleadas:** Enemigos aparecen en grupos progresivamente más grandes
- **Puntuación:** Sistema de score que registra el desempeño del jugador

### 🖼️ Interfaz Visual
- **HUD estilo pixel art:** 
  - Barra de vida del jugador
  - Contador de puntuación
  - Número de oleada actual
  - Zombis restantes en la oleada
- **Menú principal animado:** Efectos hover y transiciones suaves
- **Menú de pausa:** Fondo translúcido con opciones interactivas
- **Cursores personalizados:**
  - Mira de combate durante el juego
  - Cursor de menú en interfaces

### 🎨 Diseño Artístico
- **Fuente principal:** Press Start 2P (estilo retro)
- **Texturas pixel art:** Sprites optimizados con transparencia
- **Paleta de colores:** Diseño coherente inspirado en juegos clásicos
- **Animaciones:** Movimiento y efectos visuales fluidos

---

## 🗺️ Generación Procedural de Mapas

### 🚧 Estado Actual: En Desarrollo

El sistema de generación procedural está siendo implementado para crear mundos únicos en cada partida.

#### 🔧 Tecnologías Implementadas
- **Texturas preparadas:** Assets completos para todos los biomas planificados

#### 🌍 Biomas Planificados

<table>
<tr>
<th>Bioma</th>
<th>Terreno</th>
<th>Vegetación</th>
<th>Características</th>
</tr>
<tr>
<td>🏜️ <b>Desierto</b></td>
<td>Arena</td>
<td>Cactus, rocas áridas</td>
<td>Visibilidad alta, pocos obstáculos</td>
</tr>
<tr>
<td>🌲 <b>Bosque</b></td>
<td>Pasto verde</td>
<td>Árboles, arbustos, flores</td>
<td>Bioma equilibrado, cobertura media</td>
</tr>
<tr>
<td>🌨️ <b>Taiga</b></td>
<td>Nieve</td>
<td>Pinos, hielo</td>
<td>Visibilidad reducida, terreno resbaladizo</td>
</tr>
<tr>
<td>🌿 <b>Pantano</b></td>
<td>Barro</td>
<td>Árboles secos, agua estancada</td>
<td>Movimiento lento, alta densidad de vegetación</td>
</tr>
<tr>
<td>⛰️ <b>Montaña</b></td>
<td>Piedra</td>
<td>Rocas, nieve en picos</td>
<td>Terreno irregular, enemigos más fuertes</td>
</tr>
<tr>
<td>🌾 <b>Pradera</b></td>
<td>Pasto seco</td>
<td>Arbustos dispersos</td>
<td>Espacios abiertos, combate a distancia</td>
</tr>
</table>

```

#### 🌳 Decoraciones Ambientales Planificadas
- **Árboles:** Roble, pino, seco, tropical
- **Vegetación:** Arbustos, flores, hierba alta, cactus
- **Elementos naturales:** Rocas, agua, nieve, arena
- **Estructuras:** Ruinas, objetos abandonados (futuro)

---

## 🏗️ Arquitectura del Proyecto
```
ZombieSurvival/
├── launcher.py
├── settings.py
├── 📂 assets/
│   ├── 📂 fonts/
│   │   └── PressStart2P.ttf
│   ├── 📂 images/
│   │   ├── 📂 player/
│   │   │   ├── player_idle.png
│   │   │   └── player_run.png
│   │   ├── 📂 zombie/
│   │   │   ├── zombie_common.png
│   │   │   ├── zombie_fast.png
│   │   │   ├── zombie_tank.png
│   │   │   └── zombie_boss.png
│   │   ├── 📂 terrain/
│   │   │   ├── grass.png
│   │   │   ├── sand.png
│   │   │   ├── snow.png
│   │   │   ├── mud.png
│   │   │   └── stone.png
│   │   ├── 📂 objects/
│   │   │   ├── tree_oak.png
│   │   │   ├── tree_pine.png
│   │   │   ├── cactus.png
│   │   │   ├── rock.png
│   │   │   └── bush.png
│   │   └── 📂 menus/
│   │       ├── menu_background.png
│   │       └── pause_overlay.png
│   └── 📂 ui/
│       ├── crosshair.png
│       ├── cursor_menu.png
│       └── health_bar.png
│
├── core/
│   ├── game_component/
│   ├── camera.py
│   ├── impact.py
│   ├── upgrade.py
│   ├── world.py
│   └── state_manager.py
│
├── entities/
│   ├── player_components/
│   ├── zombie_components/
│   ├── player.py
│   ├── weapon.py
│   ├── bullet.py
│   ├── zombie.py
│   └── spawner.py 
│
├── ui/
│   ├── buttons.py
│   ├── map.py
│   ├── lose_menu.py
│   ├── player_card.py
│   ├── hud.py
│   ├── pause_menu.py
│   ├── main_menu.py
│   ├── loading_screen.py
│   └── buttons.py 
│
├── utils/
│   ├── image_utils.py
│   ├── sound_utils.py
│   ├── movement_utils.py
│   ├── math_utils.py
│   └── helpers.py
│
└── data/
```

---

## 🎮 Controles

<table>
<tr>
<th>Acción</th>
<th>Teclas</th>
</tr>
<tr>
<td><b>Movimiento</b></td>
<td><kbd>W</kbd> <kbd>A</kbd> <kbd>S</kbd> <kbd>D</kbd> o <kbd>↑</kbd> <kbd>←</kbd> <kbd>↓</kbd> <kbd>→</kbd></td>
</tr>
<tr>
<td><b>Disparar</b></td>
<td><kbd>Clic Izquierdo</kbd></td>
</tr>
<tr>
<td><b>Stats</b></td>
<td><kbd>E</kbd></td>
</tr>
<tr>
<td><b>Recargar</b></td>
<td><kbd>R</kbd></td>
</tr>
<tr>
<td><b>Pausar</b></td>
<td><kbd>ESC</kbd></td>
</tr>
<tr>
<td><b>Salir del juego</b></td>
<td><kbd>Alt</kbd> + <kbd>F4</kbd></td>
</tr>
</table>

---

## 💻 Instalación

### Requisitos Previos
- Python 3.13 o superior
- pip (gestor de paquetes de Python)

### Pasos de Instalación
```bash
# 1. Clonar el repositorio
git clone https://github.com/EstebanVC23/ZombieSurvival.git
cd ZombieSurvival

# 2. Instalar dependencias
pip install pygame numpy

# 3. Ejecutar el juego
python launcher.py
```

### Dependencias

| Librería | Versión | Propósito |
|----------|---------|-----------|
| **pygame** | 2.6+ | Motor de juego 2D |
| **Pillow** | (Opcional) | Manipulación avanzada de imágenes |

---

## 🚀 Estado del Desarrollo

### ✅ Completado
- [x] Menú principal con animaciones
- [x] Menú de pausa interactivo
- [x] Sistema de disparo dinámico
- [x] Múltiples tipos de zombis
- [x] Sistema de colisiones
- [x] HUD completo estilo pixel art
- [x] Cámara con seguimiento fluido
- [x] Sistema de oleadas progresivas
- [x] Cursores personalizados
- [x] Texturas de biomas preparadas

### 🚧 En Desarrollo
- [ ] Generación de mapas
- [ ] Transiciones entre biomas
- [ ] Decoraciones ambientales
- [ ] Mini-mapa

### 🔜 Planificado
- [ ] Sistema de experiencia y niveles
- [ ] Mejoras de armas y habilidades
- [ ] Gestión de recursos (munición, botiquines)
- [ ] IA avanzada para zombis (detección de sonido)
- [ ] Modo cooperativo local
- [ ] Sistema de construcción
- [ ] Efectos visuales avanzados (sombras, niebla)
- [ ] Sonido ambiental y música reactiva
- [ ] Sistema de clima dinámico

---

## 🎯 Roadmap

### Versión 0.3 (Actual)
- ✅ Sistema de combate funcional
- ✅ Múltiples enemigos
- 🚧 Generación de mapas procedurales

### Versión 0.4 (Próxima)
- Biomas completamente implementados
- Sistema de decoraciones
- Mini-mapa funcional

### Versión 0.5
- Sistema de progresión del jugador
- Mejoras de armas
- Gestión de recursos

### Versión 1.0 (Release)
- Mundo infinito completamente funcional
- Modo cooperativo
- Sistema de logros
- Múltiples armas y habilidades

---

## 🛠️ Tecnologías Utilizadas

<div align="center">

| Tecnología | Versión | Uso |
|:----------:|:-------:|:---:|
| ![Python](https://img.shields.io/badge/Python-3.13+-3776AB?logo=python&logoColor=white) | 3.13+ | Lenguaje principal |
| ![Pygame](https://img.shields.io/badge/Pygame-2.6+-00AA00?logo=python&logoColor=white) | 2.6+ | Motor de juego 2D |
| **Noise** | 1.2+ | Generación procedural |
| **Pillow** | Opcional | Procesamiento de imágenes |

</div>

---

## 📚 Documentación Técnica

### Sistema de Oleadas
```python
# Progresión de dificultad
Wave 1-5:   Zombis comunes
Wave 6-10:  Zombis comunes + rápidos
Wave 11-15: Todos los tipos + aumento de cantidad
Wave 16+:   Zombis jefe + oleadas masivas
```

### Sistema de Puntuación
```python
Zombie Común:  +10 puntos
Zombie Rápido: +15 puntos
Zombie Tanque: +25 puntos
Zombie Jefe:   +50 puntos
Bonus Oleada:  +100 puntos
```

---

## 🎨 Guía de Estilo Visual

### Paleta de Colores Principal
- **Interfaz:** `#2C3E50` (Azul oscuro), `#ECF0F1` (Blanco humo)
- **Jugador:** `#3498DB` (Azul brillante)
- **Enemigos:** `#27AE60` (Verde zombi)
- **Peligro:** `#E74C3C` (Rojo)
- **Éxito:** `#2ECC71` (Verde)

### Especificaciones de Assets
- **Formato:** PNG con transparencia
- **Resolución:** Sprites de 64x64px (escalables)
- **Estilo:** Pixel art con paleta limitada
- **Animaciones:** 4-8 frames por ciclo

---

## 🤝 Contribuciones

Este proyecto es parte de un trabajo académico, pero se aceptan sugerencias y reportes de bugs.

### ¿Cómo contribuir?
1. Fork el repositorio
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

---

## 📝 Notas de Desarrollo

### Consideraciones Técnicas
- Todos los assets deben tener **fondo transparente** (`.png`)
- La fuente **Press Start 2P** es obligatoria para mantener la coherencia visual
- El código está estructurado de manera modular para facilitar la expansión
- Se utiliza un sistema de coordenadas con origen en (0, 0) en la esquina superior izquierda

### Optimización
- Sistema de cámara optimizado para renderizar solo elementos visibles
- Generación de chunks para evitar cargar el mapa completo
- Pooling de objetos para balas y enemigos (planificado)

---

## 👨‍💻 Autor

**Esteban Vásquez Castañeda**  
📧 Email: [tu_email@utp.edu.co]  
🎓 Universidad Tecnológica de Pereira  
💼 Ingeniería de Sistemas y Computación

---

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.

---

## 🙏 Agradecimientos

- **Comunidad de Pygame** por la documentación y recursos
- **Universidad Tecnológica de Pereira** por el apoyo académico
- **Desarrolladores independientes** que inspiran la creación de juegos creativos
- Comunidad de **pixel art** por los recursos y tutoriales

---

## 🔮 Visión del Proyecto

> *"Zombie Survival: Endless Apocalypse busca combinar la nostalgia de los juegos clásicos con mecánicas modernas de generación procedural, ofreciendo una experiencia única en cada partida donde la estrategia, los reflejos y la adaptabilidad son clave para la supervivencia."*

### Objetivos a Largo Plazo
- 🌍 Crear un mundo verdaderamente infinito y explorable
- 🎮 Implementar mecánicas de juego profundas y satisfactorias
- 🧠 Desarrollar una IA desafiante pero justa
- 🎨 Mantener una identidad visual cohesiva y atractiva
- 🔊 Integrar audio y música que mejore la inmersión

---

## 📊 Estadísticas del Proyecto
```
Líneas de código:    ~2,500+
Archivos Python:     15+
Assets gráficos:     50+
Tiempo desarrollo:   En curso
Versión actual:      0.3-alpha
```

---

<div align="center">

### 💀 "No hay final para el apocalipsis... solo sobrevivientes que aprenden a disparar mejor." 💀

**¿Cuánto tiempo podrás sobrevivir?**

---

[![Python](https://img.shields.io/badge/Made%20with-Python-blue?logo=python&logoColor=white)](https://www.python.org/)
[![Pygame](https://img.shields.io/badge/Powered%20by-Pygame-green?logo=python&logoColor=white)](https://www.pygame.org/)
[![UTP](https://img.shields.io/badge/Universidad-UTP-red)](https://www.utp.edu.co/)

**[⬆ Volver arriba](#-zombie-survival-endless-apocalypse)**

</div>