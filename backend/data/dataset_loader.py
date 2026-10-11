
import csv
from typing import List, Dict, Any
from pathlib import Path
from backend.config import DATASET_PATH


REQUIRED_COLUMNS = {"ticket_id", "asset_type", "description", "target_severity", "target_category"}

def load_dataset(csv_path: Path = DATASET_PATH) -> List[Dict[str, Any]]:
    """
    Safely load and validate the maintenance tickets CSV dataset.
    Returns a list of dictionaries.
    """
    if not csv_path.exists():
        return []
    
    records: List[Dict[str, Any]] = []
    try:
        with open(csv_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            # Validate columns
            missing = REQUIRED_COLUMNS - set(reader.fieldnames or [])
            if missing:
                raise ValueError(f"CSV missing required columns: {missing}")
            for row in reader:
                # Ensure required keys and strip whitespace
                cleaned = {k: (v.strip() if isinstance(v, str) else "") for k, v in row.items() if k in REQUIRED_COLUMNS}
                # Fill missing keys with empty string
                for key in REQUIRED_COLUMNS:
                    cleaned.setdefault(key, "")
                records.append(cleaned)
        return records
    except Exception as e:
        # Return fallback empty list on error
        return []

def get_historical_records(csv_path: Path = DATASET_PATH) -> List[Dict[str, Any]]:
    """
    Returns list of dicts representing historical benchmark dataset.
    """
    return load_dataset(csv_path)
