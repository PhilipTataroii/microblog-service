# импортирую pytest для создания фикстур
import pytest

# импортирую приложение и базу данных
from app import create_app, db

# импортирую модель пользователя
from app.models import User


@pytest.fixture
def app():
    # создаю приложение сразу с тестовыми настройками
    # SQLite работает только в памяти и не трогает PostgreSQL
    app = create_app({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:"
    })

    # создаю контекст тестового приложения
    with app.app_context():
        # создаю таблицы в тестовой SQLite базе
        db.create_all()

        # создаю тестового пользователя Filip
        user = User(
            name="Filip",
            api_key="test"
        )

        # создаю второго тестового пользователя
        user2 = User(
            name="Alex",
            api_key="alex"
        )

        # добавляю пользователей только в тестовую базу
        db.session.add_all([user, user2])

        # сохраняю изменения
        db.session.commit()

        # передаю приложение тестам
        yield app

        # очищаю сессию после теста
        db.session.remove()

        # удаляю таблицы тестовой базы
        db.drop_all()


@pytest.fixture
def client(app):
    # создаю тестовый клиент Flask
    # через него отправляю запросы без запуска настоящего сервера
    return app.test_client()
