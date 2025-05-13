from abc import ABC, abstractmethod
from core.entities.model import Model


class ModelRepository(ABC):
    @abstractmethod
    def create(self, model: Model) -> Model:
        pass

    @abstractmethod
    def get_by_id(self, model_id: int) -> Model:
        pass

    @abstractmethod
    def get_by_name(self, name: str) -> Model:
        pass

    @abstractmethod
    def get_all(self) -> list[Model]:
        pass

    @abstractmethod
    def update(self, model: Model) -> Model:
        pass

    @abstractmethod
    def delete(self, model_id: int) -> bool:
        pass
