import hashlib
from core.entities.user import User
from core.repositories.user_repository import UserRepository


class UserRegistrationUseCase:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def execute(self, username: str, password: str, email: str) -> User:
        # Существует ли пользователь с таким именем
        existing_user = self.user_repository.get_by_username(username)
        if existing_user:
            raise ValueError("Пользователь с таким именем уже существует")

        # Хешируем
        password_hash = hashlib.sha256(password.encode()).hexdigest()

        # Создаем пользователя
        new_user = User(
            username=username,
            password_hash=password_hash,
            email=email,
            credits=100 # Начальный депозит при регистрации
        )

        # Сохраняем
        return self.user_repository.create(new_user)


class UserAuthenticationUseCase:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def execute(self, username: str, password: str) -> User:
        # username
        user = self.user_repository.get_by_username(username)
        if not user:
            raise ValueError("Пользователь с таким именем не найден")

        # password
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        if user.password_hash != password_hash:
            raise ValueError("Неверный пароль")

        return user
