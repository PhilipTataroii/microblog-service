# os нужен для работы с путями к файлам
import os

# uuid нужен, чтобы создавать уникальные имена для изображений
import uuid

# импортирую инструменты Flask для маршрутов, ответов и frontend
from flask import (
    Blueprint,
    current_app,
    jsonify,
    request,
    send_from_directory,
)

# secure_filename делает имя загруженного файла безопасным
from werkzeug.utils import secure_filename

# импортирую базу данных
from app import db

# импортирую модели пользователя, твита и изображения
from app.models import Media, Tweet, User

# импортирую функцию, которая находит пользователя по api-key
from app.utils import get_current_user


# создаю Blueprint, в котором будут находиться маршруты API
bp = Blueprint("api", __name__)


# создаю тестовый маршрут главной страницы
@bp.route("/")
def index():
    # открываю готовую главную страницу из папки dist
    return current_app.send_static_file("index.html")


# создаю маршрут для отображения загруженных изображений
@bp.route("/uploads/<path:filename>")
def uploaded_file(filename):
    # получаю путь к корню моего проекта
    project_root = os.path.abspath(
        os.path.join(current_app.root_path, "..")
    )

    # получаю полный путь к папке uploads
    uploads_folder = os.path.join(project_root, "uploads")

    # отправляю изображение пользователю
    return send_from_directory(
        uploads_folder,
        filename
    )


# создаю маршрут для получения данных текущего пользователя
@bp.route("/api/users/me", methods=["GET"])
def get_me():
    # получаю текущего пользователя по api-key
    user = get_current_user()

    # если пользователя не нашли
    if user is None:
        return jsonify({
            "result": False,
            "error_type": "Unauthorized",
            "error_message": "Invalid or missing api-key"
        }), 401

    # возвращаю информацию о пользователе
    return jsonify({
        "result": True,
        "user": {
            # id пользователя
            "id": user.id,

            # имя пользователя
            "name": user.name,

            # пользователи, на которых я подписан
            "following": [
                {
                    "id": followed_user.id,
                    "name": followed_user.name
                }
                for followed_user in user.following
            ],

            # пользователи, которые подписаны на меня
            "followers": [
                {
                    "id": follower.id,
                    "name": follower.name
                }
                for follower in user.followers
            ]
        }
    })


# создаю маршрут для добавления нового твита
@bp.route("/api/tweets", methods=["POST"])
def create_tweet():
    # определяю пользователя по api-key
    user = get_current_user()

    # если пользователя не нашли
    if user is None:
        return jsonify({
            "result": False,
            "error_type": "Unauthorized",
            "error_message": "Invalid or missing api-key"
        }), 401

    # получаю JSON из запроса
    data = request.get_json(silent=True)

    # если JSON не передали
    if data is None:
        return jsonify({
            "result": False,
            "error_type": "BadRequest",
            "error_message": "JSON body is required"
        }), 400

    # получаю текст твита
    tweet_data = data.get("tweet_data")

    # получаю список id изображений
    tweet_media_ids = data.get("tweet_media_ids", [])

    # проверяю текст твита
    if not tweet_data or not tweet_data.strip():
        return jsonify({
            "result": False,
            "error_type": "BadRequest",
            "error_message": "tweet_data is required"
        }), 400

    # создаю новый твит
    new_tweet = Tweet(
        content=tweet_data.strip(),
        author_id=user.id
    )

    # добавляю твит в сессию
    db.session.add(new_tweet)

    # получаю id твита до окончательного commit
    db.session.flush()

    # перебираю изображения, которые нужно добавить к твиту
    for media_id in tweet_media_ids:
        # ищу изображение по id
        media = db.session.get(Media, media_id)

        # если изображение существует и ещё свободно
        if media is not None and media.tweet_id is None:
            # связываю изображение с твитом
            media.tweet_id = new_tweet.id

    # сохраняю изменения
    db.session.commit()

    # возвращаю id созданного твита
    return jsonify({
        "result": True,
        "tweet_id": new_tweet.id
    }), 201


# создаю маршрут для удаления твита
@bp.route("/api/tweets/<int:tweet_id>", methods=["DELETE"])
def delete_tweet(tweet_id):
    # определяю пользователя по api-key
    user = get_current_user()

    # если пользователя не нашли
    if user is None:
        return jsonify({
            "result": False,
            "error_type": "Unauthorized",
            "error_message": "Invalid or missing api-key"
        }), 401

    # ищу твит по id
    tweet = db.session.get(Tweet, tweet_id)

    # если твита нет
    if tweet is None:
        return jsonify({
            "result": False,
            "error_type": "NotFound",
            "error_message": "Tweet not found"
        }), 404

    # запрещаю удалять чужой твит
    if tweet.author_id != user.id:
        return jsonify({
            "result": False,
            "error_type": "Forbidden",
            "error_message": "You cannot delete another user's tweet"
        }), 403

    # удаляю твит
    db.session.delete(tweet)

    # сохраняю изменения
    db.session.commit()

    # возвращаю успешный результат
    return jsonify({
        "result": True
    })


