![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![FastAPI](https://img.shields.io/badge/FastAPI-%0c584b?style=for-the-badge&logo=fastapi&logoColor=white)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)
![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-black?style=for-the-badge&logo=sqlalchemy&logoColor=red)

# Приложение Vacancy

Приложение Vacancy выдает токен доступа при регистрации или авторизации, возвращает данные о зарплате и дате повышения при предъявлении токена.

Генерирует случайные данные о зарплате и повышении в момент регистрации, сохраняет в базу данных Postgres, развернутую в Docker контейнере.
Данные базы данных хранятся в папке `pg_data` и сохраняются при удалении контейнера. Доступ к базе открыт для других приложений.




## Запуск приложения

### На локальной машине:

1. Клонировать проект с Github
2. Перейти в папку проекта
3. Запустить приложение Docker
4. Создать образ:
<br>`docker compose build`
5. Запустить контейнер:
<br>`docker compose up -d`
6. Остановить контейнер:
<br>`docker compose stop`

### На удаленном сервере:
1. Создаем папку для приложения:
<br>`mkdir vacancy`
2. Переходим в эту папку:
<br>`cd vacancy`
3. Скачиваем файл <b> 'docker-compose.yml'</b>: 
<br>`wget -O docker-compose.yaml https://raw.githubusercontent.com/ModuleB/vacancy/master/docker-compose.yaml`
4. Скачиваем файл <b> 'Dockerfile'</b>: 
<br>`wget -O Dockerfile https://raw.githubusercontent.com/ModuleB/vacancy/master/Dockerfile`
5. Скачиваем docker образы:
<br>`docker compose pull`
6. Запустить контейнер:
<br>`docker compose up -d`
7. Останить контейнер:
<br>`docker compose stop`



## Эндпоинты:

Приложение доступно по адресу:
- на локальной машине http://127.0.0.1/:8000
- на удаленном сервере http://<IP адрес сервера>:8000

<br> Информация об эндпоинтах также доступна в Swagger по адресу <b>/docs</b>

### /register

Принимает JSON с данными нового пользователя <b>[ POST ]</b>:
```
{
  "username": "string",
  "password": “String1”
}
```

Возвращает токен доступа на 30 минут или ошибку если пользователь уже существует или данные не прошли валидацию:
```
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InN0cmlmbmciLCJleHAiOjE2ODU2OTAxNzd9.bn_523efN3TdqgU1gAZzVn-RHkEMxGL3NpcHH0YTHM4",
  "token_type": "bearer"
}
```

### /login

Принимает JSON с данными уже зарегистрированного пользователя <b>[ POST ]</b>:
```
{
  "username": "string",
  "password": “String1”
}
```

Возвращает токен доступа на 30 минут или ошибку если пользователя не существует.

### /info

Не принимает параметров, ожидает токен доступа в заголовке ‘Authorization’ <b>[ GET ]</b>:
```
Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InN0cmlmbmciLCJleHAiOjE2ODU2OTAxNzd9.bn_523efN3TdqgU1gAZzVn-RHkEMxGL3NpcHH0YTHM4
```

Возвращает JSON с данными пользователя:
```
{
    "username": “string”,
    "salary": 39258,
    "promotion_date": "2025-02-28"
}
```



## База данных доступна вне приложения. Параметры подключения:
- user: <b>vacancy</b>
- password: <b>vacancy</b>
- port: <b>5435</b>
- host:
  * на локальной машине: <b>127.0.0.1</b>
  * на удаленном сервере: <b>< IP адрес сервера ></b>
