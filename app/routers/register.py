from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.container import user_service
from app.database import get_session
from app.dto.user import UserDTO
from app.services.authentication import AuthenticationService

router = APIRouter()


@router.post("/", summary="Регистрация пользователя",
             description=" - Принимает username и password нового пользователя \n - Возвращает токен доступа на 30 минут")
async def register(data: UserDTO = None, session: Session = Depends(get_session)):

    # Создаем пользователя
    new_user = user_service.create_user(data, session)

    # Генерируем токен на основе username
    access_token = AuthenticationService.create_access_token(new_user.username)

    # Возвращаем токен
    return {"access_token": access_token, "token_type": "bearer"}
