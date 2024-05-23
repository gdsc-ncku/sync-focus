from fastapi import APIRouter, Depends, status

from api.security import required_login
from schemas import DetailSchema
from schemas.setting import CreateSettingRequest, Setting, UpdateSettingRequest
from service.setting import SettingService

# from auth.action import get_current_user
from .services import get_setting_service

router = APIRouter(prefix="/settings", tags=["settings"])


@router.post(
    "/update",
    responses={
        status.HTTP_200_OK: {"model": None},
        status.HTTP_401_UNAUTHORIZED: {"model": DetailSchema},
        status.HTTP_404_NOT_FOUND: {"model": DetailSchema},
    },
)
def update_setting(
    new_setting: UpdateSettingRequest,
    setting_service: SettingService = Depends(get_setting_service),
    auth_user_id: str = Depends(required_login),
):
    return setting_service.update_setting(
        auth_user_id, new_setting.rev, new_setting.raw
    )


@router.post(
    "/create",
    responses={
        status.HTTP_201_CREATED: {"model": Setting},
        status.HTTP_401_UNAUTHORIZED: {"model": DetailSchema},
        status.HTTP_404_NOT_FOUND: {"model": DetailSchema},
    },
)
def create_setting(
    setting: CreateSettingRequest,
    setting_service: SettingService = Depends(get_setting_service),
    auth_user_id: str = Depends(required_login),
):
    return setting_service.create_setting(auth_user_id, setting.raw)


@router.get(
    "",
    responses={
        status.HTTP_200_OK: {"model": Setting},
        status.HTTP_401_UNAUTHORIZED: {"model": DetailSchema},
        status.HTTP_404_NOT_FOUND: {"model": DetailSchema},
    },
)
def get_setting(
    setting_service: SettingService = Depends(get_setting_service),
    auth_user_id: str = Depends(required_login),
):
    return setting_service.get_by_user(auth_user_id)
