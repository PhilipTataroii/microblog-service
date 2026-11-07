# импортирую базу данных
from app import db

# импортирую модель твита
from app.models import Tweet


# проверяю создание нового твита
def test_create_tweet(client, app):
    # отправляю POST-запрос от пользователя Filip
    response = client.post(
        "/api/tweets",
        headers={"api-key": "test"},
        json={
            "tweet_data": "Тестовый твит",
            "tweet_media_ids": []
        }
    )

    # получаю JSON из ответа
    data = response.get_json()

    # проверяю код успешного создания
    assert response.status_code == 201

    # проверяю результат
    assert data["result"] is True

    # проверяю, что сервер вернул id твита
    assert "tweet_id" in data

    # открываю контекст приложения для проверки базы
    with app.app_context():
        # ищу созданный твит
        tweet = db.session.get(Tweet, data["tweet_id"])

        # проверяю, что твит действительно существует
        assert tweet is not None

        # проверяю текст твита
        assert tweet.content == "Тестовый твит"

        # проверяю, что автором является Filip с id 1
        assert tweet.author_id == 1


# проверяю удаление своего твита
def test_delete_tweet(client, app):
    # сначала создаю твит через API
    create_response = client.post(
        "/api/tweets",
        headers={"api-key": "test"},
        json={
            "tweet_data": "Твит для удаления",
            "tweet_media_ids": []
        }
    )

    # получаю id созданного твита
    tweet_id = create_response.get_json()["tweet_id"]

    # удаляю созданный твит
    response = client.delete(
        f"/api/tweets/{tweet_id}",
        headers={"api-key": "test"}
    )

    # получаю JSON
    data = response.get_json()

    # проверяю успешный HTTP-код
    assert response.status_code == 200

    # проверяю успешный результат
    assert data["result"] is True

    # проверяю базу данных
    with app.app_context():
        # пытаюсь найти удалённый твит
        tweet = db.session.get(Tweet, tweet_id)

        # после удаления его уже не должно быть
        assert tweet is None


# проверяю удаление несуществующего твита
def test_delete_missing_tweet(client):
    # пытаюсь удалить твит с несуществующим id
    response = client.delete(
        "/api/tweets/9999",
        headers={"api-key": "test"}
    )

    # получаю JSON
    data = response.get_json()

    # сервер должен вернуть 404
    assert response.status_code == 404

    # проверяю формат ошибки
    assert data["result"] is False
    assert data["error_type"] == "NotFound"