# создаю маршрут для загрузки изображения
@bp.route("/api/medias", methods=["POST"])
def upload_media():
    # определяю пользователя по api-key
    user = get_current_user()

    # если пользователя не нашли
    if user is None:
        return jsonify({
            "result": False,
            "error_type": "Unauthorized",
            "error_message": "Invalid or missing api-key"
        }), 401

    # проверяю наличие файла
    if "file" not in request.files:
        return jsonify({
            "result": False,
            "error_type": "BadRequest",
            "error_message": "File is required"
        }), 400

    # получаю файл
    file = request.files["file"]

    # проверяю, что файл был выбран
    if file.filename == "":
        return jsonify({
            "result": False,
            "error_type": "BadRequest",
            "error_message": "File is required"
        }), 400

    # делаю имя файла безопасным
    original_filename = secure_filename(file.filename)

    # получаю расширение файла
    extension = os.path.splitext(original_filename)[1]

    # создаю уникальное имя файла
    filename = f"{uuid.uuid4().hex}{extension}"

    # создаю путь к файлу
    file_path = os.path.join("uploads", filename)

    # сохраняю файл
    file.save(file_path)

    # создаю запись изображения в базе
    media = Media(
        file_path=file_path
    )

    # добавляю запись
    db.session.add(media)

    # сохраняю изменения
    db.session.commit()

    # возвращаю id изображения
    return jsonify({
        "result": True,
        "media_id": media.id
    }), 201


# создаю маршрут для добавления лайка
@bp.route("/api/tweets/<int:tweet_id>/likes", methods=["POST"])
def like_tweet(tweet_id):
    # определяю пользователя по api-key
    user = get_current_user()

    # если пользователя не нашли
    if user is None:
        return jsonify({
            "result": False,
            "error_type": "Unauthorized",
            "error_message": "Invalid or missing api-key"
        }), 401

    # ищу твит
    tweet = db.session.get(Tweet, tweet_id)

    # если твита нет
    if tweet is None:
        return jsonify({
            "result": False,
            "error_type": "NotFound",
            "error_message": "Tweet not found"
        }), 404

    # если пользователь ещё не ставил лайк
    if user not in tweet.liked_by:
        # добавляю пользователя в список лайков
        tweet.liked_by.append(user)

        # сохраняю лайк
        db.session.commit()

    # возвращаю успешный результат
    return jsonify({
        "result": True
    })


# создаю маршрут для удаления лайка
@bp.route("/api/tweets/<int:tweet_id>/likes", methods=["DELETE"])
def unlike_tweet(tweet_id):
    # определяю пользователя по api-key
    user = get_current_user()

    # если пользователя не нашли
    if user is None:
        return jsonify({
            "result": False,
            "error_type": "Unauthorized",
            "error_message": "Invalid or missing api-key"
        }), 401

    # ищу твит
    tweet = db.session.get(Tweet, tweet_id)

    # если твита нет
    if tweet is None:
        return jsonify({
            "result": False,
            "error_type": "NotFound",
            "error_message": "Tweet not found"
        }), 404

    # если пользователь ставил лайк
    if user in tweet.liked_by:
        # удаляю его лайк
        tweet.liked_by.remove(user)

        # сохраняю изменения
        db.session.commit()

    # возвращаю успешный результат
    return jsonify({
        "result": True
    })


# создаю маршрут для подписки на пользователя
@bp.route("/api/users/<int:user_id>/follow", methods=["POST"])
def follow_user(user_id):
    # определяю текущего пользователя по api-key
    current_user = get_current_user()

    # если пользователя не нашли
    if current_user is None:
        return jsonify({
            "result": False,
            "error_type": "Unauthorized",
            "error_message": "Invalid or missing api-key"
        }), 401

    # ищу пользователя, на которого хотим подписаться
    user_to_follow = db.session.get(User, user_id)

    # если такого пользователя нет
    if user_to_follow is None:
        return jsonify({
            "result": False,
            "error_type": "NotFound",
            "error_message": "User not found"
        }), 404

    # запрещаю пользователю подписываться на самого себя
    if current_user.id == user_to_follow.id:
        return jsonify({
            "result": False,
            "error_type": "BadRequest",
            "error_message": "You cannot follow yourself"
        }), 400

    # проверяю, что подписки ещё нет
    if user_to_follow not in current_user.following:
        # добавляю пользователя в мои подписки
        current_user.following.append(user_to_follow)

        # сохраняю подписку в базе данных
        db.session.commit()

    # возвращаю успешный результат
    return jsonify({
        "result": True
    })


