import sqlite3
import os

class Database:
    def __init__(self, database_file_name: str):
        os.makedirs(os.path.dirname(database_file_name), exist_ok=True)
        self.database_file_name = database_file_name
        self.create_tables()

    def create_tables(self):
        with sqlite3.connect(self.database_file_name) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS Users (
                ID INT NOT NULL UNIQUE,
                user_name VARCHAR(255) NOT NULL,
                password VARCHAR(255) NOT NULL,
                PRIMARY KEY (ID)
                )
                """
            )
