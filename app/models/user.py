from typing import Optional
from datetime import date
from sqlalchemy import Column, Integer, String, Date, DECIMAL
from sqlalchemy.ext.declarative import declarative_base

from app.database import engine

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    username: str = Column(String, unique=True, nullable=False, index=True)
    password: str = Column(String, nullable=False)
    promotion_date: Optional[date] = Column(Date)
    salary: Optional[DECIMAL] = Column(DECIMAL(precision=8, scale=2))
    # DECIMAL(precision=8, scale=2) --> всего 8 цифр, два знака после запятой (напр. 300.000.00)

Base.metadata.create_all(engine)