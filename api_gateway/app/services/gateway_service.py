from typing import Any

import httpx
from fastapi import Request

from api_gateway.app.core.config import settings
from api_gateway.app.services.http_clients import ServiceClient
from shared.exceptions.api import ForbiddenException, NotFoundException, UnauthorizedException


class GatewayService:
    """Gateway orchestration between auth, authorization and registry."""

    def __init__(self) -> None:
        self.auth_client = ServiceClient(settings.auth_service_url)
        self.authorization_client = ServiceClient(settings.authorization_service_url)
        self.registry_client = ServiceClient(settings.service_registry_url)

    async def authenticate_request(self, request: Request, route_data: dict[str, Any]) -> dict[str, Any]:
        if not route_data["is_protected"]:
            return {"user_id": None, "roles": [], "permissions": []}

        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            raise UnauthorizedException("Missing bearer token")
        token = auth_header.removeprefix("Bearer ").strip()
        validation_response = await self.auth_client.post("/auth/validate", {"token": token})
        return validation_response["data"]

    async def authorize_request(self, user_id: str | None, route_data: dict[str, Any]) -> dict[str, Any]:
        if not route_data["is_protected"]:
            return {"allowed": True, "roles": [], "permissions": []}
        permission = route_data.get("required_permission")
        if not permission:
            return {"allowed": True, "roles": [], "permissions": []}
        resource, action = permission.split(":", maxsplit=1)
        result = await self.authorization_client.post(
            "/authorize/check", {"user_id": user_id, "resource": resource, "action": action}
        )
        if not result["data"]["allowed"]:
            raise ForbiddenException("Access denied for requested resource")
        return result["data"]

    async def resolve_route(self, path: str, method: str) -> dict[str, Any]:
        response = await self.registry_client.get("/services/resolve/route", params={"path": path, "method": method})
        data = response["data"]
        if data["status"] != "ACTIVE":
            raise NotFoundException("Target service is not available")
        return data

    async def forward_request(
        self,
        target_base_url: str,
        path: str,
        request: Request,
        user_context: dict[str, Any],
        authz_context: dict[str, Any],
    ) -> httpx.Response:
        headers = {
            key: value
            for key, value in request.headers.items()
            if key.lower() not in {"host", "content-length"}
        }
        if user_context.get("user_id"):
            headers["x-user-id"] = user_context["user_id"]
        if authz_context.get("roles"):
            headers["x-user-roles"] = ",".join(authz_context["roles"])
        body = await request.body()
        async with httpx.AsyncClient(timeout=20.0) as client:
            return await client.request(
                request.method,
                f"{target_base_url}{path}",
                headers=headers,
                params=request.query_params,
                content=body,
            )
