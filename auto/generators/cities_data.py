import uuid

from faker import Faker

fake = Faker("ru_RU")


def generate_city_payload(**overrides) -> dict:

    defaults = {"name": f"smoke-{uuid.uuid4().hex[:8]}{fake.city()}"}
    return {**defaults, **overrides}


def generate_update_city_payload(**overrides) -> dict:
    return {"name": f"upd-{uuid.uuid4().hex[:8]}{fake.city()}", **overrides}
