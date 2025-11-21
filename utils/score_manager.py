import json
import os
from datetime import datetime

class ScoreManager:
    """Gestor de puntuaciones con ranking y desempate por olas."""

    FILE_PATH = "data/scores.json"
    MAX_ENTRIES = 10  # Mantener solo las 10 mejores puntuaciones

    def __init__(self):
        os.makedirs(os.path.dirname(self.FILE_PATH), exist_ok=True)
        self.scores = self._load_scores()
        self._update_positions()

    def _load_scores(self):
        if not os.path.exists(self.FILE_PATH):
            return []
        try:
            with open(self.FILE_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
                if not isinstance(data, list):
                    return []
                # Normalizar entradas antiguas
                for entry in data:
                    if "player" not in entry:
                        entry["player"] = entry.get("name", "Player")
                    if "score" not in entry:
                        entry["score"] = 0
                    if "wave" not in entry:
                        entry["wave"] = 1
                return data
        except Exception as e:
            print(f"[ERROR][ScoreManager] No se pudo cargar JSON: {e}")
        return []

    def add_score(self, player_name, player_score, wave_reached):
        entry = {
            "player": player_name,
            "score": int(player_score),
            "wave": int(wave_reached),
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self.scores.append(entry)
        # Ordenar primero por score desc, luego por wave desc
        self.scores.sort(key=lambda x: (-x["score"], -x["wave"]))
        # Limitar al máximo de entries
        self.scores = self.scores[:self.MAX_ENTRIES]
        self._update_positions()
        self._save_scores()

    def _update_positions(self):
        """Calcula la posición actual de cada jugador, compartiendo posiciones si score y wave iguales."""
        if not self.scores:
            return

        current_position = 1
        last_score = None
        last_wave = None
        shared_count = 0

        for i, entry in enumerate(self.scores):
            if last_score is not None and entry["score"] == last_score and entry["wave"] == last_wave:
                # Mismo score y wave → comparte posición
                entry["position"] = current_position
                shared_count += 1
            else:
                # Nuevo ranking → sumar shared_count
                current_position += shared_count
                entry["position"] = current_position
                shared_count = 1  # este entry cuenta como 1
                last_score = entry["score"]
                last_wave = entry["wave"]

    def _save_scores(self):
        try:
            with open(self.FILE_PATH, "w", encoding="utf-8") as f:
                json.dump(self.scores, f, indent=4)
        except Exception as e:
            print(f"[ERROR][ScoreManager] No se pudo guardar JSON: {e}")

    def get_top_scores(self):
        return self.scores
