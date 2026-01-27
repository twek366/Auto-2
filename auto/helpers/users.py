from models.auth import UserAuthDto
from models.user import UserReadDto


def assert_user_auth_response(resp, expected_username=None) -> UserAuthDto:
    assert resp.status_code in (200, 201), \
        f"Ожидался статус 200/201, но получен {resp.status_code}: {resp.text}"

    data = resp.json()
    dto = UserAuthDto.model_validate(data)

    if expected_username is not None:
        assert dto.username == expected_username, \
            f"Ожидался username '{expected_username}', но получен '{dto.username}'"

    return dto

def assert_user_get_response(resp, expected_username: str | None = None) -> UserReadDto:
    assert resp.status_code == 200, \
        f"Unexpected status {resp.status_code}: {resp.text}"

    dto = UserReadDto.model_validate(resp.json())

    if expected_username:
        assert dto.username == expected_username

    return dto
