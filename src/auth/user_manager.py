import sqlite3
import os

class UserManager:
    def __init__(self, db_path: str = "config/users.db"):
        self.db_path = db_path

        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        
        conn = self._get_connection()
        conn.cursor().execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                username TEXT UNIQUE,
                password_hash TEXT,
                public_key TEXT
            )    
            """
        )

        conn.commit()
        conn.close()

    def register_user(self, username: str, password_hash: str, public_key: str) -> bool:
        try:
            conn = self._get_connection()
            conn.cursor().execute(
                """
                INSERT INTO users (username, password_hash, public_key)
                VALUES (?, ?, ?)
                """, 
                (username, password_hash, public_key)
            )
            conn.commit()
            conn.close()
            return True  
        except sqlite3.IntegrityError:
            return False  

    def authenticate(self,username: str, password_hash: str) -> bool:
        conn = self._get_connection()

        result = conn.cursor().execute(
            """
            SELECT password_hash FROM users WHERE username=? 
            """,
            (username,)
        ).fetchone()

        conn.close()

        if result is None: return False
        return result[0] == password_hash

    def delete_user(self,username: str):
        conn = self._get_connection()

        conn.cursor().execute(
            """
            DELETE FROM users WHERE username=?
            """,
            (username,)
        )

        conn.commit()
        changes = conn.total_changes > 0
        conn.close()

        return changes

    def get_all_users(self) -> list[str]:
        conn = self._get_connection()

        result = conn.cursor().execute(
            "SELECT username FROM users ORDER BY username"
        ).fetchall()

        conn.close()

        return [row[0] for row in result]

    def _get_connection(self):
        return sqlite3.connect(self.db_path)
