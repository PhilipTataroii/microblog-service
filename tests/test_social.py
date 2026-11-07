# импортирую базу данных
from app import db

# импортирую модели пользователя и твита
from app.models import Tweet, User


# проверяю, что пользователь может поставить лайк твиту
def test_like_tweet(client, app):
    # создаю твит от пользователя Alex
    response = client.post(
        "/api/tweets",
        headers={"api-key": "alex"},
        json={
            "tweet_data": "Твит Alex для проверки лайка",
            "tweet_media_ids": []
        }
    )

    # получаю id созданного твита
    tweet_id = response.get_json()["tweet_id"]

    # пользователь Filip ставит лайк твиту Alex
    response = client.post(
        f"/api/tweets/{tweet_id}/likes",
        headers={"api-key": "test"}
    )

    # проверяю успешный ответ
    assert response.status_code == 200
    assert response.get_json()["result"] is True

    # проверяю, что лайк действительно сохранился в базе
    with app.app_context():
        # получаю твит из тестовой базы
        tweet = db.session.get(Tweet, tweet_id)

        # у твита должен быть один лайк
        assert len(tweet.liked_by) == 1

        # лайк должен принадлежать Filip
        assert tweet.liked_by[0].name == "Filip"


# проверяю удаление лайка
def test_unlike_tweet(client, app):
    # создаю твит от Alex
    response = client.post(
        "/api/tweets",
        headers={"api-key": "alex"},
        json={
            "tweet_data": "Твит для удаления лайка",
            "tweet_media_ids": []
        }
    )

    # получаю id твита
    tweet_id = response.get_json()["tweet_id"]

    # Filip сначала ставит лайк
    client.post(
        f"/api/tweets/{tweet_id}/likes",
        headers={"api-key": "test"}
    )

    # Filip убирает свой лайк
    response = client.delete(
        f"/api/tweets/{tweet_id}/likes",
        headers={"api-key": "test"}
    )

    # проверяю успешный ответ
    assert response.status_code == 200
    assert response.get_json()["result"] is True

    # проверяю базу данных
    with app.app_context():
        # получаю твит
        tweet = db.session.get(Tweet, tweet_id)

        # после удаления лайков быть не должно
        assert len(tweet.liked_by) == 0


# проверяю подписку на другого пользователя
def test_follow_user(client, app):
    # Filip подписывается на Alex с id 2
    response = client.post(
        "/api/users/2/follow",
        headers={"api-key": "test"}
    )

    # проверяю успешный ответ
    assert response.status_code == 200
    assert response.get_json()["result"] is True

    # проверяю подписку непосредственно в базе
    with app.app_context():
        # получаю Filip
        filip = db.session.get(User, 1)

        # у Filip должна быть одна подписка
        assert len(filip.following) == 1

        # подписан он должен быть на Alex
        assert filip.following[0].name == "Alex"


# проверяю отписку от пользователя
def test_unfollow_user(client, app):
    # сначала Filip подписывается на Alex
    client.post(
        "/api/users/2/follow",
        headers={"api-key": "test"}
    )

    # теперь Filip отписывается от Alex
    response = client.delete(
        "/api/users/2/follow",
        headers={"api-key": "test"}
    )

    # проверяю успешный ответ
    assert response.status_code == 200
    assert response.get_json()["result"] is True

    # проверяю изменения в базе
    with app.app_context():
        # получаю Filip
        filip = db.session.get(User, 1)

        # список подписок должен снова стать пустым
        assert len(filip.following) == 0


# проверяю просмотр профиля другого пользователя
def test_get_user_profile(client):
    # Filip запрашивает профиль Alex
    response = client.get(
        "/api/users/2",
        headers={"api-key": "test"}
    )

    # получаю JSON
    data = response.get_json()

    # проверяю успешный ответ
    assert response.status_code == 200
    assert data["result"] is True

    # проверяю данные Alex
    assert data["user"]["id"] == 2
    assert data["user"]["name"] == "Alex"


# проверяю, что твиты подписанного пользователя появляются в ленте
def test_tweets_feed(client):
    # Filip подписывается на Alex
    client.post(
        "/api/users/2/follow",
        headers={"api-key": "test"}
    )

    # Alex создаёт твит
    create_response = client.post(
        "/api/tweets",
        headers={"api-key": "alex"},
        json={
            "tweet_data": "Твит Alex в ленте",
            "tweet_media_ids": []
        }
    )

    # получаю id созданного твита
    tweet_id = create_response.get_json()["tweet_id"]

    # Filip получает свою ленту
    response = client.get(
        "/api/tweets",
        headers={"api-key": "test"}
    )

    # получаю JSON ленты
    data = response.get_json()

    # проверяю успешный ответ
    assert response.status_code == 200
    assert data["result"] is True

    # получаю id всех твитов из ленты
    tweet_ids = [
        tweet["id"]
        for tweet in data["tweets"]
    ]

    # твит Alex должен присутствовать в ленте Filip
    assert tweet_id in tweet_ids


# проверяю сортировку твитов по количеству лайков
def test_tweets_sorted_by_likes(client):
    # Filip подписывается на Alex
    client.post(
        "/api/users/2/follow",
        headers={"api-key": "test"}
    )

    # Filip создаёт свой твит без лайков
    filip_response = client.post(
        "/api/tweets",
        headers={"api-key": "test"},
        json={
            "tweet_data": "Твит Filip без лайков",
            "tweet_media_ids": []
        }
    )

    # сохраняю id твита Filip
    filip_tweet_id = filip_response.get_json()["tweet_id"]

    # Alex создаёт второй твит
    alex_response = client.post(
        "/api/tweets",
        headers={"api-key": "alex"},
        json={
            "tweet_data": "Популярный твит Alex",
            "tweet_media_ids": []
        }
    )

    # сохраняю id твита Alex
    alex_tweet_id = alex_response.get_json()["tweet_id"]

    # Filip ставит лайк твиту Alex
    client.post(
        f"/api/tweets/{alex_tweet_id}/likes",
        headers={"api-key": "test"}
    )

    # получаю ленту Filip
    response = client.get(
        "/api/tweets",
        headers={"api-key": "test"}
    )

    # получаю список твитов
    tweets = response.get_json()["tweets"]

    # популярный твит Alex должен быть первым
    assert tweets[0]["id"] == alex_tweet_id

    # твит Filip без лайков должен идти после него
    assert tweets[1]["id"] == filip_tweet_id
