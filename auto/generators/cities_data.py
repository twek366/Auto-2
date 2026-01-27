from helpers.cities import generate_unique_city_name


def generate_update_payload(new_name=None):

    if not new_name:
        new_name = generate_unique_city_name()
    return {"name": new_name}, new_name

def update_city(api, city_id, new_name=None):
    payload, name = generate_update_payload(new_name)
    resp = api.update(city_id, payload)
    return resp, name