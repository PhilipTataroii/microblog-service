# импортирую request, чтобы получать данные из HTTP-запроса
from flask import request

# импортирую модель пользователя
from app.models import User


def get_current_user():
    # получаю api-key из заголовка запроса
    api_key = request.headers.get("api-key")

    # если api-key вообще не передали, возвращаю None
    if not api_key:
        return None

    # ищу пользователя в базе по его api-key
    user = User.query.filter_by(api_key=api_key).first()

    # возвращаю найденного пользователя
    # если такого api-key нет, здесь будет None
    return user
