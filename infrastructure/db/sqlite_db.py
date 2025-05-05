import sqlite3
import os


class SQLiteDB:
    def __init__(self, db_path="sleep_prediction.db"):
        self.db_path = db_path
        self.connection = None
        self.init_db()

    def get_connection(self):
        if self.connection is None:
            self.connection = sqlite3.connect(self.db_path, check_same_thread=False)
            self.connection.row_factory = sqlite3.Row
        return self.connection

    def init_db(self):
        conn = self.get_connection()
        cursor = conn.cursor()

        # Создаем таблицу пользователей
        cursor.execute('''
                       CREATE TABLE IF NOT EXISTS users
                       (
                           id
                           INTEGER
                           PRIMARY
                           KEY
                           AUTOINCREMENT,
                           username
                           TEXT
                           UNIQUE
                           NOT
                           NULL,
                           password_hash
                           TEXT
                           NOT
                           NULL,
                           email
                           TEXT
                           UNIQUE
                           NOT
                           NULL,
                           credits
                           INTEGER
                           NOT
                           NULL
                           DEFAULT
                           100
                       )
                       ''')

        # Создаем таблицу моделей
        cursor.execute('''
                       CREATE TABLE IF NOT EXISTS models
                       (
                           id
                           INTEGER
                           PRIMARY
                           KEY
                           AUTOINCREMENT,
                           name
                           TEXT
                           UNIQUE
                           NOT
                           NULL,
                           type
                           TEXT
                           NOT
                           NULL,
                           credit_cost
                           INTEGER
                           NOT
                           NULL,
                           model_path
                           TEXT
                           NOT
                           NULL
                       )
                       ''')

        # Создаем таблицу предсказаний
        cursor.execute('''
                       CREATE TABLE IF NOT EXISTS predictions
                       (
                           id
                           INTEGER
                           PRIMARY
                           KEY
                           AUTOINCREMENT,
                           user_id
                           INTEGER
                           NOT
                           NULL,
                           model_id
                           INTEGER
                           NOT
                           NULL,
                           input_data
                           TEXT
                           NOT
                           NULL,
                           prediction_result
                           TEXT
                           NOT
                           NULL,
                           timestamp
                           TIMESTAMP
                           NOT
                           NULL,
                           credits_spent
                           INTEGER
                           NOT
                           NULL,
                           FOREIGN
                           KEY
                       (
                           user_id
                       ) REFERENCES users
                       (
                           id
                       ),
                           FOREIGN KEY
                       (
                           model_id
                       ) REFERENCES models
                       (
                           id
                       )
                           )
                       ''')

        # Создаем таблицу кредитов
        cursor.execute('''
                       CREATE TABLE IF NOT EXISTS credits
                       (
                           id
                           INTEGER
                           PRIMARY
                           KEY
                           AUTOINCREMENT,
                           user_id
                           INTEGER
                           NOT
                           NULL,
                           amount
                           INTEGER
                           NOT
                           NULL,
                           operation_type
                           TEXT
                           NOT
                           NULL,
                           timestamp
                           TIMESTAMP
                           NOT
                           NULL,
                           balance_after
                           INTEGER
                           NOT
                           NULL,
                           FOREIGN
                           KEY
                       (
                           user_id
                       ) REFERENCES users
                       (
                           id
                       )
                           )
                       ''')

        # Вставляем информацию о моделях, если таблица пуста
        cursor.execute("SELECT COUNT(*) FROM models")
        if cursor.fetchone()[0] == 0:
            cursor.execute('''
                           INSERT INTO models (name, type, credit_cost, model_path)
                           VALUES ("Логистическая регрессия", "LogisticRegression", 5,
                                   "models/logistic_regression.pkl"),
                                  ("Random Forest", "RandomForest", 10, "models/random_forest.pkl"),
                                  ("CatBoost", "CatBoost", 15, "models/catboost.pkl")
                           ''')

        conn.commit()
