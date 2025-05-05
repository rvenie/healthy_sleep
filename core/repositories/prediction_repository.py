from abc import ABC, abstractmethod
from core.entities.prediction import Prediction


class PredictionRepository(ABC):
    @abstractmethod
    def create(self, prediction: Prediction) -> Prediction:
        pass

    @abstractmethod
    def get_by_id(self, prediction_id: int) -> Prediction:
        pass

    @abstractmethod
    def get_by_user_id(self, user_id: int) -> list[Prediction]:
        pass

    @abstractmethod
    def update(self, prediction: Prediction) -> Prediction:
        pass

    @abstractmethod
    def delete(self, prediction_id: int) -> bool:
        pass
