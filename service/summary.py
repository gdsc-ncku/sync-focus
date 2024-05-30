from sqlalchemy import distinct, func
from sqlalchemy.orm import Session

import models as models
import schemas as schemas
from models import Summary, SummaryItem


class SummaryService:
    db_session: Session = None

    def __init__(self, db_session: Session):
        self.db_session = db_session

    def list_domain(self, user_id: str, offset: int, limit: int) -> list[str]:
        query = (
            self.db_session.query(distinct(SummaryItem.key))
            .join(Summary, Summary.id == SummaryItem.summary_id)
            .filter(Summary.user_id == user_id, SummaryItem.type == 0)
            .order_by(Summary.time.desc())
            .offset(offset)
            .limit(limit)
        )

        list = [row.domain for row in query.all()]
        return list

    def get_path(self, user_id: str, domain: str) -> list[dict]:
        # duplicated code
        summary_subquery = (
            self.db_session.query(Summary.id, Summary.user_id)
            .filter(Summary.user_id == user_id)
            .join(SummaryItem, Summary.id == SummaryItem.summary_id)
            .filter(SummaryItem.key == domain, SummaryItem.type == 0)
        )
        items = self.db_session.query(SummaryItem, func.count(SummaryItem.key)).filter(
            SummaryItem.type == 1, SummaryItem.id.in_(summary_subquery)
        )
        result = {}
        for x in items:
            result[x[0]] = x[1]

        return result

    def get_agent(self, user_id: str, domain: str) -> list[dict]:
        # duplicated code
        summary_subquery = (
            self.db_session.query(Summary.id, Summary.user_id)
            .filter(Summary.user_id == user_id)
            .join(SummaryItem, Summary.id == SummaryItem.summary_id)
            .filter(SummaryItem.key == domain, SummaryItem.type == 0)
        )
        items = self.db_session.query(SummaryItem, func.count(SummaryItem.key)).filter(
            SummaryItem.type == 2, SummaryItem.id.in_(summary_subquery)
        )
        result = {}
        for x in items:
            result[x[0]] = x[1]

        return result
