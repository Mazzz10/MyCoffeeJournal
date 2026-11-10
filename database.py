
import sqlite3
from pathlib import Path


class DatabaseManager:

    def __init__(self):
        self.db_path = Path(__file__).parent / "database" / "coffee_shops.db"

        # Ensure the database folder exists
        self.db_path.parent.mkdir(parents=True, exist_ok=True)

        self.create_table()

    def get_connection(self):
        """Create a new database connection."""
        connection = sqlite3.connect(self.db_path)
        connection.row_factory = sqlite3.Row
        return connection

    def create_table(self):
        connection = self.get_connection()

        try:
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

        finally:
            connection.close()

    def add_shop(self, name, city, rating, category, notes):
        """Add a new coffee shop to the database."""
        connection = self.get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute("""
                INSERT INTO coffee_shops
                (name, city, rating, category, notes)
                VALUES (?, ?, ?, ?, ?)
            """, (name, city, rating, category, notes))

            connection.commit()

            return cursor.lastrowid

        finally:
            connection.close()

    def get_all_shops(self):
        """Retrieve all coffee shops from the database."""
        connection = self.get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute("""
                SELECT * FROM coffee_shops
                ORDER BY id
            """)

            rows = cursor.fetchall()

            return [dict(row) for row in rows]

        finally:
            connection.close()
