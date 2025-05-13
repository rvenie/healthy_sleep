from core.entities.credit import Credit
from core.repositories.credit_repository import CreditRepository
from core.repositories.user_repository import UserRepository
from datetime import datetime

class GetUserBalanceUseCase:
    def __init__(self, credit_repository: CreditRepository):
        self.credit_repository = credit_repository

    def execute(self, user_id: int) -> int:
        return self.credit_repository.get_current_balance(user_id)


class DeductCreditsUseCase:
    def __init__(self, credit_repository: CreditRepository, user_repository: UserRepository):
        self.credit_repository = credit_repository
        self.user_repository = user_repository

    def execute(self, user_id: int, amount: int, operation_type: str) -> Credit:
        # текущий баланс пользователя
        current_balance = self.credit_repository.get_current_balance(user_id)

        if current_balance < amount:
            raise ValueError("Недостаточно кредитов на счете")

        # Создаем запись о списании кредитов
        credit = Credit(
            user_id=user_id,
            amount=-amount,  # Отрицательное значение для списания
            operation_type=operation_type,
            balance_after=current_balance - amount
        )

        # Обновляем баланс
        user = self.user_repository.get_by_id(user_id)
        user.credits -= amount
        self.user_repository.update(user)

        # Сохраняем 
        return self.credit_repository.create(credit)
    
class AddCreditsUseCase:
    def __init__(self, credit_repository, user_repository):
        self.credit_repository = credit_repository
        self.user_repository = user_repository
    
    def execute(self, user_id: int, amount: int, operation_type: str = "manual_add") -> int:
        # текущий баланс
        current_balance = self.credit_repository.get_current_balance(user_id)
        
        # новый баланс
        new_balance = current_balance + amount
        
        # Запись о пополнении кредитов
        credit = Credit(
            user_id=user_id,
            amount=amount,
            operation_type=operation_type,
            timestamp=datetime.now(),
            balance_after=new_balance
        )
        
        # Сохраняем транзакцию
        self.credit_repository.create(credit)
        
        # Обновляем баланс у юзера
        user = self.user_repository.get_by_id(user_id)
        user.credits = new_balance
        self.user_repository.update(user)
        
        return new_balance

