import os

# импортирую load_dotenv, чтобы брать данные из файла .env
from dotenv import load_dotenv


# загружаю переменные из файла .env
load_dotenv()


class Config:
    # получаю адрес базы данных из .env
    # если DATABASE_URL нет, использую адрес PostgreSQL по умолчанию
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "postgresql://postgres:postgres@localhost:5432/microblog"
    )

    # отключаю лишнее отслеживание изменений SQLAlchemy
    SQLALCHEMY_TRACK_MODIFICATIONS = False
