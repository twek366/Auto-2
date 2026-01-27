import os

import allure
import pytest

from api.base_client import BaseApiClient
from fixtures.auth_fixtures import *
from fixtures.city_fixtures import *
from fixtures.user_fixtures import *
from logging_config import logger


@pytest.fixture
def api_client(admin_token):
    return BaseApiClient(token=admin_token)


def pytest_sessionstart(session):
    allure_results_dir = os.getenv("ALLURE_RESULTS_DIR", "allure-results")
    os.makedirs(allure_results_dir, exist_ok=True)

    env_file = os.path.join(allure_results_dir, "environment.properties")
    with open(env_file, "w", encoding="utf-8") as f:
        f.write("PROJECT=API\n")
        f.write("ENV=TEST\n")


@pytest.fixture(autouse=True)
def log_test_start_end(request):
    with allure.step(f"START TEST: {request.node.name}"):
        logger.info(f"START TEST: {request.node.name}")
        yield
        logger.info(f"END TEST: {request.node.name}")


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()

    if rep.when == "call" and rep.failed:
        allure.attach(
            str(rep.longrepr),
            name="Failure reason",
            attachment_type=allure.attachment_type.TEXT,
        )
