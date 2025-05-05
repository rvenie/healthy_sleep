from abc import ABC, abstractmethod
from core.entities.credit import Credit


class CreditRepository(ABC):
    @abstractmethod
    def create(self, credit: Credit) -> Credit:
        pass

    @abstractmethod
    def get_by_id(self, credit_id: int) -> Credit:
        pass

    @abstractmethod
    def get_by_user_id(self, user_id: int) -> list[Credit]:
        pass

    @abstractmethod
    def get_current_balance(self, user_id: int) -> int:
        pass

    @abstractmethod
    def update(self, credit: Credit) -> Credit:
        pass
