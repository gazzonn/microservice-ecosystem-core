import pytest
from fastapi import Request

from api_gateway.app.services.gateway_service import GatewayService
from shared.exceptions.api import ForbiddenException, UnauthorizedException


class DummyClient:
    def __init__(self, get_response=None, post_response=None) -> None:
        self.get_response = get_response
        self.post_response = post_response

    async def get(self, path: str, params=None):
        _ = path, params
        return self.get_response

    async def post(self, path: str, json):
        _ = path, json
        return self.post_response


@pytest.fixture
def request_without_auth() -> Request:
    scope = {
        "type": "http",
        "method": "GET",
        "path": "/gateway/demo/private",
        "headers": [],
        "query_string": b"",
        "client": ("127.0.0.1", 12345),
    }
    return Request(scope)


@pytest.mark.asyncio
async def test_authenticate_request_raises_when_bearer_token_is_missing(request_without_auth: Request) -> None:
    gateway = GatewayService()

    with pytest.raises(UnauthorizedException):
        await gateway.authenticate_request(request_without_auth, {"is_protected": True})


@pytest.mark.asyncio
async def test_authorize_request_raises_when_permission_check_denies_access() -> None:
    gateway = GatewayService()
    gateway.authorization_client = DummyClient(post_response={"data": {"allowed": False, "roles": [], "permissions": []}})

    with pytest.raises(ForbiddenException):
        await gateway.authorize_request("user-1", {"is_protected": True, "required_permission": "demo:read_admin"})


@pytest.mark.asyncio
async def test_authorize_request_skips_permission_check_for_unprotected_route() -> None:
    gateway = GatewayService()

    result = await gateway.authorize_request(None, {"is_protected": False, "required_permission": None})

    assert result["allowed"] is True
