import pandas as pd
import numpy as np
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import os


class DataPreprocessor:
    def __init__(self, data_path):
        self.data_path = data_path
        self.preprocessor = None
        self.X = None
        self.y = None
        self.feature_names = None

    def load_data(self):
        if not os.path.exists(self.data_path):
            raise FileNotFoundError(f"Файл данных не найден: {self.data_path}")

        df = pd.read_csv(self.data_path)

        # Целевая переменная - Sleep quality
        self.y = df["Sleep quality"].values

        # Удаляем целевую переменную из признаков
        df = df.drop(["Sleep quality"], axis=1)

        # Сохраняем имена признаков для дальнейшего использования
        self.feature_names = df.columns.tolist()

        # Разделяем числовые и категориальные признаки
        numeric_features = df.select_dtypes(include=["int64", "float64"]).columns.tolist()
        categorical_features = df.select_dtypes(include=["object"]).columns.tolist()

        # Создаем преобразователь для предобработки данных
        preprocessor = ColumnTransformer(
            transformers=[
                ("num", StandardScaler(), numeric_features),
                ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_features)
            ]
        )

        # Применяем преобразования к данным
        self.X = df.copy()
        self.preprocessor = preprocessor

        return self.X, self.y, self.preprocessor

    def get_column_names(self):
        return self.feature_names

    def transform_input_data(self, input_data):
        # Преобразуем входные данные в формат, понятный модели
        input_df = pd.DataFrame([input_data])

        # Убеждаемся, что у нас правильный порядок столбцов
        input_df = input_df[self.feature_names]

        # Применяем преобразования
        return self.preprocessor.transform(input_df)
