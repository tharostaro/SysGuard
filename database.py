import sqlite3
from datetime import datetime

DB_NAME = "sysguard.db"


def init_db():
    with sqlite3.connect(DB_NAME) as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS metrics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                metric_name TEXT NOT NULL,
                metric_value REAL NOT NULL,
                timestamp TEXT NOT NULL
            )
        """)


def save_metric(name, value):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with sqlite3.connect(DB_NAME) as connection:
        connection.execute("""
            INSERT INTO metrics (metric_name, metric_value, timestamp)
            VALUES (?, ?, ?)
        """, (name, value, timestamp))


def get_history():
    with sqlite3.connect(DB_NAME) as connection:
        return connection.execute("""
            SELECT metric_name, metric_value, timestamp
            FROM metrics
            ORDER BY id DESC
            LIMIT 10
        """).fetchall()
