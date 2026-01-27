import json

import allure
import pytest

from api.cities_api import CitiesApi
from helpers.cities import *
from logging_config import logger


@pytest.fixture
def city_factory(admin_token):

    api = CitiesApi(token=admin_token)
    created_cities = []

    def _create_city(name: str | None = None):
        city_name = name or generate_unique_city_name()

        with allure.step(f"Создание города: {city_name}"):
            payload = create_city_payload(city_name)

            allure.attach(
                json.dumps(payload, indent=2),
                name="Create city payload",
                attachment_type=allure.attachment_type.JSON,
            )

            resp = api.create(payload)

            allure.attach(
                resp.text,
                name="Create city response",
                attachment_type=allure.attachment_type.JSON,
            )

            data = assert_city_response(resp, city_name)

        city_data = {
            "id": data["id"],
            "name": city_name,
            "api": api,
            "deleted": False,
        }

        created_cities.append(city_data)
        return city_data

    yield _create_city

    for city in created_cities:
        if not city["deleted"]:
            with allure.step(f"Удаление тестового города id={city['id']}"):
                delete_resp = api.delete_by_id(city["id"])

                logger.info(
                    f"City delete id={city['id']}, status={delete_resp.status_code}"
                )

                allure.attach(
                    f"Status: {delete_resp.status_code}\n{delete_resp.text}",
                    name="Delete city response",
                    attachment_type=allure.attachment_type.TEXT,
                )


@pytest.fixture
def city(city_factory):
    return city_factory()