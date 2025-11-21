import json
import os
from datetime import datetime

class ScoreManager:
    """Gestor de puntuaciones con ranking y desempate por olas."""

    FILE_PATH = "data/scores.json"
    # REMOVIDO: MAX_ENTRIES - Ahora guardamos TODAS las puntuaciones

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
        # YA NO SE LIMITA - Guardamos todas las puntuaciones
        self._update_positions()
        self._save_scores()

    def _update_positions(self):
        if not self.scores:
            return

        current_position = 1
        prev_score = None
        prev_wave = None

        for i, entry in enumerate(self.scores):
            if i == 0:
                entry["position"] = 1
            else:
                if entry["score"] == prev_score and entry["wave"] == prev_wave:
                    entry["position"] = current_position  # comparte
                else:
                    current_position = i + 1  # nueva posición
                    entry["position"] = current_position

            prev_score = entry["score"]
            prev_wave = entry["wave"]

    def _save_scores(self):
        try:
            with open(self.FILE_PATH, "w", encoding="utf-8") as f:
                json.dump(self.scores, f, indent=4)
        except Exception as e:
            print(f"[ERROR][ScoreManager] No se pudo guardar JSON: {e}")

    def get_top_scores(self):
        return self.scores