# MicroBlog Service

Итоговый проект курса Python Advanced.

MicroBlog — сервис микроблогов, в котором пользователи могут создавать и удалять твиты, прикреплять изображения, ставить лайки и подписываться на других пользователей.

## Возможности проекта

- создание твитов;
- удаление своих твитов;
- загрузка изображений;
- добавление изображений к твитам;
- лайки и удаление лайков;
- подписка и отписка от пользователей;
- просмотр профиля пользователя;
- просмотр ленты твитов;
- сортировка ленты по популярности;
- авторизация через заголовок `api-key`;
- Swagger-документация API;
- запуск приложения через Docker Compose.

## Используемые технологии

- Python
- Flask
- SQLAlchemy
- PostgreSQL
- Flask-Migrate
- Alembic
- Flasgger / Swagger
- Pytest
- Flake8
- Docker
- Docker Compose

## Запуск через Docker

Для запуска проекта должны быть установлены Docker и Docker Compose.

Собрать и запустить приложение:

```bash
docker compose up -d --build
```

Проверить состояние контейнеров:

```bash
docker compose ps
```

После запуска приложение доступно по адресу:

```text
http://127.0.0.1:5000/
```

Остановить приложение:

```bash
docker compose down
```

## База данных

В проекте используется PostgreSQL.

При запуске через Docker база данных запускается в отдельном контейнере.

Миграции применяются автоматически перед запуском Flask-приложения:

```bash
flask db upgrade
```

## Авторизация

Для определения пользователя используется HTTP-заголовок:

```text
api-key
```

Пример:

```text
api-key: test
```

Пользователь с таким ключом должен существовать в базе данных.

## Основные API-маршруты

Получение текущего пользователя:

```text
GET /api/users/me
```

Получение пользователя по ID:

```text
GET /api/users/<user_id>
```

Получение ленты твитов:

```text
GET /api/tweets
```

Создание твита:

```text
POST /api/tweets
```

Удаление твита:

```text
DELETE /api/tweets/<tweet_id>
```

Загрузка изображения:

```text
POST /api/medias
```

Поставить или удалить лайк:

```text
POST /api/tweets/<tweet_id>/likes
DELETE /api/tweets/<tweet_id>/likes
```

Подписаться или отписаться от пользователя:

```text
POST /api/users/<user_id>/follow
DELETE /api/users/<user_id>/follow
```

## Swagger

После запуска приложения интерактивная документация API доступна по адресу:

```text
http://127.0.0.1:5000/apidocs/
```

Через Swagger можно посмотреть доступные API-маршруты и их параметры.

## Тестирование

Запустить все тесты:

```bash
pytest -v
```

На момент завершения проекта:

```text
12 passed
```

## Проверка кода

Для проверки проекта с помощью Flake8:

```bash
flake8 app tests run.py config.py
```

При успешной проверке команда завершается без ошибок.

## Структура проекта

```text
microblog_service/
├── app/
│   ├── __init__.py
│   ├── models.py
│   ├── routes.py
│   └── utils.py
├── dist/
├── migrations/
├── tests/
├── uploads/
├── config.py
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── run.py
├── swagger.yml
└── README.md
```

## Автор

Filip Tataroi