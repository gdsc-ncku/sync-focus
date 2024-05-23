from fastapi import APIRouter, Depends, Query

from api.services import get_summary_service
from schemas.summary import ListAgentRequest, ListDomainRequest, ListPathRequest
from service.summary import SummaryService
from service.user import UserService

router = APIRouter(prefix="/settings", tags=["users"])


@router.post("/domain")
def list_domain(
    request: ListDomainRequest,
    summary_service: SummaryService = Depends(get_summary_service),
    user_id: str = Query(...),
):
    return summary_service.list_domain(user_id, request.offset, request.limit)


@router.post("/path")
def get_path_usage(
    request: ListPathRequest,
    summary_service: SummaryService = Depends(get_summary_service),
    user_id: str = Query(...),
):
    return summary_service.get_path(user_id, request.domain)


@router.post("/agent")
def get_agent_usage(
    request: ListAgentRequest,
    summary_service: SummaryService = Depends(get_summary_service),
    user_id: str = Query(...),
):
    return summary_service.get_agent(user_id, request.domain)
