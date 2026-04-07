from datetime import datetime, timedelta, timezone

import jwt

from auth_service.app.models.token import Token
from auth_service.app.models.user import User
from auth_service.app.repositories.token_repository import TokenRepository
from auth_service.app.repositories.user_repository import UserRepository
from auth_service.app.schemas.auth import (
    ChangePasswordRequest,
    RefreshTokenRequest,
    TokenResponse,
    TokenValidationResponse,
    UserLoginRequest,
    UserRegisterRequest,
)
from shared.config.settings import get_settings
from shared.exceptions.api import ConflictException, ForbiddenException, UnauthorizedException
from shared.security.jwt import create_token, decode_token
from shared.utils.enums import TokenType, UserStatus


class AuthService:
    """Authentication and token issuance."""

    def __init__(self, user_repository: UserRepository, token_repository: TokenRepository) -> None:
        self.user_repository = user_repository
        self.token_repository = token_repository
        self.settings = get_settings()

    def register_user(self, data: UserRegisterRequest) -> User:
        if self.user_repository.get_by_username(data.username):
            raise ConflictException("Username already exists")
        if self.user_repository.get_by_email(data.email):
            raise ConflictException("Email already exists")

        user = User(username=data.username, email=data.email, password_hash="")
        user.set_password(data.password)
        return self.user_repository.create(user)

    def authenticate(self, data: UserLoginRequest) -> TokenResponse:
        user = self.user_repository.get_by_username_or_email(data.username)
        if not user or not user.verify_password(data.password):
            raise UnauthorizedException("Invalid credentials")
        if user.status != UserStatus.ACTIVE.value:
            raise ForbiddenException("User account is not active")

        user.last_login_at = datetime.now(timezone.utc)
        self.user_repository.save(user)

        access_token = self.create_access_token(user)
        refresh_token, refresh_expires_at = self.create_refresh_token(user)
        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            user_id=user.id,
            expires_at=refresh_expires_at,
        )

    def create_access_token(self, user: User) -> str:
        return create_token(
            subject=user.id,
            token_type=TokenType.ACCESS.value,
            expires_delta=timedelta(minutes=self.settings.access_token_expire_minutes),
            extra_claims={"username": user.username, "status": user.status},
        )

    def create_refresh_token(self, user: User) -> tuple[str, datetime]:
        expires_at = datetime.now(timezone.utc) + timedelta(days=self.settings.refresh_token_expire_days)
        token_value = create_token(
            subject=user.id,
            token_type=TokenType.REFRESH.value,
            expires_delta=timedelta(days=self.settings.refresh_token_expire_days),
        )
        self.token_repository.create(
            Token(
                user_id=user.id,
                token_value=token_value,
                token_type=TokenType.REFRESH.value,
                expires_at=expires_at,
            )
        )
        return token_value, expires_at

    def refresh_access_token(self, data: RefreshTokenRequest) -> TokenResponse:
        stored_token = self.token_repository.get_by_value(data.refresh_token)
        if not stored_token or stored_token.revoked or stored_token.is_expired():
            raise UnauthorizedException("Refresh token is invalid")
        payload = decode_token(data.refresh_token)
        user = self.user_repository.get_by_id(payload["sub"])
        if not user or user.status != UserStatus.ACTIVE.value:
            raise ForbiddenException("User account is not active")

        return TokenResponse(
            access_token=self.create_access_token(user),
            refresh_token=data.refresh_token,
            user_id=user.id,
            expires_at=stored_token.expires_at,
        )

    def revoke_token(self, token_value: str) -> None:
        stored_token = self.token_repository.get_by_value(token_value)
        if not stored_token:
            raise UnauthorizedException("Refresh token not found")
        self.token_repository.revoke(stored_token)

    def validate_token(self, token: str) -> TokenValidationResponse:
        try:
            payload = decode_token(token)
        except jwt.PyJWTError as error:
            raise UnauthorizedException("Invalid token", {"reason": str(error)}) from error

        if payload.get("type") != TokenType.ACCESS.value:
            raise UnauthorizedException("Token type is not access")

        user = self.user_repository.get_by_id(payload["sub"])
        if not user or user.status != UserStatus.ACTIVE.value:
            raise ForbiddenException("User account is not active")

        return TokenValidationResponse(valid=True, user_id=user.id, username=user.username, status=user.status)

    def change_password(self, data: ChangePasswordRequest) -> None:
        user = self.user_repository.get_by_username_or_email(data.username)
        if not user or not user.verify_password(data.old_password):
            raise UnauthorizedException("Invalid credentials")
        user.set_password(data.new_password)
        self.user_repository.save(user)
