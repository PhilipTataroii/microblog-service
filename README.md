# MicroBlog Service

🌐 **Documentation Languages**

🇬🇧 **English** | 🇷🇺 [Русский](README.ru.md) | 🇷🇴 [Română](README.ro.md)

## Overview

MicroBlog is a RESTful microblogging application developed as the final project of the Python Advanced professional training program.

The application allows users to create and delete tweets, upload images, like posts, follow other users, and explore a personalized tweet feed.

The project demonstrates practical backend development skills, REST API design, database management, containerization, and automated testing.

## Features

- Create and delete tweets
- Upload images and attach them to tweets
- Like and unlike tweets
- Follow and unfollow users
- View user profiles
- Browse the tweet feed
- Sort tweets by popularity
- Authenticate users using an `api-key` HTTP header
- Explore interactive API documentation with Swagger
- Run the application using Docker Compose

## Technologies

- **Backend:** Python, Flask
- **Database:** PostgreSQL, SQLAlchemy
- **Database Migrations:** Flask-Migrate, Alembic
- **API Documentation:** Flasgger, Swagger
- **Testing:** Pytest
- **Code Quality:** Flake8
- **Containerization:** Docker, Docker Compose

## Getting Started

### Prerequisites

Make sure Docker and Docker Compose are installed.

### Installation and Deployment

Clone the repository:

```bash
git clone https://github.com/PhilipTataroii/microblog-service.git
cd microblog-service
```

Build and start the application:

```bash
docker compose up -d --build
```

Check the container status:

```bash
docker compose ps
```

Once the application is running, open:

`http://127.0.0.1:5000/`

Stop the application:

```bash
docker compose down
```

## Database

MicroBlog uses PostgreSQL as its relational database.

When running through Docker Compose, PostgreSQL operates in a separate container.

Database migrations are automatically applied before starting the Flask application using:

```bash
flask db upgrade
```

## Authentication

The application identifies users through the HTTP `api-key` header.

Example:

```http
api-key: test
```

The corresponding user must exist in the database.

## REST API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/users/me` | Get the current user |
| GET | `/api/users/<user_id>` | Get a user by ID |
| GET | `/api/tweets` | Retrieve the tweet feed |
| POST | `/api/tweets` | Create a tweet |
| DELETE | `/api/tweets/<tweet_id>` | Delete a tweet |
| POST | `/api/medias` | Upload an image |
| POST | `/api/tweets/<tweet_id>/likes` | Like a tweet |
| DELETE | `/api/tweets/<tweet_id>/likes` | Remove a like |
| POST | `/api/users/<user_id>/follow` | Follow a user |
| DELETE | `/api/users/<user_id>/follow` | Unfollow a user |

## Swagger API Documentation

Interactive API documentation is available at:

`http://127.0.0.1:5000/apidocs/`

Swagger provides information about available endpoints, request parameters, and API operations.

## Testing

Run the automated test suite:

```bash
pytest -v
```

Test results at project completion:

**12 tests passed.**

## Code Quality

Run Flake8 to check code quality:

```bash
flake8 app tests run.py config.py
```

A successful execution completes without reporting errors.

## Project Structure

```text
microblog-service/
├── app/
│   ├── __init__.py
│   ├── models.py
│   ├── routes.py
│   └── utils.py
├── dist/
├── migrations/
├── tests/
├── uploads/
├── config.py
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── run.py
├── swagger.yml
├── README.md
├── README.ru.md
└── README.ro.md
```

## Author

**Filip Tataroi**

Python Backend Developer

GitHub: https://github.com/PhilipTataroii

LinkedIn: https://www.linkedin.com/in/filip-tataroi/

**Project Type:** Python Advanced — Final Educational Project
