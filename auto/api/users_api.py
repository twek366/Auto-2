from api.base_client import BaseApiClient
from models.user import UserReadDto


class UsersApi(BaseApiClient):
    def list(self):
        return self.get("/api/users")

    def get_by_id(self, user_id: int):
        return self.get(f"/api/users/{user_id}", response_model=UserReadDto)

    def update(self, user_id: int, payload: dict):
        return self.put(f"/api/users/{user_id}", json=payload, response_model=UserReadDto)

    def delete_by_id(self, user_id: int):
        return self.delete(f"/api/users/{user_id}")

    def get_profile(self):
        return self.get("/api/users/profile")

    def upload_avatar(self, user_id: int, file_path: str):
        return self.post_file(
            endpoint=f"/users/{user_id}/avatar",
            file_field="avatar",
            file_path=file_path,
            content_type="image/png",
        )