# создаю маршрут для отписки от пользователя
@bp.route("/api/users/<int:user_id>/follow", methods=["DELETE"])
def unfollow_user(user_id):
    # определяю текущего пользователя по api-key
    current_user = get_current_user()

    # если пользователя не нашли
    if current_user is None:
        return jsonify({
            "result": False,
            "error_type": "Unauthorized",
            "error_message": "Invalid or missing api-key"
        }), 401

    # ищу пользователя, от которого хотим отписаться
    user_to_unfollow = db.session.get(User, user_id)

    # если такого пользователя нет
    if user_to_unfollow is None:
        return jsonify({
            "result": False,
            "error_type": "NotFound",
            "error_message": "User not found"
        }), 404

    # если пользователь находится в моих подписках
    if user_to_unfollow in current_user.following:
        # удаляю пользователя из моих подписок
        current_user.following.remove(user_to_unfollow)

        # сохраняю изменения в базе данных
        db.session.commit()

    # возвращаю успешный результат
    return jsonify({
        "result": True
    })


# создаю маршрут для просмотра профиля пользователя по его id
@bp.route("/api/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    # определяю текущего пользователя по api-key
    # без правильного ключа смотреть профиль нельзя
    current_user = get_current_user()

    # если api-key отсутствует или неправильный
    if current_user is None:
        return jsonify({
            "result": False,
            "error_type": "Unauthorized",
            "error_message": "Invalid or missing api-key"
        }), 401

    # ищу пользователя, профиль которого хотим посмотреть
    user = db.session.get(User, user_id)

    # если пользователя с таким id нет
    if user is None:
        return jsonify({
            "result": False,
            "error_type": "NotFound",
            "error_message": "User not found"
        }), 404

    # возвращаю информацию о найденном пользователе
    return jsonify({
        "result": True,
        "user": {
            # id пользователя
            "id": user.id,

            # имя пользователя
            "name": user.name,

            # список пользователей, на которых он подписан
            "following": [
                {
                    "id": followed_user.id,
                    "name": followed_user.name
                }
                for followed_user in user.following
            ],

            # список его подписчиков
            "followers": [
                {
                    "id": follower.id,
                    "name": follower.name
                }
                for follower in user.followers
            ]
        }
    })


# создаю маршрут для получения ленты твитов
@bp.route("/api/tweets", methods=["GET"])
def get_tweets():
    # определяю текущего пользователя по api-key
    user = get_current_user()

    # если api-key отсутствует или неправильный
    if user is None:
        return jsonify({
            "result": False,
            "error_type": "Unauthorized",
            "error_message": "Invalid or missing api-key"
        }), 401

    # получаю id пользователей, на которых я подписан
    following_ids = [
        followed_user.id
        for followed_user in user.following
    ]

    # добавляю свой id
    # так в ленте будут также мои собственные твиты
    following_ids.append(user.id)

    # получаю твиты мои и пользователей, на которых я подписан
    tweets = Tweet.query.filter(
        Tweet.author_id.in_(following_ids)
    ).all()

    # сортирую твиты сначала по количеству лайков
    # самые популярные твиты будут выше
    # если лайков одинаково, новый твит будет выше старого
    tweets.sort(
        key=lambda tweet: (
            len(tweet.liked_by),
            tweet.created_at
        ),
        reverse=True
    )

    # создаю список, который отправлю фронтенду
    tweets_data = []

    # перебираю найденные твиты
    for tweet in tweets:
        # добавляю информацию о каждом твите
        tweets_data.append({
            # id твита
            "id": tweet.id,

            # текст твита
            "content": tweet.content,

            # изображения этого твита
            "attachments": [
                media.file_path
                for media in tweet.media
            ],

            # информация об авторе твита
            "author": {
                "id": tweet.author.id,
                "name": tweet.author.name
            },

            # пользователи, которые поставили лайк
            "likes": [
                {
                    "user_id": liked_user.id,
                    "name": liked_user.name
                }
                for liked_user in tweet.liked_by
            ]
        })

    # возвращаю готовую ленту
    return jsonify({
        "result": True,
        "tweets": tweets_data
    })
