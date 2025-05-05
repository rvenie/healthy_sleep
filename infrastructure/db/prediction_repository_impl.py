import json
from datetime import datetime
from core.entities.prediction import Prediction
from core.repositories.prediction_repository import PredictionRepository
from infrastructure.db.sqlite_db import SQLiteDB


class PredictionRepositoryImpl(PredictionRepository):
    def __init__(self, db: SQLiteDB):
        self.db = db

    def create(self, prediction: Prediction) -> Prediction:
        conn = self.db.get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO predictions
            (user_id, model_id, input_data, prediction_result, timestamp, credits_spent)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                prediction.user_id,
                prediction.model_id,
                json.dumps(prediction.input_data),
                str(prediction.prediction_result),
                prediction.timestamp.isoformat(),
                prediction.credits_spent
            )
        )
        conn.commit()

        prediction.id = cursor.lastrowid
        return prediction

    def get_by_id(self, prediction_id: int) -> Prediction:
        conn = self.db.get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM predictions WHERE id = ?", (prediction_id,))
        row = cursor.fetchone()

        if not row:
            return None

        return Prediction(
            id=row["id"],
            user_id=row["user_id"],
            model_id=row["model_id"],
            input_data=json.loads(row["input_data"]),
            prediction_result=row["prediction_result"],
            timestamp=datetime.fromisoformat(row["timestamp"]),
            credits_spent=row["credits_spent"]
        )

    def get_by_user_id(self, user_id: int) -> list[Prediction]:
        conn = self.db.get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM predictions WHERE user_id = ?", (user_id,))
        rows = cursor.fetchall()

        predictions = []
        for row in rows:
            predictions.append(Prediction(
                id=row["id"],
                user_id=row["user_id"],
                model_id=row["model_id"],
                input_data=json.loads(row["input_data"]),
                prediction_result=row["prediction_result"],
                timestamp=datetime.fromisoformat(row["timestamp"]),
                credits_spent=row["credits_spent"]
            ))

        return predictions

    def update(self, prediction: Prediction) -> Prediction:
        conn = self.db.get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            UPDATE predictions
            SET user_id           = ?,
                model_id          = ?,
                input_data        = ?,
                prediction_result = ?,
                timestamp         = ?,
                credits_spent     = ?
            WHERE id = ?
            """,
            (
                prediction.user_id,
                prediction.model_id,
                json.dumps(prediction.input_data),
                str(prediction.prediction_result),
                prediction.timestamp.isoformat(),
                prediction.credits_spent,
                prediction.id
            )
        )
        conn.commit()

        return prediction

    def delete(self, prediction_id: int) -> bool:
        conn = self.db.get_connection()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM predictions WHERE id = ?", (prediction_id,))
        conn.commit()

        return cursor.rowcount > 0
