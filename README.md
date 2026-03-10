# Проект табло теннисного матча TennisScoreboard

Веб-приложение, реализующее табло счёта теннисного матча.

[Техническое задание проекта](https://zhukovsd.github.io/python-backend-learning-course/Projects/TennisScoreboard/)

## Функционал приложения

Работа с матчами:

- Создание нового матча
- Просмотр законченных матчей, поиск матчей по именам игроков
- Подсчёт очков в текущем матче

## Подсчёт очков в теннисном матче

Каждый матч играется по следующим правилам:
- Матч играется до двух сетов (best of 3)
- При счёте 6/6 в сете, играется тай-брейк до 7 очков

## Варианты запуска приложения:


#### 1. Через Docker

(Предполагается что Docker desctop установлен и запущен)

Создайте конфигурационный файл ".env", следуя образцу ".env.example"
Пример .env:
```
DB_HOST="postgres"
DB_PORT=5432
DB_USER="root"
DB_PASS="password"
DB_NAME="main"

SERVER_HOST='0.0.0.0'
SERVER_PORT=8000"
```
Измените настройки nginx, файл nginx.conf в главной папке
```
server_name  ваш_ip;
```
Запустите докер с помощью консоли:
```
docker-compose up --build
```
Инициализируйте бд с помощью alembic:
```
DB_HOST="127.0.0.1"
```
```
alembic upgrade head
```
Теперь сайт будет доступен по адресу http://ваш_ip/


#### 2. Через терминал

Создайте конфигурационный файл ".env", следуя образцу ".env.example"
Пример .env:
```
DB_HOST="127.0.0.1"
DB_PORT=5432
DB_USER="root"
DB_PASS="password"
DB_NAME="main"

SERVER_HOST='0.0.0.0'
SERVER_PORT=8000"
```

Запустите бд postgresql локально или с помощью docker

Инициализируйте бд с помощью alembic:
```
DB_HOST="127.0.0.1"
```
```
alembic upgrade head
```
Установите необходимые библиотеки и запустите виртуальное окружение
```
python3 -m pip install --upgrade pip && pip install uv
uv venv /app/.venv
uv sync
```
Активируйте venv
```
.\.venv\scripts\activate
```
Запустите Проект:
```
python main.py
```
Теперь сайт будет доступен по адресу http://ваш_ip/.



#### 3. Запуск тестов

```
python tests/test_render_score.py
```
Для второго теста необходимо, чтобы бд была запущена и настроена
```
python tests/test_server.py
```


Также доступен сайт, на котором уже запущено приложение: http://185.21.156.184:8000/