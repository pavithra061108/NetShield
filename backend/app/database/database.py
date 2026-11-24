import sqlite3
import json

from pathlib import Path
from datetime import datetime, timezone

PROJECT_ROOT = Path(__file__).resolve().parents[3]

DATA_DIR = PROJECT_ROOT / "data"
DATA_DIR.mkdir(exist_ok=True)

DB_PATH = DATA_DIR / "netshield.db"


def get_connection():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database():

    with get_connection() as conn:

        conn.execute("""
            CREATE TABLE IF NOT EXISTS analysis_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                source_file TEXT NOT NULL,
                features TEXT NOT NULL,
                label TEXT NOT NULL,
                probability REAL NOT NULL,
                model TEXT NOT NULL
            )
        """)

        conn.commit()


def save_result(source_file, features, result):

    with get_connection() as conn:

        cursor = conn.execute("""
            INSERT INTO analysis_results (
                timestamp,
                source_file,
                features,
                label,
                probability,
                model
            )
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            datetime.now(timezone.utc).isoformat(),
            source_file,
            json.dumps(features),
            result["label"],
            result["attack_probability"],
            result["model"]
        ))

        conn.commit()

        return cursor.lastrowid


def get_results():

    with get_connection() as conn:

        rows = conn.execute("""
            SELECT * FROM analysis_results
            ORDER BY id DESC
        """).fetchall()

    results = []

    for row in rows:

        item = dict(row)
        item["features"] = json.loads(item["features"])

        results.append(item)

    return results


def get_statistics():

    results = get_results()

    total = len(results)

    benign = sum(
        row["label"] == "BENIGN"
        for row in results
    )

    flagged = sum(
        row["label"] == "ATTACK"
        for row in results
    )

    return {
        "total_flows": total,
        "benign_flows": benign,
        "flagged_flows": flagged,
        "analysis_mode": "Offline demonstration"
    }