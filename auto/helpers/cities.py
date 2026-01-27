import uuid

from models.city import CityCreateDto


def generate_unique_city_name(prefix="smoke-city"):
    return f"{prefix}-{uuid.uuid4().hex[:8]}"

def create_city_payload(name: str):

    return CityCreateDto(name=name).model_dump()

def assert_city_response(resp, expected_name):

    assert resp.status_code == 200 or resp.status_code == 201, \
        f"Ожидался статус 200/201, но получен {resp.status_code}: {resp.text}"
    data = resp.json()
    assert data["name"] == expected_name, f"Ожидаемое имя '{expected_name}', но получили '{data['name']}'"
    return data