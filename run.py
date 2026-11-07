# импортирую функцию, которая создаёт Flask-приложение
from app import create_app


# создаю приложение
app = create_app()


# этот код запускается, когда я запускаю файл через python run.py
if __name__ == "__main__":
    # запускаю Flask-сервер
    # host 0.0.0.0 нужен, чтобы приложение было доступно из Docker
    # порт 5000 использую для моего MicroBlog
    # debug=True оставляю для удобной разработки
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )
