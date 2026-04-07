from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

from api_gateway.app.services.gateway_service import GatewayService
from shared.schemas.base import SuccessResponse


router = APIRouter(tags=["gateway"])


@router.get("/routes", response_model=SuccessResponse)
async def routes() -> SuccessResponse:
    return SuccessResponse(message="Gateway route endpoint is available", data={"entrypoint": "/gateway/{path:path}"})


@router.api_route("/gateway/{path:path}", methods=["GET", "POST", "PUT", "PATCH", "DELETE"])
async def gateway_proxy(path: str, request: Request) -> JSONResponse:
    gateway = GatewayService()
    resolved_path = f"/{path}"
    route_data = await gateway.resolve_route(path=resolved_path, method=request.method)
    user_context = await gateway.authenticate_request(request=request, route_data=route_data)
    authz_context = await gateway.authorize_request(user_id=user_context.get("user_id"), route_data=route_data)
    upstream_response = await gateway.forward_request(
        target_base_url=route_data["base_url"],
        path=resolved_path,
        request=request,
        user_context=user_context,
        authz_context=authz_context,
    )
    return JSONResponse(status_code=upstream_response.status_code, content=upstream_response.json())
