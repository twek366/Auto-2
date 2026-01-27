import json
from pathlib import Path

import allure
import httpx
from pydantic import ValidationError

from config.settings import base_url, timeout
from logging_config import logger


class BaseApiClient:
    def __init__(self, token: str | None = None):
        self.base_url = base_url
        self._client = httpx.Client(base_url=self.base_url, timeout=timeout)
        self._token = token

    def _headers(self):
        headers = {"Content-Type": "application/json"}
        if self._token:
            headers["Authorization"] = "Bearer *****"
        return headers

    def _real_headers(self):
        headers = {"Content-Type": "application/json"}
        if self._token:
            headers["Authorization"] = f"Bearer {self._token}"
        return headers

    def _attach_request(self, request: httpx.Request):
        allure.attach(
            json.dumps(
                {
                    "method": request.method,
                    "url": str(request.url),
                    "headers": dict(request.headers),
                    "body": request.content.decode(errors="ignore") if request.content else None,
                },
                indent=2,
                ensure_ascii=False,
            ),
            name="Request",
            attachment_type=allure.attachment_type.JSON,
        )

    def _attach_response(self, response: httpx.Response):
        allure.attach(
            json.dumps(
                {
                    "status_code": response.status_code,
                    "headers": dict(response.headers),
                    "body": response.text,
                },
                indent=2,
                ensure_ascii=False,
            ),
            name="Response",
            attachment_type=allure.attachment_type.JSON,
        )

    def _log_request_response(self, response: httpx.Response):
        req = response.request

        logger.info(f">>> {req.method} {req.url}")
        logger.debug(f">>> Headers: {req.headers}")
        if req.content:
            try:
                logger.debug(f">>> Body: {req.content.decode()}")
            except Exception:
                logger.debug(f">>> Body (binary): {req.content}")

        logger.info(f"<<< Status: {response.status_code}")
        logger.debug(f"<<< Response body: {response.text}")

        self._attach_request(req)
        self._attach_response(response)

    def _validate_response_schema(self, response, model):
        if model is None:
            return response

        if not (200 <= response.status_code < 300):
            return response

        if not response.content:
            return response

        try:
            data = response.json()
        except ValueError:
            return response

        with allure.step(f"Schema validation: {model.__name__}"):
            try:
                model.model_validate(data)
            except ValidationError as e:
                allure.attach(
                    e.json(),
                    name="Schema validation error",
                    attachment_type=allure.attachment_type.JSON,
                )
                raise

        return response

    def get(self, path: str, params: dict | None = None, response_model=None):
        with allure.step(f"GET {path}"):
            response = self._client.get(
                path,
                headers=self._real_headers(),
                params=params,
            )
            self._log_request_response(response)
            return self._validate_response_schema(response, response_model)

    def post(self, path: str, json: dict | None = None, response_model=None):
        with allure.step(f"POST {path}"):
            response = self._client.post(
                path,
                headers=self._real_headers(),
                json=json,
            )
            self._log_request_response(response)
            return self._validate_response_schema(response, response_model)

    def put(self, path: str, json: dict | None = None, response_model=None):
        with allure.step(f"PUT {path}"):
            response = self._client.put(
                path,
                headers=self._real_headers(),
                json=json,
            )
            self._log_request_response(response)
            return self._validate_response_schema(response, response_model)

    def delete(self, path: str):
        with allure.step(f"DELETE {path}"):
            response = self._client.delete(
                path,
                headers=self._real_headers(),
            )
            self._log_request_response(response)
            return response

    def post_file(
        self,
        endpoint: str,
        file_field: str,
        file_path: str | Path,
        content_type: str = "image/jpeg",
        extra_fields: dict | None = None,
    ) -> httpx.Response:
        file_path = Path(file_path)

        with allure.step(f"POST FILE {endpoint}"):
            with file_path.open("rb") as file:
                files = {
                    file_field: (
                        file_path.name,
                        file,
                        content_type,
                    )
                }

                response = self._client.post(
                    f"{self.base_url}{endpoint}",
                    headers=self._real_headers(),
                    files=files,
                    data=extra_fields or {},
                )

                allure.attach(
                    file_path.name,
                    name="Uploaded file",
                    attachment_type=allure.attachment_type.TEXT,
                )

                self._log_request_response(response)
                return response
