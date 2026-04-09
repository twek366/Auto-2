import allure
import pytest

from WS.api.cities_api import CitiesApi
from WS.generators.cities_data import generate_city_payload
from WS.helpers.cities import get_dto


@pytest.fixture
def city_factory(admin_token):
    api = CitiesApi(admin_token)
    created_cities = []

    def _factory(cleanup=True, **overrides):
        with allure.step(f"Создание тестового города {overrides.get('name', '')}"):
            payload = generate_city_payload(**overrides)

            allure.attach(
                str(payload),
                name="City Payload",
                attachment_type=allure.attachment_type.JSON,
            )

            resp = api.create(payload)
            dto = get_dto(resp)
            dto.__dict__["api"] = api

            if cleanup:
                created_cities.append(dto)
            return dto

    yield _factory

    if created_cities:
        with allure.step(
            f"Очистка данных: удаление городов ({len(created_cities)} шт.)"
        ):
            for city in reversed(created_cities):
                api.delete_by_id(city.id)


@pytest.fixture
def city(city_factory):
    return city_factory()
