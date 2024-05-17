from typing import List

from fastapi import APIRouter, Body, Depends, HTTPException, Query, status

from api.services import get_heartbeat_service, get_user_service
from exception.exception import HTTPError
from schemas.heartbeat import Heartbeat, HeartbeatCreateRequest
from service.heartbeat import HeartbeatService
from service.user import UserService

router = APIRouter(prefix="/heartbeats", tags=["heartbeats"])


@router.post(
    "/",
    description="Receive a heartbeat from the client(browser extension)",
    responses={
        status.HTTP_201_CREATED: {"model": Heartbeat},
        status.HTTP_401_UNAUTHORIZED: {"model": HTTPError},
    },
)
def heartbeat(
    heartbeat: HeartbeatCreateRequest = Body(..., description="The heartbeat"),
    api_key: str = Query(None, description="API key"),
    heartbeat_service: HeartbeatService = Depends(get_heartbeat_service),
    user_service: UserService = Depends(get_user_service),
):
    heartbeat_obj = Heartbeat.from_request(heartbeat)
    user_id: str = None
    if api_key:
        user = user_service.get_user_by_api_key(api_key)
        if not user:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid API key")
        user_id = user.id
    else:
        user_id = "anonymous"
    heartbeat_obj.user_id = user_id
    return heartbeat_service.insert(heartbeat_obj)


@router.post(
    "/batch",
    description="Receive a batch of heartbeats from the client(browser extension)",
    responses={
        status.HTTP_201_CREATED: {"model": List[Heartbeat]},
        status.HTTP_401_UNAUTHORIZED: {"model": HTTPError},
    },
)
def heartbeat_batch(
    heartbeats: List[HeartbeatCreateRequest] = Body(..., description="The heartbeats"),
    api_key: str = Query(None, description="API key"),
    heartbeat_service: HeartbeatService = Depends(get_heartbeat_service),
    user_service: UserService = Depends(get_user_service),
) -> List[Heartbeat]:
    heartbeat_objs = [Heartbeat.from_request(heartbeat) for heartbeat in heartbeats]
    user_id: str = None
    if api_key:
        user = user_service.get_user_by_api_key(api_key)
        if not user:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid API key")
        user_id = user.id
    else:
        user_id = "anonymous"
    for heartbeat_obj in heartbeat_objs:
        heartbeat_obj.user_id = user_id
    return heartbeat_service.insert_batch(heartbeat_objs)
