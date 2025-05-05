import os
from joblib import dump, load
from core.entities.model import Model
from core.repositories.model_repository import ModelRepository
from infrastructure.db.sqlite_db import SQLiteDB

class ModelRepositoryImpl(ModelRepository):
    def __init__(self, db: SQLiteDB, models_directory: str = "models"):
        self.db = db
        self.models_directory = models_directory
        os.makedirs(self.models_directory, exist_ok=True)

    def _path_for(self, model: Model) -> str:
        # Можно включать ID после первого сохранения, 
        # или timestamp, или версию
        filename = f"{model.name}.pkl"
        return os.path.join(self.models_directory, filename)

    def create(self, model: Model) -> Model:
        conn = self.db.get_connection()
        cursor = conn.cursor()

        # Сохраняем Pipeline/модель на диск
        model_path = self._path_for(model)
        dump(model.model_object, model_path)

        cursor.execute(
            "INSERT INTO models (name, type, credit_cost, model_path) VALUES (?, ?, ?, ?)",
            (model.name, model.type, model.credit_cost, model_path)
        )
        conn.commit()

        model.id = cursor.lastrowid
        return model

    def get_by_id(self, model_id: int) -> Model:
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM models WHERE id = ?", (model_id,))
        row = cursor.fetchone()
        if not row:
            return None

        model_path = row["model_path"]
        # Загружаем обратно
        model_object = load(model_path)

        # Проверка, что у объекта есть predict
        if not hasattr(model_object, "predict"):
            raise ValueError(f"Файл {model_path} не содержит модель с методом predict")

        return Model(
            id=row["id"],
            name=row["name"],
            type=row["type"],
            credit_cost=row["credit_cost"],
            model_object=model_object
        )

    def get_by_name(self, name: str) -> Model:
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM models WHERE name = ?", (name,))
        row = cursor.fetchone()
        if not row:
            return None

        model_object = load(row["model_path"])
        return Model(
            id=row["id"],
            name=row["name"],
            type=row["type"],
            credit_cost=row["credit_cost"],
            model_object=model_object
        )

    def get_all(self) -> list[Model]:
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, type, credit_cost FROM models")
        rows = cursor.fetchall()
        return [
            Model(id=r["id"], name=r["name"], type=r["type"], credit_cost=r["credit_cost"])
            for r in rows
        ]

    def update(self, model: Model) -> Model:
        conn = self.db.get_connection()
        cursor = conn.cursor()

        # Пересохраняем объект, если он был передан
        model_path = None
        if model.model_object is not None:
            model_path = self._path_for(model)
            dump(model.model_object, model_path)
        else:
            cursor.execute("SELECT model_path FROM models WHERE id = ?", (model.id,))
            row = cursor.fetchone()
            model_path = row["model_path"]

        cursor.execute(
            "UPDATE models SET name = ?, type = ?, credit_cost = ?, model_path = ? WHERE id = ?",
            (model.name, model.type, model.credit_cost, model_path, model.id)
        )
        conn.commit()
        return model

    def delete(self, model_id: int) -> bool:
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT model_path FROM models WHERE id = ?", (model_id,))
        row = cursor.fetchone()
        if row and os.path.exists(row["model_path"]):
            os.remove(row["model_path"])
        cursor.execute("DELETE FROM models WHERE id = ?", (model_id,))
        conn.commit()
        return cursor.rowcount > 0
