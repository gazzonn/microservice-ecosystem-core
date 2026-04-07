from typing import Any

import httpx

from shared.exceptions.api import AppException


class ServiceClient:
    def __init__(self, base_url: str) -> None:
        self.base_url = base_url.rstrip("/")

    async def get(self, path: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
        async with httpx.AsyncClient(timeout=10.0) as client:
            try:
                response = await client.get(f"{self.base_url}{path}", params=params)
                response.raise_for_status()
                return response.json()
            except httpx.HTTPStatusError as error:
                payload = error.response.json()
                raise AppException(
                    message=payload.get("message", "Upstream service returned an error"),
                    error_code=payload.get("error_code", "UPSTREAM_ERROR"),
                    status_code=error.response.status_code,
                    details=payload.get("details", {}),
                ) from error
            except httpx.HTTPError as error:
                raise AppException(
                    message="Upstream service is unavailable",
                    error_code="UPSTREAM_UNAVAILABLE",
                    status_code=503,
                    details={"service_url": self.base_url},
                ) from error

    async def post(self, path: str, json: dict[str, Any]) -> dict[str, Any]:
        async with httpx.AsyncClient(timeout=10.0) as client:
            try:
                response = await client.post(f"{self.base_url}{path}", json=json)
                response.raise_for_status()
                return response.json()
            except httpx.HTTPStatusError as error:
                payload = error.response.json()
                raise AppException(
                    message=payload.get("message", "Upstream service returned an error"),
                    error_code=payload.get("error_code", "UPSTREAM_ERROR"),
                    status_code=error.response.status_code,
                    details=payload.get("details", {}),
                ) from error
            except httpx.HTTPError as error:
                raise AppException(
                    message="Upstream service is unavailable",
                    error_code="UPSTREAM_UNAVAILABLE",
                    status_code=503,
                    details={"service_url": self.base_url},
                ) from error
