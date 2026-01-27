import uuid
from dataclasses import asdict, dataclass, field
from typing import Any

from models import UserRegisterDto


def generate_unique_username() -> str:
    return f"user_{uuid.uuid4().hex[:8]}"

def generate_unique_email() -> str:
    return f"user_{uuid.uuid4().hex[:8]}@example.com"

def create_user_payload(default_city: int) -> dict:
    dto = UserRegisterDto(
        username=generate_unique_username(),
        email=generate_unique_email(),
        password="Test12345!",
        firstName="Test",
        lastName="User",
        defaultCity=default_city,
        role="ADMINISTRATOR",
    )
    return dto.model_dump(exclude_none=True)

@dataclass
class UserUpdatePayload:
    username: str = field(default_factory=generate_unique_username)
    email: str = field(default_factory=generate_unique_email)
    firstName: str = "UpdatedFirst"
    lastName: str = "UpdatedLast"
    role: str | None = None
    defaultCity: int | None = None

def generate_update_user_payload(**overrides) -> tuple[dict[str, Any], dict[str, Any]]:
    payload_obj = UserUpdatePayload(**overrides)
    payload_dict = asdict(payload_obj)
    payload = {k: v for k, v in payload_dict.items() if v is not None}
    return payload, payload

def update_user(api, user_id: int, **kwargs) -> tuple:
    payload, updated_values = generate_update_user_payload(**kwargs)
    resp = api.update(user_id, payload)
    return resp, updated_values