import sqlite3
import os

class DatabaseConnection:
    _instance = None  # Singleton instance
    _connection = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseConnection, cls).__new__(cls)
            db_path = os.path.join(os.path.dirname(__file__), 'users.db')
            cls._connection = sqlite3.connect('users.db', check_same_thread=False) 
            cls._connection = sqlite3.connect(db_path, check_same_thread=False)
            cls._cursor = cls._connection.cursor()
        return cls._instance

    def get_cursor(self):
        return self._cursor

    def commit(self):
        self._connection.commit()

    def close(self):
        pass  # Do nothing (keep connection open)