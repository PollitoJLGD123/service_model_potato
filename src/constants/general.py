from pathlib import Path

MODEL_DIR = Path(__file__).parent.parent.parent / "model"

MODEL_PATH = MODEL_DIR / "model.keras"

JSON_PATH = MODEL_DIR / "metrics.json"

HISTORY_PATH = MODEL_DIR / "history_efficient.png"