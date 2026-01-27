from api.base_client import BaseApiClient
from models.auth import CurrentUserDto, UserAuthDto


class AuthApi(BaseApiClient):
    def login(self, login: str, password: str):
        return self.post("/api/auth/login", json={"login": login, "password": password}, response_model=CurrentUserDto)

    def refresh(self):
        return self.get("/api/auth/refresh-token", response_model=CurrentUserDto)

    def register(self, payload: dict):
        return self.post("/api/auth/register", json=payload, response_model=UserAuthDto)