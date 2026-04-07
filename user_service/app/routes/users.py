from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from shared.schemas.base import SuccessResponse
from user_service.app.core.dependencies import get_session
from user_service.app.repositories.user_repository import UserRepository
from user_service.app.schemas.user import UserCreateRequest, UserResponse, UserUpdateRequest
from user_service.app.services.user_service import UserService


router = APIRouter(prefix="/users", tags=["users"])


def build_service(session: Session) -> UserService:
    return UserService(UserRepository(session))


@router.post("", response_model=SuccessResponse, status_code=status.HTTP_201_CREATED)
def create_user(payload: UserCreateRequest, session: Session = Depends(get_session)) -> SuccessResponse:
    user = build_service(session).create_user(payload)
    return SuccessResponse(message="User created", data=UserResponse.model_validate(user))


@router.get("", response_model=SuccessResponse)
def list_users(session: Session = Depends(get_session)) -> SuccessResponse:
    users = build_service(session).list_users()
    return SuccessResponse(message="Users retrieved", data=[UserResponse.model_validate(item) for item in users])


@router.get("/{user_id}", response_model=SuccessResponse)
def get_user(user_id: str, session: Session = Depends(get_session)) -> SuccessResponse:
    user = build_service(session).get_user(user_id)
    return SuccessResponse(message="User retrieved", data=UserResponse.model_validate(user))


@router.put("/{user_id}", response_model=SuccessResponse)
def update_user(user_id: str, payload: UserUpdateRequest, session: Session = Depends(get_session)) -> SuccessResponse:
    user = build_service(session).update_user(user_id, payload)
    return SuccessResponse(message="User updated", data=UserResponse.model_validate(user))


@router.delete("/{user_id}", response_model=SuccessResponse)
def delete_user(user_id: str, session: Session = Depends(get_session)) -> SuccessResponse:
    build_service(session).delete_user(user_id)
    return SuccessResponse(message="User deleted", data={})


@router.patch("/{user_id}/block", response_model=SuccessResponse)
def block_user(user_id: str, session: Session = Depends(get_session)) -> SuccessResponse:
    user = build_service(session).block_user(user_id)
    return SuccessResponse(message="User blocked", data=UserResponse.model_validate(user))


@router.patch("/{user_id}/unblock", response_model=SuccessResponse)
def unblock_user(user_id: str, session: Session = Depends(get_session)) -> SuccessResponse:
    user = build_service(session).unblock_user(user_id)
    return SuccessResponse(message="User unblocked", data=UserResponse.model_validate(user))
