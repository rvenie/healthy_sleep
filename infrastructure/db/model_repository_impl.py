import os
from joblib import dump, load
from core.entities.model import Model
from core.repositories.model_repository import ModelRepository
from infrastructure.db.sqlite_db import SQLiteDB

class ModelRepositoryImpl(ModelRepository):
    def __init__(self, db: SQLiteDB, models_directory: str = "models"):

        self.db = db
        self.models_directory = models_directory
        # если не существует
        os.makedirs(self.models_directory, exist_ok=True)

    def _path_for(self, model: Model) -> str:
        # Название файла модели
        filename = f"{model.name}.pkl" 
        return os.path.join(self.models_directory, filename)

    def create(self, model: Model) -> Model:
        conn = self.db.get_connection()
        cursor = conn.cursor()

        # Путь для сохранения модели на диске
        model_path = self._path_for(model)
        dump(model.model_object, model_path)

        # Модель в базе
        cursor.execute(
            "INSERT INTO models (name, type, credit_cost, model_path) VALUES (?, ?, ?, ?)",
            (model.name, model.type, model.credit_cost, model_path)
        )
        conn.commit()
        model.id = cursor.lastrowid 
        return model

    def get_by_id(self, model_id: int) -> Model | None:
        conn = self.db.get_connection()
        cursor = conn.cursor()
        # по id
        cursor.execute("SELECT * FROM models WHERE id = ?", (model_id,))
        row = cursor.fetchone()

        if not row:
            return None

        model_path = row["model_path"]
        # Загружаем модель с диска
        model_object = load(model_path)

        # Проверка на формат
        if not hasattr(model_object, "predict"):
            raise ValueError(f"Файл {model_path} не содержит объект модели с методом predict")

        # Возврщаем модель
        return Model(
            id=row["id"],
            name=row["name"],
            type=row["type"],
            credit_cost=row["credit_cost"],
            model_object=model_object
        )

    def get_by_name(self, name: str) -> Model | None:
        conn = self.db.get_connection()
        cursor = conn.cursor()
        # Для обращения по имени
        cursor.execute("SELECT * FROM models WHERE name = ?", (name,))
        row = cursor.fetchone()

        if not row:
            return None

        # Загружаем 
        model_object = load(row["model_path"])
        # Возвращаем
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
        # Просто собрать все имеющиеся модели
        cursor.execute("SELECT id, name, type, credit_cost FROM models")
        rows = cursor.fetchall()  # Извлекаем все строки результата
        # Вовзращаем список
        return [
            Model(id=r["id"], name=r["name"], type=r["type"], credit_cost=r["credit_cost"])
            for r in rows
        ]

    def update(self, model: Model) -> Model:
        conn = self.db.get_connection()
        cursor = conn.cursor()

        model_path = None
        # Если в переданном объекте Model есть новый model_object (не None),
        # то пересохраняем его на диск.
        if model.model_object is not None:
            model_path = self._path_for(model)
            dump(model.model_object, model_path)
        else:
            # Если новый model_object не передан, то оставляем старый путь к файлу.
            # Для этого сначала извлекаем его из БД.
            cursor.execute("SELECT model_path FROM models WHERE id = ?", (model.id,))
            row = cursor.fetchone()
            if row:
                model_path = row["model_path"]
            else:
                # Ситуация, когда модель с таким ID не найдена для обновления, должна обрабатываться.
                raise ValueError(f"Модель с ID {model.id} не найдена для обновления.")


        # Выполняем SQL-запрос на обновление записи в таблице 'models'
        cursor.execute(
            "UPDATE models SET name = ?, type = ?, credit_cost = ?, model_path = ? WHERE id = ?",
            (model.name, model.type, model.credit_cost, model_path, model.id)
        )
        conn.commit()
        return model

    def delete(self, model_id: int) -> bool:
        conn = self.db.get_connection()
        cursor = conn.cursor()

        # Сначала получаем путь к файлу модели, чтобы удалить его
        cursor.execute("SELECT model_path FROM models WHERE id = ?", (model_id,))
        row = cursor.fetchone()
        if row and row["model_path"] and os.path.exists(row["model_path"]):
            # Если путь существует и файл по этому пути есть, удаляем файл
            os.remove(row["model_path"])

        # Удаляем запись о модели из базы данных
        cursor.execute("DELETE FROM models WHERE id = ?", (model_id,))
        conn.commit()
        # cursor.rowcount содержит количество удаленных строк. Если > 0, значит тру
        return cursor.rowcount > 0
