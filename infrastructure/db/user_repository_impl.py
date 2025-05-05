import json
from core.entities.user import User
from core.repositories.user_repository import UserRepository
from infrastructure.db.sqlite_db import SQLiteDB


class UserRepositoryImpl(UserRepository):
    def __init__(self, db: SQLiteDB):
        self.db = db

    def create(self, user: User) -> User:
        conn = self.db.get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO users (username, password_hash, email, credits) VALUES (?, ?, ?, ?)",
            (user.username, user.password_hash, user.email, user.credits)
        )
        conn.commit()

        user.id = cursor.lastrowid
        return user

    def get_by_id(self, user_id: int) -> User:
        conn = self.db.get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        row = cursor.fetchone()

        if not row:
            return None

        return User(
            id=row["id"],
            username=row["username"],
            password_hash=row["password_hash"],
            email=row["email"],
            credits=row["credits"]
        )

    def get_by_username(self, username: str) -> User:
        conn = self.db.get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        row = cursor.fetchone()

        if not row:
            return None

        return User(
            id=row["id"],
            username=row["username"],
            password_hash=row["password_hash"],
            email=row["email"],
            credits=row["credits"]
        )

    def update(self, user: User) -> User:
        conn = self.db.get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "UPDATE users SET username = ?, password_hash = ?, email = ?, credits = ? WHERE id = ?",
            (user.username, user.password_hash, user.email, user.credits, user.id)
        )
        conn.commit()

        return user

    def delete(self, user_id: int) -> bool:
        conn = self.db.get_connection()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
        conn.commit()

        return cursor.rowcount > 0
