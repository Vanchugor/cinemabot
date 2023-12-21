import sqlite3
import typing as tp

from cinemabot.definitions import DEFAULT_DB_FILE


class DBConnector:
    def __init__(self, db_file_path: str = DEFAULT_DB_FILE) -> None:
        self.db_file_path = db_file_path

    def __enter__(self) -> sqlite3.Cursor:
        self.connection = sqlite3.connect(self.db_file_path)
        self.cursor = self.connection.cursor()

        self.make_dbs()
        return self.cursor

    def __exit__(self, exc_type: tp.Any, exc_val: tp.Any, exc_tb: tp.Any) -> None:
        self.cursor.close()
        self.connection.close()

    def make_dbs(self) -> None:
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS Users (
        id INTEGER PRIMARY KEY,
        full_name TEXT NOT NULL,
        reg_date TEXT NOT NULL
        )
        ''')

        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS Films (
        id INTEGER PRIMARY KEY,
        title TEXT NOT NULL,
        genre TEXT NOT NULL,
        year INTEGER NOT NULL,
        links TEXT NOT NULL
        )
        ''')

        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS Requests (
        id INTEGER PRIMARY KEY,
        film_id INTEGER NOT NULL,
        user_id INTEGER NOT NULL,
        request_date TEXT NOT NULL
        )
        ''')
