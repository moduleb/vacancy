from app.dao.user import UserDAO
from app.services.user import UserService

user_dao = UserDAO()
user_service = UserService(user_dao)
