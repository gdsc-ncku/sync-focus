import hashlib
from typing import List

from sqlalchemy import delete, select, update
from sqlalchemy.orm import Session

import models
import schemas
from service.utils import get_password_hash


class UserService:
    db_session = None

    def __init__(self, db_session: Session = None):
        self.db_session = db_session

    def get_user_by_username(self, username: str):
        stmt = select(models.User).where(models.User.username == username)
        result = self.db_session.execute(stmt)
        user = result.scalars().first()
        return user

    def get_users(self) -> List[schemas.User]:
        stmt = select(models.User)
        result = self.db_session.execute(stmt)
        users = result.scalars().all()
        return [schemas.User.model_validate(user) for user in users]

    def create_user(self, user: schemas.CreateUserRequest) -> schemas.User:
        db_user = models.User(**user.model_dump())
        self.db_session.add(db_user)
        self.db_session.commit()
        return db_user

    def update_password(self, username: str, password: str):
        stmt = (
            update(models.User)
            .where(models.User.username == username)
            .values(password=get_password_hash(password))
        )
        stmt.execution_options(synchronize_session="fetch")
        self.db_session.execute(stmt)

    def delete_user(self, username: str):
        stmt = delete(models.User).where(models.User.username == username)
        stmt.execution_options(synchronize_session="fetch")
        self.db_session.execute(stmt)

    def get_password_hash(password: str):
        return hashlib.sha256(password).hexdigest()
