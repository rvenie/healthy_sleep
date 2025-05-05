import joblib
from typing import List
import numpy as np

from core.entities.model import Model
from core.repositories.model_repository import ModelRepository
from core.repositories.log_repository import LogRepository
from core.repositories.user_repository import UserRepository
from core.entities.prediction_log import PredictionLog
from datetime import datetime

class ModelUseCases:
    def __init__(self,
                 model_repo: ModelRepository,
                 user_repo: UserRepository,
                 log_repo: LogRepository,
                 model_dir: str):
        self.model_repo = model_repo
        self.user_repo = user_repo
        self.log_repo = log_repo
        self.model_dir = model_dir

    def upload_model(self, owner_id: int, name: str, file_bytes: bytes) -> Model:
        # сохраняем на диск
        import os
        path = os.path.join(self.model_dir, f"{owner_id}_{name}.pkl")
        with open(path, "wb") as f:
            f.write(file_bytes)
        m = Model(id=None, name=name, path=path, owner_id=owner_id)
        return self.model_repo.add(m)

    def predict(self,
                user_id: int,
                model_id: int,
                data: List[List[float]],
                cost_per_prediction: int = 1) -> List[float]:
        # получаем пользователя
        user = self.user_repo.get_by_id(user_id)
        if not user:
            raise ValueError("Пользователь не найден")
        # проверяем баланс
        if user.credits < cost_per_prediction * len(data):
            raise ValueError("Недостаточно кредитов для этой операции")
        # загружаем модель
        model_meta = self.model_repo.get_by_id(model_id)
        if not model_meta:
            raise ValueError("Модель не найдена")
        model = joblib.load(model_meta.path)
        # делаем предсказание
        arr = np.array(data)
        preds = model.predict(arr).tolist()
        # списываем кредиты и логируем каждый прогноз
        from core.use_cases.user_use_cases import UserUseCases
        uu = UserUseCases(self.user_repo)
        for _ in preds:
            uu.deduct_credits(user, cost_per_prediction)
            log = PredictionLog(id=None,
                                user_id=user.id,
                                model_id=model_meta.id,
                                timestamp=datetime.utcnow(),
                                credits_used=cost_per_prediction)
            self.log_repo.add(log)
        return preds
