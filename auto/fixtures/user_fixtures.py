import allure
import pytest

from api.auth_api import AuthApi
from api.users_api import UsersApi
from generators.users_data import create_user_payload
from helpers.users import assert_user_auth_response
from logging_config import logger


@pytest.fixture
def user(admin_token, city):
    with allure.step("Инициализация Auth API клиента"):
        auth_client = AuthApi(token=admin_token)

    with allure.step("Формирование payload для регистрации пользователя"):
        payload = create_user_payload(default_city=city["id"])

        allure.attach(
            str(payload),
            name="Register payload",
            attachment_type=allure.attachment_type.JSON,
        )

    with allure.step("Регистрация пользователя"):
        create_resp = auth_client.register(payload)
        user_dto = assert_user_auth_response(create_resp)

        allure.attach(
            create_resp.text,
            name="Register response",
            attachment_type=allure.attachment_type.JSON,
        )

    with allure.step("Инициализация Users API клиента"):
        users_client = UsersApi(token=admin_token)

    yield {
        "id": user_dto.id,
        "email": user_dto.email,
        "username": user_dto.username,
        "register_client": auth_client,
        "api": users_client,
        "dto": user_dto,
    }

    with allure.step("Удаление тестового пользователя (teardown)"):
        delete_resp = users_client.delete_by_id(user_dto.id)

        if delete_resp.status_code == 204:
            logger.info(
                f"User {user_dto.email} ({user_dto.id}) deleted in teardown"
            )
        else:
            logger.warning(
                f"Failed to delete user {user_dto.email} ({user_dto.id}): "
                f"{delete_resp.status_code}"
            )

        allure.attach(
            f"Status: {delete_resp.status_code}\n{delete_resp.text}",
            name="Teardown delete response",
            attachment_type=allure.attachment_type.TEXT,
        )
