from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.container import user_service
from app.database import get_session
from app.dto.user import ShowUser
from app.services.authentication import AuthenticationService

router = APIRouter()


@router.get("/", response_model=ShowUser,
            summary="Получение информации о зарплате и дате повышения",
            description=" - Возвращает JSON с информацией о зарплате и дате повышения\n"
                        " - Требует наличия токена в заголовке запроса в поле 'Authorization'")
async def info(current_username: str = Depends(AuthenticationService.verify_token),
               session: Session = Depends(get_session)):
    # Возвращаем информацию о пользователе
    return user_service.get_user(current_username, session)
