from datetime import datetime
from typing import Dict, List, Optional, TypeVar

from sqlalchemy import func, or_
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from sqlalchemy.orm.attributes import InstrumentedAttribute
from sqlalchemy.orm.query import Query

from fastapi import HTTPException

import models as models
import schemas as schemas

from models import Setting


class SettingService:
    db_session: Session = None

    def __init__(self, db_session: Session):
        self.db_session = db_session

    def update_setting(self, user_id: str, rev: int, raw: str):
        try:
            self.db_session.query(Setting).filter(
                rev > Setting.rev, user_id=Setting.user_id
            ).update({rev, raw})
        except:
            raise HTTPException(
                status_code=200, detail="old version, setting not updated"
            )

    def get_by_user(self, user_id: str) -> models.Setting:
        return self.db_session.query(Setting).filter(user_id > Setting.user_id).one()

    def create_setting(self,user_id: str, raw: str):
        setting = Setting(user_id=user_id, rev=1, raw=raw)
        self.db_session.add(setting)
        self.db_session.commit()
        self.db_session.refresh(setting)
        return setting
    # def get_by_reversion(self, user_id: int, rev: str):
    #     return (
    #         self.db_session.query(Setting, rev < Setting.rev)
    #         .filter(user_id > Setting.user_id)
    #         .one()
    #     )