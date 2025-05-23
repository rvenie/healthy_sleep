import pandas as pd
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
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

        # Целевая переменная
        self.y = df["Sleep quality"].values

        # Удаляем из признаков
        df = df.drop(["Sleep quality"], axis=1)

        # имена признаков
        self.feature_names = df.columns.tolist()

        # Разделяем числовые и категориальные признаки
        numeric_features = df.select_dtypes(include=["int64", "float64"]).columns.tolist()
        categorical_features = df.select_dtypes(include=["object"]).columns.tolist()

        # пайп для работы над категориями
        preprocessor = ColumnTransformer(
            transformers=[
                ("num", StandardScaler(), numeric_features),
                ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_features)
            ]
        )

        self.X = df.copy()
        self.preprocessor = preprocessor

        return self.X, self.y, self.preprocessor

    def get_column_names(self):
        return self.feature_names

    def transform_input_data(self, input_data):
        # в Пандас
        input_df = pd.DataFrame([input_data])

        # метчимся с фичами модели
        input_df = input_df[self.feature_names]

        # Обрабатываем
        return self.preprocessor.transform(input_df)
