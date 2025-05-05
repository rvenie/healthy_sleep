from datetime import datetime

class Credit:
    def __init__(self, id=None, user_id=None, amount=None, operation_type=None,
                 timestamp=None, balance_after=None):
        self.id = id
        self.user_id = user_id
        self.amount = amount  # Количество кредитов (положительное - пополнение, отрицательное - списание)
        self.operation_type = operation_type  # Тип операции (пополнение, списание за предсказание)
        self.timestamp = timestamp or datetime.now()  # Время операции
        self.balance_after = balance_after  # Баланс после операции

# Класс описывает операцию с кредитами пользователя, включая тип операции, сумму и остаток после операции.