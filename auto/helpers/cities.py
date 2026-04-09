from WS.models.city import CityReadDto


def get_dto(resp) -> CityReadDto:
    assert resp.status_code in [
        200,
        201,
    ], f"Ошибка API: {resp.status_code} - {resp.text}"
    return CityReadDto.model_validate(resp.json())
