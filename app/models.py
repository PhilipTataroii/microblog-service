# импортирую datetime, чтобы сохранять время создания твита
from datetime import datetime

# импортирую db, через который работаю с базой данных
from app import db


# таблица лайков
# связывает пользователя с твитом, который он лайкнул
likes = db.Table(
    "likes",

    # id пользователя, который поставил лайк
    db.Column(
        "user_id",
        db.Integer,
        db.ForeignKey("users.id"),
        primary_key=True
    ),

    # id твита, которому поставили лайк
    db.Column(
        "tweet_id",
        db.Integer,
        db.ForeignKey("tweets.id"),
        primary_key=True
    )
)


# таблица подписок пользователей друг на друга
follows = db.Table(
    "follows",

    # пользователь, который подписывается
    db.Column(
        "follower_id",
        db.Integer,
        db.ForeignKey("users.id"),
        primary_key=True
    ),

    # пользователь, на которого подписываются
    db.Column(
        "followed_id",
        db.Integer,
        db.ForeignKey("users.id"),
        primary_key=True
    )
)


class User(db.Model):
    # название таблицы в базе данных
    __tablename__ = "users"

    # уникальный id пользователя
    id = db.Column(db.Integer, primary_key=True)

    # имя пользователя
    name = db.Column(db.String(100), nullable=False)

    # ключ пользователя
    # фронтенд будет отправлять его в заголовке api-key
    api_key = db.Column(
        db.String(100),
        unique=True,
        nullable=False
    )

    # получаю все твиты этого пользователя
    tweets = db.relationship(
        "Tweet",
        back_populates="author",
        cascade="all, delete-orphan"
    )

    # получаю твиты, которым пользователь поставил лайк
    liked_tweets = db.relationship(
        "Tweet",
        secondary=likes,
        back_populates="liked_by"
    )

    # пользователи, на которых подписан этот пользователь
    following = db.relationship(
        "User",

        # использую таблицу follows для связи пользователей
        secondary=follows,

        # здесь мой id находится в follower_id
        primaryjoin=id == follows.c.follower_id,

        # здесь id другого пользователя находится в followed_id
        secondaryjoin=id == follows.c.followed_id,

        # позволяет получить обратную связь:
        # кто подписан на этого пользователя
        backref="followers"
    )


class Tweet(db.Model):
    # название таблицы с твитами
    __tablename__ = "tweets"

    # уникальный id твита
    id = db.Column(db.Integer, primary_key=True)

    # текст твита
    content = db.Column(db.Text, nullable=False)

    # сохраняю текущее время создания твита
    # использую datetime.now вместо устаревшего utcnow
    created_at = db.Column(
        db.DateTime,
        default=datetime.now,
        nullable=False
    )

    # id автора твита
    author_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    # получаю автора этого твита
    author = db.relationship(
        "User",
        back_populates="tweets"
    )

    # получаю пользователей, которые лайкнули этот твит
    liked_by = db.relationship(
        "User",
        secondary=likes,
        back_populates="liked_tweets"
    )

    # получаю все изображения этого твита
    media = db.relationship(
        "Media",
        back_populates="tweet",
        cascade="all, delete-orphan"
    )


class Media(db.Model):
    # название таблицы с изображениями
    __tablename__ = "media"

    # уникальный id изображения
    id = db.Column(db.Integer, primary_key=True)

    # сохраняю путь или имя загруженного файла
    file_path = db.Column(
        db.String(255),
        nullable=False
    )

    # id твита, к которому относится изображение
    # nullable=True, потому что картинка сначала загружается
    # через /api/medias, а твит создаётся после этого
    tweet_id = db.Column(
        db.Integer,
        db.ForeignKey("tweets.id"),
        nullable=True
    )

    # получаю твит, к которому прикреплена картинка
    tweet = db.relationship(
        "Tweet",
        back_populates="media"
    )
