import allure
import pytest

from generators.users_data import update_user
from helpers.users import assert_user_get_response
from logging_config import logger


@allure.epic("Controller users")
@allure.feature("Создание пользователя")
@allure.story("POST /users")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.smoke
def test_create_user(user):
    """Проверка создания пользователя"""
    logger.info(
        f"Тест создания пользователя прошёл успешно: {user['username']}"
    )


@allure.epic("Controller users")
@allure.feature("Получение пользователя")
@allure.story("GET /users/{id}")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.smoke
def test_get_user(user):
    """Получение пользователя по ID"""
    get_resp = user["api"].get_by_id(user["id"])
    assert_user_get_response(get_resp, user["username"])


@allure.epic("Controller users")
@allure.feature("Обновление пользователя")
@allure.story("PUT /users/{id}")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.smoke
def test_update_user(user):
    """Обновление данных пользователя"""
    resp, updated_values = update_user(user["api"], user["id"])
    assert resp.status_code == 200

    dto = assert_user_get_response(resp)
    for key, val in updated_values.items():
        assert getattr(dto, key) == val

    logger.info(
        f"Пользователь {user['username']} ({user['id']}) успешно обновлён"
    )

@allure.epic("Controller users")
@allure.feature("Удаление пользователя")
@allure.story("DELETE /users/{id}")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.smoke
def test_delete_user(user):
    """Удаление пользователя"""
    delete_resp = user["api"].delete_by_id(user["id"])
    assert delete_resp.status_code == 204, (
        f"Не удалось удалить пользователя {user['username']}: "
        f"{delete_resp.status_code}"
    )

    get_after_delete = user["api"].get_by_id(user["id"])
    assert get_after_delete.status_code == 404, (
        f"Пользователь {user['username']} не был удалён"
    )

    logger.info(
        f"Тест удаления пользователя прошёл успешно: {user['username']}"
    )


@allure.epic("Controller users")
@allure.feature("Группы и настройки пользователя")
@allure.story("POST /users/{id}/groups & settings")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.smoke
def test_toggle_group_and_settings(user):
    """Переключение групп и настроек пользователя"""
    group_id = 1
    setting_id1 = 1
    setting_id2 = 2

    resp_group = user["api"].toggle_group(user["id"], group_id)
    assert resp_group.status_code == 200, (
        f"Ожидался 200 при установке группы, получено {resp_group.status_code}\n"
        f"Ответ: {resp_group.text[:200]}"
    )

    resp_1 = user["api"].toggle_settings(user["id"], setting_id1)
    assert resp_1.status_code == 200, (
        f"Ожидался 200 при переключении настройки, получено {resp_1.status_code}\n"
        f"Ответ: {resp_1.text[:200]}"
    )

    resp_2 = user["api"].toggle_settings(user["id"], setting_id2)
    assert resp_2.status_code == 200, (
        f"Ожидался 200 при повторном переключении настройки, "
        f"получено {resp_2.status_code}\n"
        f"Ответ: {resp_2.text[:200]}"
    )
