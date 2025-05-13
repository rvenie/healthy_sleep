from typing import Dict
from core.entities.model import Model

models_dict: Dict[str, Model] = {}
feature_names: list = []


def init_models(model_repository, data_preprocessor):
    global models_dict, feature_names

    # Получаем все модели из репы
    models = model_repository.get_all()

    # Сохраняем модели в словаре для быстрого доступа
    for model in models:
        models_dict[model.name] = model

    # Получаем имена признаков для обработки входных данных
    feature_names = data_preprocessor.get_column_names()


def get_all_models() -> Dict[str, Model]:
    """
    Возвращаем словарь всех моделей.
    """
    return models_dict


def get_feature_names() -> list:
    """
    Возвращаем список имен признаков.
    """
    return feature_names
