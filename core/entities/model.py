class Model:
    def __init__(self, id=None, name=None, type=None, credit_cost=None, model_object=None):
        self.id = id
        self.name = name  # Название модели
        self.type = type  # Тип модели
        self.credit_cost = credit_cost  # Стоимость использования модели в кредитах
        self.model_object = model_object  # Объект модели (сериализованный)