from shared.exceptions.api import ConflictException, NotFoundException
from shared.utils.enums import UserStatus
from user_service.app.models.user import User
from user_service.app.repositories.user_repository import UserRepository
from user_service.app.schemas.user import UserCreateRequest, UserUpdateRequest


class UserService:
    """Business logic for user management."""

    def __init__(self, repository: UserRepository) -> None:
        self.repository = repository

    def create_user(self, data: UserCreateRequest) -> User:
        if self.repository.get_by_username(data.username):
            raise ConflictException("Username already exists")
        if self.repository.get_by_email(data.email):
            raise ConflictException("Email already exists")

        user = User(username=data.username, email=data.email, password_hash="")
        user.set_password(data.password)
        return self.repository.create(user)

    def get_user(self, user_id: str) -> User:
        user = self.repository.get_by_id(user_id)
        if not user:
            raise NotFoundException("User not found")
        return user

    def update_user(self, user_id: str, data: UserUpdateRequest) -> User:
        user = self.get_user(user_id)
        if data.email:
            user.email = data.email
        if data.status:
            user.status = data.status
        return self.repository.save(user)

    def delete_user(self, user_id: str) -> None:
        user = self.get_user(user_id)
        self.repository.delete(user)

    def block_user(self, user_id: str) -> User:
        user = self.get_user(user_id)
        user.status = UserStatus.BLOCKED.value
        return self.repository.save(user)

    def unblock_user(self, user_id: str) -> User:
        user = self.get_user(user_id)
        user.status = UserStatus.ACTIVE.value
        return self.repository.save(user)

    def list_users(self) -> list[User]:
        return self.repository.list_users()
