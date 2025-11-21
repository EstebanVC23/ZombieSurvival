# core/map_loader.py
import os

from settings import TILE_SIZE, TERRAIN_DEFAULT_LETTER, TERRAIN_LETTER_MAP

# cache interno { normalized_path: matrix }
_MAP_CACHE = {}


def _save_map_to_file(path, mapa):
    """
    Guarda el mapa (lista de listas de caracteres) en un archivo .txt.
    """
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        for fila in mapa:
            f.write("".join(fila) + "\n")


def load_map_file(path, world_width, world_height, force_reload=False):
    """
    Carga un mapa desde archivo .txt (compatible con la firma anterior).
    Si el archivo no existe o está vacío, crea uno relleno con TERRAIN_DEFAULT_LETTER.
    Si el archivo contiene letras inválidas o filas/columnas cortas, las corrige
    (reemplaza letras inválidas por TERRAIN_DEFAULT_LETTER y rellena/recorta).
    Usa cache a menos que force_reload=True.

    Retorna:
        mapa (lista de listas de chars), cols (int), rows (int)
    """

    normalized = os.path.abspath(path)

    # calcular cols/rows esperados según TILE_SIZE (compatibilidad)
    cols = max(1, int(world_width // TILE_SIZE))
    rows = max(1, int(world_height // TILE_SIZE))

    # usar cache si corresponde
    if not force_reload and normalized in _MAP_CACHE:
        matrix = _MAP_CACHE[normalized]
        return matrix, len(matrix[0]), len(matrix)

    # si el archivo no existe -> crear mapa por defecto y guardarlo
    if not os.path.exists(normalized):
        matrix = [[TERRAIN_DEFAULT_LETTER for _ in range(cols)] for _ in range(rows)]
        _save_map_to_file(normalized, matrix)
        _MAP_CACHE[normalized] = matrix
        return matrix, cols, rows

    # leer archivo (no eliminar líneas vacías: las trataremos como filas a rellenar)
    with open(normalized, "r", encoding="utf-8") as f:
        raw_lines = [line.rstrip("\n").replace(" ", "") for line in f.readlines()]

    # si el archivo está vacío o todas las líneas son vacías -> crear mapa por defecto
    if not raw_lines or all(line == "" for line in raw_lines):
        matrix = [[TERRAIN_DEFAULT_LETTER for _ in range(cols)] for _ in range(rows)]
        _save_map_to_file(normalized, matrix)
        _MAP_CACHE[normalized] = matrix
        return matrix, cols, rows

    # procesar líneas: validar caracteres, rellenar/recortar columnas y filas
    changed = False
    matrix = []

    # número de líneas leídas (puede ser < rows o > rows)
    for y in range(rows):
        if y < len(raw_lines) and raw_lines[y] != "":
            line = raw_lines[y]
            # validar y transformar cada carácter
            row_chars = []
            for ch in line:
                # si el char no está en el map de terrains -> reemplazar por default
                if ch not in TERRAIN_LETTER_MAP:
                    row_chars.append(TERRAIN_DEFAULT_LETTER)
                    changed = True
                else:
                    row_chars.append(ch)
            # si la fila es más corta que cols -> rellenar
            if len(row_chars) < cols:
                row_chars.extend([TERRAIN_DEFAULT_LETTER] * (cols - len(row_chars)))
                changed = True
            # si la fila es más larga -> recortar
            if len(row_chars) > cols:
                row_chars = row_chars[:cols]
                changed = True
        else:
            # fila faltante o vacía -> rellenar con default
            row_chars = [TERRAIN_DEFAULT_LETTER] * cols
            changed = True

        matrix.append(row_chars)

    # si había más filas de las esperadas, ignorarlas (pero no modificamos el archivo salvo que changed=True)
    # matrix ya tiene exactamente 'rows' filas.

    # si detectamos cambios en validación/normalización, sobrescribimos el archivo con la versión corregida
    if changed:
        try:
            _save_map_to_file(normalized, matrix)
        except Exception:
            # si no podemos guardar, no rompemos el flow: dejamos matrix en memoria
            pass

    # cachear y devolver
    _MAP_CACHE[normalized] = matrix
    return matrix, cols, rows


# utilidades de cache
def clear_map_cache():
    _MAP_CACHE.clear()


def unload_map(path):
    normalized = os.path.abspath(path)
    if normalized in _MAP_CACHE:
        del _MAP_CACHE[normalized]
