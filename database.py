import sqlite3
from pathlib import Path


class DatabaseManager:

    def __init__(self):
        self.db_path = Path(__file__).parent / "database" / "coffee_shops.db"

        self.create_table()

    def create_table(self):
        connection = sqlite3.connect(self.db_path)

        cursor = connection.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS coffee_shops (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                city TEXT NOT NULL,
                rating REAL NOT NULL,
                category TEXT NOT NULL,
                notes TEXT
            )
        """)

        connection.commit()
        connection.close()
