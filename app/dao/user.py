import logging

from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError

from app.logger import logger
from app.models.user import User


class UserDAO:
    def create_user(self, new_user, session):
        """
        Добавляет нового пользователя в базу данных.

        :param new_user: Объект с данными нового пользователя
        :param session: Объект сессии SQLAlchemy для выполнения операций в базе данных
        :return: Созданный пользователь
        """
        try:
            # Добавление нового пользователя и сохранение изменений в базе данных
            session.add(new_user)
            session.commit()
        except IntegrityError as e:
            # Если произошла ошибка целостности (дублирование)
            if 'already exists' in str(e):
                raise HTTPException(500, detail="Пользователь уже существует")
        except Exception as e:
            # Если произошла какая-либо другая ошибка
            logger.error(f"Ошибка подключения к базе данных: {e}")
            raise HTTPException(500, detail="Ошибка базы данных")
        else:
            # Если ошибок не возникло, возвращаем созданного пользователя
            return new_user


    def get_user(self, username, session):
        """
        Извлекает пользователя с заданным именем пользователя из базы данных.

        :param username: Имя пользователя для поиска в базе данных
        :param session: Объект сессии SQLAlchemy для выполнения операций в базе данных
        :return: Найденный пользователь или None, если пользователь не найден
        """
        try:
            # Выполнение запроса к базе данных для поиска пользователя с заданным именем пользователя
            return session.query(User).filter(User.username == username).first()
        except Exception as e:
            logger.error(f"Ошибка подключения к базе данных: {e}")
            raise HTTPException(500, detail="Ошибка базы данных")
