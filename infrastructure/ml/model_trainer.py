import os
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from catboost import CatBoostClassifier
from sklearn.pipeline import Pipeline
from infrastructure.ml.data_preprocessing import DataPreprocessor
from core.entities.model import Model
from core.repositories.model_repository import ModelRepository


class ModelTrainer:
    def __init__(self, data_path, model_repository):
        self.data_path = data_path
        self.model_repository = model_repository
        self.preprocessor = DataPreprocessor(data_path)
        self.X = None
        self.y = None
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None

    def prepare_data(self):
        # Загружаем и подготавливаем данные
        self.X, self.y, preprocessor = self.preprocessor.load_data()

        # Разделяем данные на обучающую и тестовую выборки
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            self.X, self.y, test_size=0.2, random_state=42
        )

        return preprocessor

    def train_logistic_regression(self):
        print('Начинаю обучение Логрег')
        preprocessor = self.prepare_data()

        # Создаем и обучаем модель логистической регрессии
        model = Pipeline([
            ("preprocessor", preprocessor),
            ("classifier", LogisticRegression(max_iter=1000, random_state=42))
        ])

        model.fit(self.X_train, self.y_train)

        # Создаем объект модели для сохранения в базе данных
        lr_model = Model(
            name="Логистическая регрессия",
            type="LogisticRegression",
            credit_cost=10,
            model_object=model
        )

        # Сохраняем модель в репозитории
        return self.model_repository.create(lr_model)

    def train_random_forest(self):
        print('Начинаю обучение Случ Леса')
        preprocessor = self.prepare_data()

        # Создаем и обучаем модель Random Forest
        model = Pipeline([
            ("preprocessor", preprocessor),
            ("classifier", RandomForestClassifier(n_estimators=100, random_state=42))
        ])

        model.fit(self.X_train, self.y_train)

        # Создаем объект модели для сохранения в базе данных
        rf_model = Model(
            name="Random Forest",
            type="RandomForest",
            credit_cost=20,
            model_object=model
        )

        # Сохраняем модель в репозитории
        return self.model_repository.create(rf_model)

    def train_catboost(self):
        print('Начинаю обучение Кэтбуста')
        preprocessor = self.prepare_data()

        # Создаем и обучаем модель CatBoost
        model = Pipeline([
            ("preprocessor", preprocessor),
            ("classifier", CatBoostClassifier(iterations=100, learning_rate=0.1, random_state=42, verbose=False))
        ])

        model.fit(self.X_train, self.y_train)

        # Создаем объект модели для сохранения в базе данных
        cb_model = Model(
            name="CatBoost",
            type="CatBoost",
            credit_cost=30,
            model_object=model
        )

        # Сохраняем модель в репозитории
        return self.model_repository.create(cb_model)

    def train_all_models(self):
        # Обучаем все модели и возвращаем их
        models = []
        models.append(self.train_logistic_regression())
        models.append(self.train_random_forest())
        models.append(self.train_catboost())
        return models
