import allure
import pytest

from api.auth_api import AuthApi
from config.settings import login_owner, pass_owner
from logging_config import logger


@allure.epic("Controller auth")
@allure.feature("Логин")
@allure.story("POST /auth/login")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.smoke
def test_login_success_token_changes():
    """Проверка авторизации"""
    api = AuthApi()

    resp1 = api.login(login=login_owner, password=pass_owner)
    assert resp1.status_code == 200
    data1 = resp1.json()
    assert "token" in data1 and data1["token"] is not None
    token1 = data1["token"]

    resp2 = api.login(login=login_owner, password=pass_owner)
    assert resp2.status_code == 200
    data2 = resp2.json()
    assert "token" in data2 and data2["token"] is not None
    token2 = data2["token"]

    assert token1 != token2


@allure.epic("Controller auth")
@allure.feature("Обновление токена")
@allure.story("GET /auth/refresh-token")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.smoke
def test_refresh_token(admin_token):
    """Проверка обновления токена"""
    logger.info("Начало теста обновления токена")

    api = AuthApi(token=admin_token)
    resp = api.refresh()

    assert resp.status_code == 200, f"Ожидался статус 200, получен {resp.status_code}. Ответ: {resp.text}"
    logger.info("Статус код 200 подтверждён")

    data = resp.json()
    assert "token" in data, f"Ответ не содержит ключ 'token'. Ответ: {data}"

    logger.info("Тест обновления токена успешно завершён")
