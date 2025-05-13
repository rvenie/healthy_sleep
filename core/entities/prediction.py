from datetime import datetime

class Prediction:
    def __init__(self, id=None, user_id=None, model_id=None, input_data=None,
                 prediction_result=None, timestamp=None, credits_spent=None):
        self.id = id
        self.user_id = user_id
        self.model_id = model_id
        self.input_data = input_data  # Входные данные для предсказания
        self.prediction_result = prediction_result  # Результат предсказания
        self.timestamp = timestamp or datetime.now()  # Время предсказания
        self.credits_spent = credits_spent  # Количество потраченных кредитов