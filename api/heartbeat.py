from typing import List

from fastapi import APIRouter, Body, Depends, Query

from api.services import get_heartbeat_service
from schemas.heartbeat import Heartbeat, HeartbeatCreateRequest
from service.heartbeat import HeartbeatService

router = APIRouter(prefix="/heartbeat", tags=["heartbeat"])


@router.post(
    "/",
    description="Receive a heartbeat from the client(browser extension)",
)
def heartbeat(
    heartbeat: HeartbeatCreateRequest = Body(..., description="The heartbeat"),
    api_key: str = Query(None, description="API key"),
    heartbeat_service: HeartbeatService = Depends(get_heartbeat_service),
):
    heartbeat_obj = Heartbeat.from_request(heartbeat)
    heartbeat_obj.user_id = api_key  # TODO: implement user authentication to get real user id through api_key, this is for testing
    return heartbeat_service.insert(heartbeat_obj)


@router.post(
    "/batch",
    description="Receive a batch of heartbeats from the client(browser extension)",
)
def heartbeat_batch(
    heartbeats: List[HeartbeatCreateRequest] = Body(..., description="The heartbeats"),
    api_key: str = Query(None, description="API key"),
    heartbeat_service: HeartbeatService = Depends(get_heartbeat_service),
):
    heartbeat_objs = [Heartbeat.from_request(heartbeat) for heartbeat in heartbeats]
    for heartbeat_obj in heartbeat_objs:
        heartbeat_obj.user_id = api_key  # TODO: implement user authentication to get real user id through api_key, this is for testing
    return heartbeat_service.insert_batch(heartbeat_objs)
