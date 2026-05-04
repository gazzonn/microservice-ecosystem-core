from datetime import datetime, timedelta, timezone
from uuid import uuid4

import pytest

from auth_service.app.models.token import Token
from auth_service.app.models.user import User
from auth_service.app.schemas.auth import RefreshTokenRequest, UserLoginRequest, UserRegisterRequest
from auth_service.app.services.auth_service import AuthService
from shared.exceptions.api import ConflictException, UnauthorizedException
from shared.utils.enums import TokenType, UserStatus


class FakeUserRepository:
    def __init__(self) -> None:
        self.users_by_id: dict[str, User] = {}
        self.users_by_username: dict[str, User] = {}
        self.users_by_email: dict[str, User] = {}

    def get_by_username(self, username: str) -> User | None:
        return self.users_by_username.get(username)

    def get_by_email(self, email: str) -> User | None:
        return self.users_by_email.get(email)

    def get_by_username_or_email(self, identity: str) -> User | None:
        return self.users_by_username.get(identity) or self.users_by_email.get(identity)

    def get_by_id(self, user_id: str) -> User | None:
        return self.users_by_id.get(user_id)

    def create(self, user: User) -> User:
        if not user.id:
            user.id = str(uuid4())
        self.users_by_id[user.id] = user
        self.users_by_username[user.username] = user
        self.users_by_email[user.email] = user
        return user

    def save(self, user: User) -> User:
        if not user.id:
            user.id = str(uuid4())
        self.users_by_id[user.id] = user
        self.users_by_username[user.username] = user
        self.users_by_email[user.email] = user
        return user


class FakeTokenRepository:
    def __init__(self) -> None:
        self.tokens: dict[str, Token] = {}

    def create(self, token: Token) -> Token:
        self.tokens[token.token_value] = token
        return token

    def get_by_value(self, token_value: str) -> Token | None:
        return self.tokens.get(token_value)

    def revoke(self, token: Token) -> Token:
        token.revoke()
        self.tokens[token.token_value] = token
        return token


@pytest.fixture
def auth_service() -> AuthService:
    return AuthService(FakeUserRepository(), FakeTokenRepository())


@pytest.fixture
def active_user(auth_service: AuthService) -> User:
    user = User(
        id=str(uuid4()),
        username="demo_user",
        email="demo@example.com",
        password_hash="",
        status=UserStatus.ACTIVE.value,
    )
    user.set_password("StrongPass123!")
    return auth_service.user_repository.create(user)


def test_register_user_success(auth_service: AuthService) -> None:
    payload = UserRegisterRequest(username="new_user", email="new@example.com", password="StrongPass123!")

    user = auth_service.register_user(payload)

    assert user.username == "new_user"
    assert user.email == "new@example.com"
    assert user.password_hash != "StrongPass123!"


def test_register_user_duplicate_username_raises_conflict(auth_service: AuthService, active_user: User) -> None:
    payload = UserRegisterRequest(username=active_user.username, email="other@example.com", password="StrongPass123!")

    with pytest.raises(ConflictException):
        auth_service.register_user(payload)


def test_authenticate_with_invalid_password_raises_unauthorized(auth_service: AuthService, active_user: User) -> None:
    payload = UserLoginRequest(username=active_user.username, password="WrongPassword")

    with pytest.raises(UnauthorizedException):
        auth_service.authenticate(payload)


def test_refresh_access_token_returns_new_access_token(auth_service: AuthService, active_user: User) -> None:
    refresh_token, expires_at = auth_service.create_refresh_token(active_user)
    payload = RefreshTokenRequest(refresh_token=refresh_token)

    response = auth_service.refresh_access_token(payload)

    assert response.user_id == active_user.id
    assert response.refresh_token == refresh_token
    assert response.expires_at == expires_at
    assert isinstance(response.access_token, str)
    assert response.access_token


def test_revoke_token_marks_token_as_revoked(auth_service: AuthService, active_user: User) -> None:
    refresh_token, expires_at = auth_service.create_refresh_token(active_user)
    _ = expires_at

    auth_service.revoke_token(refresh_token)

    stored = auth_service.token_repository.get_by_value(refresh_token)
    assert stored is not None
    assert stored.revoked is True


def test_refresh_with_revoked_token_raises_unauthorized(auth_service: AuthService, active_user: User) -> None:
    refresh_token = "revoked-token"
    token = Token(
        user_id=active_user.id,
        token_value=refresh_token,
        token_type=TokenType.REFRESH.value,
        expires_at=datetime.now(timezone.utc) + timedelta(days=1),
        revoked=True,
    )
    auth_service.token_repository.create(token)

    with pytest.raises(UnauthorizedException):
        auth_service.refresh_access_token(RefreshTokenRequest(refresh_token=refresh_token))
