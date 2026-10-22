"""SQLite history of every detection run."""
import json
import sqlite3
from datetime import datetime

import pandas as pd

from backend.config import DB_PATH


def _connect():
    return sqlite3.connect(DB_PATH)


def init_db() -> None:
    """Create the history table if it does not exist yet."""
    with _connect() as conn:
        conn.execute(
            """CREATE TABLE IF NOT EXISTS history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                source_type TEXT,
                filename TEXT,
                model_name TEXT,
                conf REAL,
                num_objects INTEGER,
                inference_ms REAL,
                class_counts_json TEXT
            )"""
        )


def save_record(source_type, filename, model_name, conf, num_objects, inference_ms, class_counts) -> None:
    """Store one run. class_counts is a dict like {"person": 3}."""
    init_db()
    with _connect() as conn:
        conn.execute(
            "INSERT INTO history (timestamp, source_type, filename, model_name, conf, "
            "num_objects, inference_ms, class_counts_json) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), source_type, filename, model_name,
             float(conf), int(num_objects), float(inference_ms), json.dumps(class_counts)),
        )


def get_history() -> pd.DataFrame:
    """Return all runs, newest first."""
    init_db()
    with _connect() as conn:
        return pd.read_sql_query("SELECT * FROM history ORDER BY id DESC", conn)


def clear_history() -> None:
    """Delete all runs."""
    init_db()
    with _connect() as conn:
        conn.execute("DELETE FROM history")
