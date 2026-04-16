from typing import Any

import httpx

from shared.config.settings import get_settings
from shared.exceptions.api import AppException


class DemoConsoleService:
    """Proxy service for the demo UI."""

    def __init__(self) -> None:
        self.settings = get_settings()

    async def _request(
        self,
        method: str,
        base_url: str,
        path: str,
        *,
        json: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        async with httpx.AsyncClient(timeout=20.0) as client:
            try:
                response = await client.request(
                    method,
                    f"{base_url.rstrip('/')}{path}",
                    json=json,
                    headers=headers,
                )
                payload = self._parse_payload(response)
                return {"status_code": response.status_code, "payload": payload}
            except httpx.HTTPError as error:
                raise AppException(
                    message="Dependent service is unavailable",
                    error_code="DEMO_UI_UPSTREAM",
                    status_code=503,
                    details={"service": base_url, "reason": str(error)},
                ) from error

    @staticmethod
    def _parse_payload(response: httpx.Response) -> Any:
        try:
            return response.json()
        except ValueError:
            return {"raw": response.text}

    async def register_user(self, payload: dict[str, Any]) -> dict[str, Any]:
        return await self._request("POST", self.settings.auth_service_url, "/auth/register", json=payload)

    async def login_user(self, payload: dict[str, Any]) -> dict[str, Any]:
        return await self._request("POST", self.settings.auth_service_url, "/auth/login", json=payload)

    async def create_role(self, payload: dict[str, Any]) -> dict[str, Any]:
        return await self._request("POST", self.settings.authorization_service_url, "/authorize/roles", json=payload)

    async def create_permission(self, payload: dict[str, Any]) -> dict[str, Any]:
        return await self._request("POST", self.settings.authorization_service_url, "/authorize/permissions", json=payload)

    async def assign_role(self, payload: dict[str, Any]) -> dict[str, Any]:
        return await self._request("POST", self.settings.authorization_service_url, "/authorize/assign-role", json=payload)

    async def assign_permission(self, payload: dict[str, Any]) -> dict[str, Any]:
        return await self._request("POST", self.settings.authorization_service_url, "/authorize/assign-permission", json=payload)

    async def register_demo_service(self) -> dict[str, Any]:
        payload = {
            "name": "demo_microservice",
            "base_url": self.settings.demo_service_url,
            "health_url": f"{self.settings.demo_service_url}/health",
            "status": "ACTIVE",
            "version": "1.0.0",
            "routes": [
                {
                    "path": "/demo/public",
                    "method": "GET",
                    "is_protected": False,
                    "required_permission": None,
                },
                {
                    "path": "/demo/private",
                    "method": "GET",
                    "is_protected": True,
                    "required_permission": None,
                },
                {
                    "path": "/demo/admin",
                    "method": "GET",
                    "is_protected": True,
                    "required_permission": "demo:read_admin",
                },
            ],
        }
        return await self._request("POST", self.settings.service_registry_url, "/services/register", json=payload)

    async def call_gateway(self, path: str, token: str | None = None) -> dict[str, Any]:
        normalized_path = path if path.startswith("/") else f"/{path}"
        headers = {"Authorization": f"Bearer {token}"} if token else None
        return await self._request("GET", self.settings.api_gateway_url, f"/gateway{normalized_path}", headers=headers)
