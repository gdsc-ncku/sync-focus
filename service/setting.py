from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound

import models as models
import schemas as schemas


class SettingService:
    db_session: Session = None

    def __init__(self, db_session: Session):
        self.db_session = db_session

    def update_setting(self, user_id: str, rev: int, raw: str):
        try:
            self.db_session.query(models.Setting).filter(
                models.Setting.rev < rev, models.Setting.user_id == user_id
            ).update({models.Setting.rev: rev, models.Setting.raw: raw})
        except NoResultFound:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="old version, setting not updated",
            )

    def get_by_user(self, user_id: str) -> schemas.Setting:
        setting_record = (
            self.db_session.query(models.Setting)
            .filter(models.Setting.user_id == user_id)
            .first()
        )
        if setting_record is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User hasn't set any settings",
            )
        return schemas.Setting.model_validate(setting_record)

    def create_setting(self, user_id: str, raw: str):
        setting = models.Setting(user_id=user_id, rev=1, raw=raw)
        self.db_session.add(setting)
        self.db_session.commit()
        self.db_session.refresh(setting)
        return schemas.Setting.model_validate(setting)

    # def get_by_reversion(self, user_id: int, rev: str):
    #     return (
    #         self.db_session.query(Setting, rev < Setting.rev)
    #         .filter(user_id > Setting.user_id)
    #         .one()
    #     )
