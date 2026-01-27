import allure
import pytest

from generators.cities_data import update_city
from helpers.cities import assert_city_response
from logging_config import logger


@allure.epic("Controller cities")
@allure.feature("Создание города")
@allure.story("POST /cities")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.smoke
def test_create_city(city):
    """Проверка создания города"""
    assert city["id"] is not None
    logger.info(f"Город успешно создан: {city['name']}")



@allure.epic("Controller cities")
@allure.feature("Получение города")
@allure.story("GET /cities/{id}")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.smoke
def test_get_city(city):
    """Получение города по ID"""
    resp = city["api"].get_by_id(city["id"])
    assert_city_response(resp, city["name"])

    logger.info(f"Город успешно получен: {city['name']}")



@allure.epic("Controller cities")
@allure.feature("Обновление города")
@allure.story("PUT /cities/{id}")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.smoke
def test_update_city(city):
    """Обновление города"""
    resp, new_name = update_city(city["api"], city["id"])

    assert resp.status_code == 200
    assert resp.json()["name"] == new_name

    logger.info(
        f"Город {city['id']} успешно обновлён: {city['name']} → {new_name}"
    )



@allure.epic("Controller cities")
@allure.feature("Удаление города")
@allure.story("DELETE /cities/{id}")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.smoke
def test_delete_city(city):
    """Удаление города"""
    delete_resp = city["api"].delete_by_id(city["id"])
    assert delete_resp.status_code == 204

    city["deleted"] = True

    get_after_delete = city["api"].get_by_id(city["id"])
    assert get_after_delete.status_code == 404

    logger.info(f"Город успешно удалён: {city['name']}")