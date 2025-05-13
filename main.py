import os
import pandas as pd
from flask import Flask, redirect, url_for

# Импортируем классы для работы с репозиториями
from infrastructure.db.sqlite_db import SQLiteDB
from infrastructure.db.user_repository_impl import UserRepositoryImpl
from infrastructure.db.model_repository_impl import ModelRepositoryImpl
from infrastructure.db.prediction_repository_impl import PredictionRepositoryImpl
from infrastructure.db.credit_repository_impl import CreditRepositoryImpl

# Импортируем классы для работы с ML
from infrastructure.ml.data_preprocessing import DataPreprocessor
from infrastructure.ml.model_trainer import ModelTrainer
from infrastructure.ml.model_store import init_models

# Импортируем контроллеры
from infrastructure.web.controllers.user_controller import user_bp, __init__ as init_user_controller
from infrastructure.web.controllers.prediction_controller import prediction_bp, __init__ as init_prediction_controller
from infrastructure.web.controllers.credit_controller import credit_bp, __init__ as init_credit_controller

# Импортируем настройки
from config.settings import SECRET_KEY, DATA_PATH
from core.repositories.prediction_repository import PredictionRepository


def create_app():
    app = Flask(__name__)
    app.secret_key = SECRET_KEY

    # Инициализируем базу данных
    db = SQLiteDB()

    # Репозитории
    user_repository = UserRepositoryImpl(db)
    model_repository = ModelRepositoryImpl(db)
    prediction_repository = PredictionRepositoryImpl(db)
    credit_repository = CreditRepositoryImpl(db)

    # Проверяем наличие файла с данными
    if not os.path.exists(DATA_PATH):
        raise FileNotFoundError(f"Файл с данными не найден: {DATA_PATH}")

    # Предобработку данных
    data_preprocessor = DataPreprocessor(DATA_PATH)

    # Есть ли обученные модели в репозитории
    models = model_repository.get_all()
    print('Модели есть, не обучаю')
    if not models:
        print('Моделей нет, начинаю обучение')
        # Если моделей нет, обучаем их
        model_trainer = ModelTrainer(DATA_PATH, model_repository)
        models = model_trainer.train_all_models()

    # хранилище моделей
    init_models(model_repository, data_preprocessor)

    # контроллеры
    init_user_controller(user_repository, prediction_repository)
    init_prediction_controller(user_repository, model_repository, prediction_repository, credit_repository)
    init_credit_controller(credit_repository, user_repository)

    # Регистрируем blueprints
    app.register_blueprint(user_bp)
    app.register_blueprint(prediction_bp)
    app.register_blueprint(credit_bp)

    @app.route("/")
    def index():
        return redirect(url_for("user.login"))

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, port=3000)
