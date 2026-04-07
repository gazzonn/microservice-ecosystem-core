from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from auth_service.app.core.dependencies import get_session
from auth_service.app.repositories.token_repository import TokenRepository
from auth_service.app.repositories.user_repository import UserRepository
from auth_service.app.schemas.auth import (
    ChangePasswordRequest,
    LogoutRequest,
    RefreshTokenRequest,
    TokenValidationRequest,
    UserLoginRequest,
    UserRegisterRequest,
)
from auth_service.app.services.auth_service import AuthService
from shared.schemas.base import SuccessResponse


router = APIRouter(prefix="/auth", tags=["auth"])


def build_service(session: Session) -> AuthService:
    return AuthService(UserRepository(session), TokenRepository(session))


@router.post("/register", response_model=SuccessResponse, status_code=status.HTTP_201_CREATED)
def register(payload: UserRegisterRequest, session: Session = Depends(get_session)) -> SuccessResponse:
    user = build_service(session).register_user(payload)
    return SuccessResponse(message="User registered", data={"user_id": user.id, "username": user.username})


@router.post("/login", response_model=SuccessResponse)
def login(payload: UserLoginRequest, session: Session = Depends(get_session)) -> SuccessResponse:
    token_response = build_service(session).authenticate(payload)
    return SuccessResponse(message="Login successful", data=token_response.model_dump(mode="json"))


@router.post("/refresh", response_model=SuccessResponse)
def refresh(payload: RefreshTokenRequest, session: Session = Depends(get_session)) -> SuccessResponse:
    token_response = build_service(session).refresh_access_token(payload)
    return SuccessResponse(message="Token refreshed", data=token_response.model_dump(mode="json"))


@router.post("/logout", response_model=SuccessResponse)
def logout(payload: LogoutRequest, session: Session = Depends(get_session)) -> SuccessResponse:
    build_service(session).revoke_token(payload.refresh_token)
    return SuccessResponse(message="Token revoked", data={})


@router.post("/validate", response_model=SuccessResponse)
def validate(payload: TokenValidationRequest, session: Session = Depends(get_session)) -> SuccessResponse:
    validation = build_service(session).validate_token(payload.token)
    return SuccessResponse(message="Token validated", data=validation.model_dump())


@router.post("/change-password", response_model=SuccessResponse)
def change_password(payload: ChangePasswordRequest, session: Session = Depends(get_session)) -> SuccessResponse:
    build_service(session).change_password(payload)
    return SuccessResponse(message="Password changed", data={})
