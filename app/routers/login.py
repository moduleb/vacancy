from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.container import user_service
from app.database import get_session
from app.services.authentication import AuthenticationService

router = APIRouter()


@router.post("/", summary="Вход в систему",
             description=" - Принимает username и password существующего пользователя, \n - Возвращает токен доступа на 30 минут")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):
    # Получаем объект пользователя из базы данных
    user = user_service.get_user(form_data.username, session)

    # Хешируем полученный из запроса пароль
    password2 = user_service.hash_password(form_data.password)

    # Сравниваем пароль из базы данных с хешированным паролем из запроса
    # Если все ОК, генерируем и возвращаем токен
    if user.password == password2:
        access_token = AuthenticationService.create_access_token(user.username)
        return {"access_token": access_token, "token_type": "bearer"}
    else:
        raise HTTPException(401, detail="Неверный логин или пароль")
