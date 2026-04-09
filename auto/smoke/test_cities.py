import allure
import pytest
from faker import Faker

from WS.helpers.cities import get_dto

fake = Faker("ru_RU")
name = f"Test {fake.city()}"


@allure.epic("Controller cities")
@pytest.mark.smoke
class TestCities:

    @allure.story("POST /cities")
    def test_create_city(self, city_factory):
        """Проверка создания города"""
        city_dto = city_factory(name=f"{name}")

        # Создаём город, проверяем что имя соответствует заданному
        assert city_dto.name == name

    @allure.story("PUT /cities/{id}")
    def test_update_client(self, city):
        """Проверка изменения города"""
        resp = city.api.update(city.id, {"name": name})

        # Вносим изменения в город, проверяем наличие внесенных изменений
        updated_dto = get_dto(resp)
        assert updated_dto.name == name

    @allure.story("DELETE /cities/{id}")
    def test_delete_client(self, city):
        """Проверка удаления города через эндпоинт"""
        # Удаляем созданный город, смотри что контент отсутствует
        assert city.api.delete_by_id(city.id).status_code == 204
        assert city.api.get_by_id(city.id).status_code == 404
