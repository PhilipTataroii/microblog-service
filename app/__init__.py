# импортирую os для работы с путями к папкам
import os

# импортирую yaml, чтобы прочитать swagger.yml
import yaml

# импортирую Flask для создания приложения
from flask import Flask

# импортирую Swagger для документации моего API
from flasgger import Swagger

# импортирую SQLAlchemy для работы с базой данных
from flask_sqlalchemy import SQLAlchemy

# импортирую Flask-Migrate для миграций базы данных
from flask_migrate import Migrate

# импортирую основные настройки приложения
from config import Config


# создаю объект для работы с базой данных
db = SQLAlchemy()

# создаю объект для работы с миграциями
migrate = Migrate()


def create_app(test_config=None):
    # получаю абсолютный путь к корню моего проекта
    project_root = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..")
    )

    # создаю Flask-приложение
    # готовый frontend находится в папке dist
    app = Flask(
        __name__,
        static_folder=os.path.join(project_root, "dist"),
        static_url_path=""
    )

    # загружаю обычные настройки приложения
    app.config.from_object(Config)

    # если приложение запускается для тестов,
    # заменяю обычные настройки тестовыми
    if test_config is not None:
        app.config.update(test_config)

    # подключаю базу данных к приложению
    db.init_app(app)

    # подключаю миграции базы данных
    migrate.init_app(app, db)

    # получаю полный путь к swagger.yml
    swagger_file = os.path.join(
        project_root,
        "swagger.yml"
    )

    # открываю файл с описанием моего API
    with open(swagger_file, "r", encoding="utf-8") as file:
        # загружаю YAML в словарь Python
        swagger_template = yaml.safe_load(file)

    # создаю Swagger сразу для этого Flask-приложения
    # передаю ему описание всех моих API-маршрутов
    Swagger(
        app,
        template=swagger_template
    )

    # импортирую модели,
    # чтобы SQLAlchemy видел все таблицы
    # noqa объясняет flake8, что этот импорт нужен специально
    from app import models  # noqa: F401

    # импортирую маршруты приложения
    from app.routes import bp

    # подключаю маршруты к Flask
    app.register_blueprint(bp)

    # возвращаю готовое приложение
    return app
