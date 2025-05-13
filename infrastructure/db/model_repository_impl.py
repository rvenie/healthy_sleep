import os
from joblib import dump, load
from core.entities.model import Model
from core.repositories.model_repository import ModelRepository
from infrastructure.db.sqlite_db import SQLiteDB

class ModelRepositoryImpl(ModelRepository):
    def __init__(self, db: SQLiteDB, models_directory: str = "models"):

        self.db = db
        self.models_directory = models_directory
        # Создаем директорию для моделей, если она еще не существует.
        os.makedirs(self.models_directory, exist_ok=True)

    def _path_for(self, model: Model) -> str:
        # Имя файла модели. Можно добавить ID, timestamp или версию для уникальности,
        filename = f"{model.name}.pkl" 
        return os.path.join(self.models_directory, filename)

    def create(self, model: Model) -> Model:
        conn = self.db.get_connection()
        cursor = conn.cursor()

        # Сохраняем объект модели (например, Pipeline scikit-learn) на диск
        model_path = self._path_for(model)
        # Сериализуем и сохраняем объект модели
        dump(model.model_object, model_path)

        # Выполняем SQL-запрос на вставку метаданных модели в таблицу 'models'
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
        # Выполняем SQL-запрос на выборку записи из таблицы 'models' по ID
        cursor.execute("SELECT * FROM models WHERE id = ?", (model_id,))
        row = cursor.fetchone()

        if not row:
            return None

        model_path = row["model_path"]
        # Загружаем объект модели с диска
        model_object = load(model_path)

        # Проверка, что загруженный объект имеет метод predict
        if not hasattr(model_object, "predict"):
            raise ValueError(f"Файл {model_path} не содержит объект модели с методом predict")

        # Создаем и возвращаем объект Model на основе данных из базы и загруженного объекта модели
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
        # Выполняем SQL-запрос на выборку записи из таблицы 'models' по имени
        cursor.execute("SELECT * FROM models WHERE name = ?", (name,))
        row = cursor.fetchone()

        if not row:
            return None

        # Загружаем объект модели с диска по пути, указанному в БД
        model_object = load(row["model_path"])
        # Создаем и возвращаем объект Model
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
        # Выбираем только метаданные, без model_path, так как сами модели не загружаем
        cursor.execute("SELECT id, name, type, credit_cost FROM models")
        rows = cursor.fetchall()  # Извлекаем все строки результата
        # Создаем список объектов Model. model_object не устанавливается (остается None по умолчанию).
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
