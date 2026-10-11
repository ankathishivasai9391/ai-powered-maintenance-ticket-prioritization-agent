import os
from pathlib import Path

# Base directories
BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"
DATASET_PATH = DATA_DIR / "maintenance_tickets.csv"

# SQLite DB Path
DB_PATH = Path(os.getenv("DB_PATH", str(DATA_DIR / "maintenance.db")))

# Server config
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", 8000))
