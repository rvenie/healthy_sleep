from core.entities.credit import Credit
from core.repositories.credit_repository import CreditRepository
from core.repositories.user_repository import UserRepository


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
        # Получаем текущий баланс пользователя
        current_balance = self.credit_repository.get_current_balance(user_id)

        # Проверяем, достаточно ли кредитов
        if current_balance < amount:
            raise ValueError("Недостаточно кредитов на счете")

        # Создаем запись о списании кредитов
        credit = Credit(
            user_id=user_id,
            amount=-amount,  # Отрицательное значение для списания
            operation_type=operation_type,
            balance_after=current_balance - amount
        )

        # Обновляем баланс пользователя
        user = self.user_repository.get_by_id(user_id)
        user.credits -= amount
        self.user_repository.update(user)

        # Сохраняем запись о списании
        return self.credit_repository.create(credit)

# Содержит классы для работы с балансом пользователя и списания кредитов.