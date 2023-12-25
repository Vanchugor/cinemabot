import sqlite3
import typing as tp

from cinemabot.definitions import DEFAULT_DB_FILE


class DBManager:
    def __init__(self, db_file_path: str = DEFAULT_DB_FILE) -> None:
        self.db_file_path = db_file_path

    def __enter__(self) -> "DBManager":
        self.connection = sqlite3.connect(self.db_file_path)
        self.cursor = self.connection.cursor()

        self.make_dbs()
        return self

    def __exit__(self, exc_type: tp.Any, exc_val: tp.Any, exc_tb: tp.Any) -> None:
        self.cursor.close()
        self.connection.close()

    def make_dbs(self) -> None:
        # self.cursor.execute('''
        # CREATE TABLE IF NOT EXISTS Users (
        # id INTEGER PRIMARY KEY,
        # full_name TEXT NOT NULL,
        # reg_date TEXT NOT NULL
        # )
        # ''')

        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS Films (
        id INTEGER PRIMARY KEY,
        title TEXT NOT NULL,
        genre TEXT NOT NULL,
        year TEXT NOT NULL,
        links TEXT NOT NULL,
        info TEXT NOT NULL,
        rate TEXT NOT NULL,
        poster TEXT NOT NULL
        )
        ''')

        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS Requests (
        id INTEGER PRIMARY KEY,
        film_id INTEGER NOT NULL,
        user_id INTEGER NOT NULL,
        reply_message_id INTEGER NOT NULL,
        request_date TEXT NOT NULL
        )
        ''')

    def find_recent_films_by_user_id_with_limit(self, user_id: int, limit: int) -> list[tuple]:
        self.cursor.execute('''
        SELECT Films.title, Films.year, Requests.reply_message_id
        FROM Requests INNER JOIN Films ON Films.id = Requests.film_id
        WHERE user_id = ?
        LIMIT ?
        ''', (user_id, limit))

        self.connection.commit()
        return self.cursor.fetchall()

    def find_film_by_name(self, film_title: str) -> list[tuple]:
        self.cursor.execute('''
        SELECT *
        FROM Films
        WHERE title = ?
        ''', (film_title,))

        self.connection.commit()
        return self.cursor.fetchall()

    def find_requests_by_film_id_and_user_id(self, film_id: int, user_id: int) -> list[tuple]:
        self.cursor.execute('''
        SELECT *
        FROM Requests
        WHERE film_id = ? AND user_id = ?
        ''', (film_id, user_id))

        self.connection.commit()
        return self.cursor.fetchall()

    def find_requests_by_reply_message_id_and_user_id(self, message_id, user_id: int):
        self.cursor.execute('''
        SELECT *
        FROM Requests
        WHERE reply_message_id = ? AND user_id = ?
        ''', (message_id, user_id))

        self.connection.commit()
        return self.cursor.fetchall()

    def insert_film(self, *args):
        norm = ["None" if arg is None else arg for arg in args]

        self.cursor.execute('''
        INSERT INTO Films (title, genre, year, links, info, rate, poster)
        VALUES(?, ?, ?, ?, ?, ?, ?) 
        ''', norm)

        self.connection.commit()
        return self.cursor.lastrowid

    def insert_request(self, film_id, user_id, message_id):
        self.cursor.execute('''
        INSERT INTO Requests (film_id, user_id, reply_message_id, request_date)
        VALUES(?, ?, ?, DATETIME('now')) 
        ''', (film_id, user_id, message_id))

        self.connection.commit()
        return self.cursor.lastrowid
