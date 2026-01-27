from api.base_client import BaseApiClient
from models.common import CityReadDto


class CitiesApi(BaseApiClient):

    def list(self):
        return self.get("/api/cities")

    def create(self, payload: dict):
        return self.post(
            "/api/cities",
            json=payload,
            response_model=CityReadDto,
        )

    def get_by_id(self, city_id: int):
        return self.get(
            f"/api/cities/{city_id}",
            response_model=CityReadDto,
        )

    def update(self, city_id: int, payload: dict):
        return self.put(
            f"/api/cities/{city_id}",
            json=payload,
            response_model=CityReadDto,
        )

    def delete_by_id(self, city_id: int):
        return self.delete(f"/api/cities/{city_id}")