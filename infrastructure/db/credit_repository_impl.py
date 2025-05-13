from datetime import datetime
from core.entities.credit import Credit  
from core.repositories.credit_repository import CreditRepository  
from infrastructure.db.sqlite_db import SQLiteDB


class CreditRepositoryImpl(CreditRepository):
    def __init__(self, db: SQLiteDB):

        self.db = db

    def create(self, credit: Credit) -> Credit:

        conn = self.db.get_connection() 
        cursor = conn.cursor()  

        # новая запись в credits
        cursor.execute(
            """
            INSERT INTO credits
                (user_id, amount, operation_type, timestamp, balance_after)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                credit.user_id,
                credit.amount,
                credit.operation_type,
                credit.timestamp.isoformat(),
                credit.balance_after
            )
        )
        conn.commit()  
        # ID последней вставленной строки = credit
        credit.id = cursor.lastrowid  
        return credit 

    def get_by_id(self, credit_id: int) -> Credit | None:
        conn = self.db.get_connection()
        cursor = conn.cursor()

        # запрос по ID
        cursor.execute("SELECT * FROM credits WHERE id = ?", (credit_id,))
        row = cursor.fetchone()

        if not row:
            return None

        # возвращаем Credit
        return Credit(
            id=row["id"],
            user_id=row["user_id"],
            amount=row["amount"],
            operation_type=row["operation_type"],
            timestamp=datetime.fromisoformat(row["timestamp"]),
            balance_after=row["balance_after"]
        )

    def get_by_user_id(self, user_id: int) -> list[Credit]:
        conn = self.db.get_connection()
        cursor = conn.cursor()

        # для указанного user_id
        cursor.execute("SELECT * FROM credits WHERE user_id = ?", (user_id,))
        rows = cursor.fetchall()  # Извлекаем все строки результата
        # для хранения  Credit
        credits = []
        for row in rows:
            # Для каждой создать Credit и добавить его в список
            credits.append(Credit(
                id=row["id"],
                user_id=row["user_id"],
                amount=row["amount"],
                operation_type=row["operation_type"],
                timestamp=datetime.fromisoformat(row["timestamp"]),
                balance_after=row["balance_after"]
            ))

        return credits

    def get_current_balance(self, user_id: int) -> int:
        conn = self.db.get_connection()
        cursor = conn.cursor()

        # Получаем текущий баланс пользователя из таблицы 'users'
        cursor.execute("SELECT credits FROM users WHERE id = ?", (user_id,))
        row = cursor.fetchone()

        if not row:
            return 0

        return row["credits"] 

    def update(self, credit: Credit) -> Credit:

        conn = self.db.get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            UPDATE credits
            SET user_id        = ?,
                amount         = ?,
                operation_type = ?,
                timestamp      = ?,
                balance_after  = ?
            WHERE id = ?
            """,
            (
                credit.user_id,
                credit.amount,
                credit.operation_type,
                credit.timestamp.isoformat(),
                credit.balance_after,
                credit.id
            )
        )
        conn.commit()

        return credit
