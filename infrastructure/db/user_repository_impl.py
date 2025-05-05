from core.repositories.user_repository import UserRepository
from core.entities.user import User
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class UserModel(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    credits = db.Column(db.Integer, default=0)

class UserRepositoryImpl(UserRepository):
    def add(self, user: User) -> User:
        db_user = UserModel(username=user.username, password_hash=user.password_hash, credits=user.credits)
        db.session.add(db_user)
        db.session.commit()
        user.id = db_user.id
        return user

    def find_by_username(self, username: str) -> User:
        db_user = UserModel.query.filter_by(username=username).first()
        if not db_user:
            return None
        return User(id=db_user.id, username=db_user.username, password_hash=db_user.password_hash, credits=db_user.credits)

    def update(self, user: User) -> None:
        db_user = UserModel.query.get(user.id)
        db_user.credits = user.credits
        db.session.commit()
