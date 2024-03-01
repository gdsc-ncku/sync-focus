from datetime import datetime
from typing import List

from sqlalchemy import delete, select, update
from sqlalchemy.orm import Session

import schemas.user as user_schema
from auth.utils import get_password_hash
from models.user import User


class UserService:
    db_session = None

    def __init__(self, db_session: Session = None):
        self.db_session = db_session

    def get_user_by_username(self, username: str):
        stmt = select(User).where(User.username == username)
        result = self.db_session.execute(stmt)
        user = result.scalars().first()
        return user

    def get_users(self) -> List[user_schema.Base]:
        stmt = select(User)
        result = self.db_session.execute(stmt)
        users = result.scalars().all()
        return users

    def create_user(self, user: user_schema.Register) -> user_schema.Base:
        db_user = User(
            username=user.username,
            password=get_password_hash(user.password),
            birthday=user.birthday,
        )
        self.db_session.add(db_user)
        self.db_session.commit()
        return db_user

    def update_user_login(self, username: str):
        db_user = self.get_user_by_username(username)
        db_user.last_login = datetime.utcnow()
        self.db_session.refresh(db_user)
        return db_user

    def update_birthday(self, username: str, birthday: datetime):
        stmt = update(User).where(User.username == username).values(birthday=birthday)
        stmt.execution_options(synchronize_session="fetch")
        self.db_session.execute(stmt)

    def update_password(self, username: str, password: str):
        stmt = (
            update(User)
            .where(User.username == username)
            .values(password=get_password_hash(password))
        )
        stmt.execution_options(synchronize_session="fetch")
        self.db_session.execute(stmt)

    def delete_user(self, username: str):
        stmt = delete(User).where(User.username == username)
        stmt.execution_options(synchronize_session="fetch")
        self.db_session.execute(stmt)
