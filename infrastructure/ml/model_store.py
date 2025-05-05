# Хранилище моделей для предотвращения циклических импортов

from typing import Dict
from core.entities.model import Model

models_dict: Dict[str, Model] = {}
feature_names: list = []


def init_models(model_repository, data_preprocessor):
    """
    Инициализирует модели и сохраняет их в глобальный словарь.
    Вызывается один раз при запуске приложения.
    """
    global models_dict, feature_names

    # Получаем все модели из репозитория
    models = model_repository.get_all()

    # Сохраняем модели в словаре для быстрого доступа
    for model in models:
        models_dict[model.name] = model

    # Получаем имена признаков для обработки входных данных
    feature_names = data_preprocessor.get_column_names()


def get_model(name: str) -> Model:
    """
    Получает модель по имени.
    """
    return models_dict.get(name)


def get_all_models() -> Dict[str, Model]:
    """
    Возвращает словарь всех моделей.
    """
    return models_dict


def get_feature_names() -> list:
    """
    Возвращает список имен признаков.
    """
    return feature_names
