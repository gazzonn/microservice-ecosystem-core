from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from auth_service.app.models.user import User


class UserRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def get_by_username(self, username: str) -> User | None:
        return self.session.execute(select(User).where(User.username == username)).scalar_one_or_none()

    def get_by_email(self, email: str) -> User | None:
        return self.session.execute(select(User).where(User.email == email)).scalar_one_or_none()

    def get_by_username_or_email(self, identity: str) -> User | None:
        return self.session.execute(
            select(User).where(or_(User.username == identity, User.email == identity))
        ).scalar_one_or_none()

    def get_by_id(self, user_id: str) -> User | None:
        return self.session.get(User, user_id)

    def create(self, user: User) -> User:
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user

    def save(self, user: User) -> User:
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user
