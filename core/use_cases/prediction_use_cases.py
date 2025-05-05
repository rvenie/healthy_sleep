from core.entities.prediction import Prediction
from core.repositories.prediction_repository import PredictionRepository
from core.repositories.model_repository import ModelRepository
from core.repositories.user_repository import UserRepository
from core.use_cases.credit_use_cases import DeductCreditsUseCase


class MakePredictionUseCase:
    def __init__(
            self,
            prediction_repository: PredictionRepository,
            model_repository: ModelRepository,
            deduct_credits_use_case: DeductCreditsUseCase
    ):
        self.prediction_repository = prediction_repository
        self.model_repository = model_repository
        self.deduct_credits_use_case = deduct_credits_use_case

    def execute(self, user_id: int, model_id: int, input_data: dict) -> Prediction:
        # Получаем модель
        model = self.model_repository.get_by_id(model_id)
        if not model:
            raise ValueError("Модель не найдена")

        # Списываем кредиты
        self.deduct_credits_use_case.execute(
            user_id=user_id,
            amount=model.credit_cost,
            operation_type="prediction"
        )

        # Выполняем предсказание
        prediction_result = model.model_object.predict([list(input_data.values())])[0]

        # Создаем запись о предсказании
        prediction = Prediction(
            user_id=user_id,
            model_id=model_id,
            input_data=input_data,
            prediction_result=prediction_result,
            credits_spent=model.credit_cost
        )

        # Сохраняем предсказание
        return self.prediction_repository.create(prediction)


class GetUserPredictionsUseCase:
    def __init__(self, prediction_repository: PredictionRepository):
        self.prediction_repository = prediction_repository

    def execute(self, user_id: int) -> list[Prediction]:
        return self.prediction_repository.get_by_user_id(user_id)
