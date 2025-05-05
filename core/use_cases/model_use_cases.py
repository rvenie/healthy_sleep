from core.entities.model import Model
from core.repositories.model_repository import ModelRepository


class GetAllModelsUseCase:
    def __init__(self, model_repository: ModelRepository):
        self.model_repository = model_repository

    def execute(self) -> list[Model]:
        return self.model_repository.get_all()


class GetModelByIdUseCase:
    def __init__(self, model_repository: ModelRepository):
        self.model_repository = model_repository

    def execute(self, model_id: int) -> Model:
        return self.model_repository.get_by_id(model_id)


# Содержит классы для получения всех моделей и конкретной модели по ID.