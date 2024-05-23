import hashlib
import json
from datetime import datetime, timedelta
from typing import List
from uuid import UUID

from fastapi import HTTPException, status
from jose import jwt
from sqlalchemy import delete, select, update
from sqlalchemy.orm import Session

import models
import schemas
from bootstrap.setting import Settings
from service.utils import get_password_hash


class UUIDEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, UUID):
            # if the obj is uuid, we simply return the value of uuid
            return obj.hex
        return json.JSONEncoder.default(self, obj)


class UserService:
    db_session = None

    def __init__(self, db_session: Session, setting: Settings):
        self.db_session = db_session
        self.setting = setting

    def get_user_by_username(self, username: str):
        stmt = select(models.User).where(models.User.username == username)
        result = self.db_session.execute(stmt)
        user = result.scalars().first()
        return user

    def get_user_by_id(self, user_id: str):
        stmt = select(models.User).where(models.User.id == user_id)
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

    def get_user_by_api_key(self, api_key: str):
        stmt = select(models.User).where(models.User.api_key == api_key)
        result = self.db_session.execute(stmt)
        user = result.scalars().first()
        return user

    def get_user_api_key(self, user_id: str):
        stmt = select(models.User.api_key).where(models.User.id == user_id)
        result = self.db_session.execute(stmt)
        api_key = result.scalars().first()
        if api_key is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="API key not found",
            )
        return schemas.UserAPIKey(api_key=api_key)

    def create_access_token(self, data: dict):
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(
            minutes=self.setting.access_token.expire_minutes
        )

        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            claims=to_encode,
            key=self.setting.access_token.secret,
            algorithm="HS256",
        )
        return encoded_jwt

    def create_refresh_token(self, data: dict):
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(
            minutes=self.setting.refresh_token.expire_minutes
        )

        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            to_encode,
            self.setting.refresh_token.secret,
            algorithm="HS256",
        )
        return encoded_jwt
