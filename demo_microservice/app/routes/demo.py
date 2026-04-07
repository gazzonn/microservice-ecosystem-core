from fastapi import APIRouter, Header, HTTPException

from shared.schemas.base import SuccessResponse


router = APIRouter(prefix="/demo", tags=["demo"])


@router.get("/public", response_model=SuccessResponse)
def public_endpoint() -> SuccessResponse:
    return SuccessResponse(message="Public endpoint available", data={"scope": "public"})


@router.get("/private", response_model=SuccessResponse)
def private_endpoint(x_user_id: str | None = Header(default=None)) -> SuccessResponse:
    if not x_user_id:
        raise HTTPException(status_code=401, detail="Missing user context")
    return SuccessResponse(message="Private endpoint available", data={"scope": "private", "user_id": x_user_id})


@router.get("/admin", response_model=SuccessResponse)
def admin_endpoint(
    x_user_id: str | None = Header(default=None),
    x_user_roles: str | None = Header(default=None),
) -> SuccessResponse:
    if not x_user_id:
        raise HTTPException(status_code=401, detail="Missing user context")
    roles = [item.strip().upper() for item in (x_user_roles or "").split(",") if item.strip()]
    if "ADMIN" not in roles:
        raise HTTPException(status_code=403, detail="Admin role required")
    return SuccessResponse(message="Admin endpoint available", data={"scope": "admin", "user_id": x_user_id})
