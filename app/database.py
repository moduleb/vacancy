from psycopg2 import OperationalError
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.config import config
from app.logger import logger

# Формируем URI для подключения к базе данных
sqlalchemy_database_uri: str = f'postgresql://' \
                               f'{config.database.user}:' \
                               f'{config.database.password}@' \
                               f'{config.database.host}:' \
                               f'{config.database.port}/' \
                               f'{config.database.name}'

# Создаем объект engine для подключения к базе данных
engine = create_engine(sqlalchemy_database_uri, pool_pre_ping=True)

# Создаем класс SessionClass для создания сессий
SessionClass = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Создаем базовый класс для ORM-моделей
Base = declarative_base()


def get_session():
    session = SessionClass()
    try:
        yield session
    except OperationalError as e:
        pass
        logger.error(f"Ошибка подключения к базе данных: {e}")
    finally:
        session.close()