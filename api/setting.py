from fastapi import APIRouter, Depends, Query

from schemas.setting import CreateSettingRequest, Setting, UpdateSettingRequest
from service.setting import SettingService

# from auth.action import get_current_user
from .services import get_setting_service

router = APIRouter(prefix="/settings", tags=["users"])


@router.post("/update")
def update_setting(
    new_setting: UpdateSettingRequest,
    setting_service: SettingService = Depends(get_setting_service),
    user_id: str = Query(...),
):
    return setting_service.update_setting(user_id, new_setting.rev, new_setting.raw)


@router.post("/create")
def create_setting(
    setting: CreateSettingRequest,
    setting_service: SettingService = Depends(get_setting_service),
    user_id: str = Query(...),
):
    return setting_service.create_setting(user_id, setting.raw)


@router.get("", response_model=Setting)
def get_setting(
    setting_service: SettingService = Depends(get_setting_service),
    user_id: str = Query(...),
):
    return setting_service.get_by_user(user_id)
