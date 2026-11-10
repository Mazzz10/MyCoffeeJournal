
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

    
    def get_shop(self, shop_id):
        """Retrieve one coffee shop using its ID."""

        # Open a new database connection
        connection = self.get_connection()

        try:
            cursor = connection.cursor()

            # Use a placeholder to safely pass the shop ID
            cursor.execute(
                "SELECT * FROM coffee_shops WHERE id = ?",
                (shop_id,)
            )

            # Fetch the matching record
            row = cursor.fetchone()

            # Return a dictionary if found, otherwise None
            return dict(row) if row else None

        finally:
            # Always close the database connection
            connection.close()

    def update_shop(self, shop_id, name, city, rating, category, notes):
        """Update an existing coffee shop."""

        connection = self.get_connection()

        try:
            cursor = connection.cursor()

            # Update the record matching the given ID
            cursor.execute("""
                UPDATE coffee_shops
                SET name = ?,
                    city = ?,
                    rating = ?,
                    category = ?,
                    notes = ?
                WHERE id = ?
            """, (name, city, rating, category, notes, shop_id))

            # Save the changes
            connection.commit()

            # Return True if a record was updated
            return cursor.rowcount > 0

        finally:
            connection.close()

    def delete_shop(self, shop_id):
        """Delete a coffee shop using its ID."""

        connection = self.get_connection()

        try:
            cursor = connection.cursor()

            # Delete only the record with the specified ID
            cursor.execute(
                "DELETE FROM coffee_shops WHERE id = ?",
                (shop_id,)
            )

            # Save the deletion
            connection.commit()

            # Return True if a record was deleted
            return cursor.rowcount > 0

        finally:
            connection.close()

