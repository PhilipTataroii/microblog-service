# беру официальный образ Python
FROM python:3.14-slim

# создаю рабочую папку приложения внутри контейнера
WORKDIR /app

# копирую файл с зависимостями
COPY requirements.txt .

# устанавливаю зависимости моего проекта
RUN pip install --no-cache-dir -r requirements.txt

# копирую весь проект внутрь контейнера
COPY . .

# указываю порт, на котором работает Flask
EXPOSE 5000

# запускаю моё Flask-приложение
CMD ["python", "run.py"]