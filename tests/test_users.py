# проверяю получение текущего пользователя
def test_get_current_user(client):
    # отправляю запрос с правильным api-key
    response = client.get(
        "/api/users/me",
        headers={"api-key": "test"}
    )

    # получаю JSON из ответа
    data = response.get_json()

    # проверяю HTTP-код
    assert response.status_code == 200

    # проверяю успешный результат
    assert data["result"] is True

    # проверяю имя пользователя
    assert data["user"]["name"] == "Filip"

    # проверяю id пользователя
    assert data["user"]["id"] == 1


# проверяю неправильный api-key
def test_get_current_user_with_wrong_api_key(client):
    # отправляю запрос с неправильным ключом
    response = client.get(
        "/api/users/me",
        headers={"api-key": "wrong-key"}
    )

    # получаю JSON
    data = response.get_json()

    # сервер должен вернуть ошибку авторизации
    assert response.status_code == 401

    # проверяю формат ошибки
    assert data["result"] is False
    assert data["error_type"] == "Unauthorized"
