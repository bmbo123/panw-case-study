import json
import os
from datetime import datetime

DATA_FILE = "data/journal.json"


def ensure_data_dir():
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)


def load_entries() -> list:
    ensure_data_dir()
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return []


def save_entries(entries: list) -> bool:
    ensure_data_dir()
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(entries, f, indent=2, ensure_ascii=False)
        return True
    except IOError:
        return False


def append_entry(text: str, analysis: dict) -> dict:
    entries = load_entries()
    entry = {
        "timestamp": datetime.now().isoformat(),
        "text": text,
        "mood": analysis.get("mood", "neutral"),
        "energy": analysis.get("energy", "medium")
    }
    entries.append(entry)
    save_entries(entries)
    return entry


def get_last_entries(n: int = 3) -> list:
    entries = load_entries()
    return entries[-n:] if entries else []


def clear_entries() -> bool:
    return save_entries([])
