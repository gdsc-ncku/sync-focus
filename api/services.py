from fastapi import Depends
from sqlalchemy.orm import Session

from bootstrap.deps import deps
from bootstrap.setting import setting
from service.duration import DurationService
from service.heartbeat import HeartbeatService
from service.setting import SettingService
from service.summary import SummaryService
from service.user import UserService


def get_heartbeat_service(db: Session = Depends(deps.get_db)) -> HeartbeatService:
    return HeartbeatService(db)


def get_duration_service(db: Session = Depends(deps.get_db)) -> DurationService:
    return DurationService(db)


def get_user_service(db: Session = Depends(deps.get_db)) -> UserService:
    return UserService(db, setting=setting)


def get_setting_service(db: Session = Depends(deps.get_db)) -> SettingService:
    return SettingService(db)


def get_summary_service(db: Session = Depends(deps.get_db)) -> SummaryService:
    return SummaryService(db)

