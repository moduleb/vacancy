import uvicorn
from fastapi import FastAPI

from app.routers import info, login, register

# Создаем приложение
app = FastAPI()

# Регистрируем эндпоинты
app.include_router(register.router, prefix='/register', tags=["/register"])
app.include_router(login.router, prefix='/login', tags=["/login"])
app.include_router(info.router, prefix='/info', tags=["/info"])

# Запускаем приложение
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0")
