
from datetime import timedelta, datetime
import jwt
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer

from app.config import config
from app.logger import logger


class AuthenticationService:
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

    @staticmethod
    def create_access_token(username: str) -> bytes:
        data = {"username": username}
        expire = datetime.utcnow() + timedelta(minutes=config.token.EXPIRATION_TIME_MINUTES)
        data_to_encode = {**data, **{"exp": expire}}

        # return access_token
        return jwt.encode(data_to_encode, config.token.SECRET, algorithm=config.token.ALGORITHM)


    @staticmethod
    def verify_token(token: str = Depends(oauth2_scheme)) -> str:
        try:
            data = jwt.decode(token, config.token.SECRET, algorithms=[config.token.ALGORITHM])
            username = data.get("username")
            if username is None:
                raise HTTPException(status_code=401, detail="Неверные данные для аутентификации")
            return username

        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Срок действия токена истек")
        except jwt.InvalidSignatureError:
            raise HTTPException(status_code=401, detail="Недействительная подпись токена")
        except Exception as e:
            logger.error(f'Ошибка токена: {e}')
            raise HTTPException(status_code=401, detail="Ошибка токена")


