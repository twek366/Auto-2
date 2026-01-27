import pytest

from api.auth_api import AuthApi
from config.settings import login_owner, pass_owner


@pytest.fixture(scope="session")
def admin_token():
    api = AuthApi()
    resp = api.login(login_owner, pass_owner)
    assert resp.status_code == 200, f"Auth failed: {resp.status_code} {resp.text}"
    data = resp.json()
    token = data.get("token")
    assert token, "No token in login response"
    return token