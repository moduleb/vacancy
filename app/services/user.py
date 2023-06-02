import base64
import hashlib
import secrets
from _decimal import Decimal
from datetime import datetime, timedelta

from faker import Faker
from fastapi import HTTPException
from sqlalchemy.orm import Session


from app.config import config
from app.dao.user import UserDAO
from app.dto.user import UserDTO
from app.logger import logger
from app.models.user import User


class UserService:
    def __init__(self, dao: UserDAO):
        self.dao = dao
        # Для генерации случайных данных
        self.faker = Faker()

    def create_user(self, data: UserDTO, session: Session) -> User:
        """
        Создает нового пользователя и сохраняет его в базу данных.
        """

        # Создаем новый объект User
        new_user = User(**data.dict())

        # Заменяем пароль на хеш
        new_user.password = self.hash_password(data.password)

        # Генерируем случайную дату между сегодня и +700 дней.
        new_user.promotion_date = self.__random_date()

        # Генерируем случайную зарплату
        new_user.salary = Decimal(self.faker.random_int(min=10000, max=300000))

        # Сохраняем пользователя и возвращаем объект User
        return self.dao.create_user(new_user, session)

    def get_user(self, username, session):
        """
        Получаем объект User по username
        """
        user = self.dao.get_user(username, session)
        if not user:
            raise HTTPException(404, detail="Пользователь не найден")
        return user

    @staticmethod
    def hash_password(password: str) -> str:
        """
        Хеширует пароль с помощью PBKDF2 и возвращает его в виде строки base64.
        """
        try:
            hash_digest = hashlib.pbkdf2_hmac(
                config.password.ALGORITHM,
                password.encode('utf-8'),
                config.password.SALT,
                config.password.ITERATIONS
            )
            return base64.b64encode(hash_digest).decode('utf-8')
        except Exception as e:
            logger.error(f'Ошибка функции хеширования пароля: {e}')
            raise HTTPException(500, detail="Ошибка функции хеширования пароля")

    @staticmethod
    def __random_date() -> str:
        """
        Генерирует случайную дату между Сегодня и 700 дней вперед.
        """
        random_days = secrets.randbelow(700)
        random_date = datetime.now() + timedelta(days=random_days)
        return datetime.strftime(random_date, '%Y-%m-%d')
