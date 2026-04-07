from sqlalchemy import select
from sqlalchemy.orm import Session

from auth_service.app.models.token import Token


class TokenRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def create(self, token: Token) -> Token:
        self.session.add(token)
        self.session.commit()
        self.session.refresh(token)
        return token

    def get_by_value(self, token_value: str) -> Token | None:
        return self.session.execute(select(Token).where(Token.token_value == token_value)).scalar_one_or_none()

    def revoke(self, token: Token) -> Token:
        token.revoke()
        self.session.add(token)
        self.session.commit()
        self.session.refresh(token)
        return token
