from datetime import datetime
from typing import Dict, List, Optional, TypeVar

from sqlalchemy import func, or_
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, aliased
from sqlalchemy.orm.attributes import InstrumentedAttribute
from sqlalchemy.orm.query import Query

import models as models

T = TypeVar("T")


class HeartbeatService:
    db_session: Session = None

    def __init__(self, db_session: Session):
        self.db_session = db_session

    def get_all(self) -> List[models.Heartbeat]:
        return self.db_session.query(models.Heartbeat).all()

    def insert_batch(self, heartbeats: List[models.Heartbeat]):
        for heartbeat in heartbeats:
            try:
                self.db_session.add(heartbeat)
                self.db_session.commit()
            except Exception as e:
                self.db_session.rollback()
                if not isinstance(e, IntegrityError):
                    raise

    def get_latest_by_user(self, user_id: str) -> Optional[models.Heartbeat]:
        return (
            self.db_session.query(models.Heartbeat)
            .filter_by(user_id=user_id)
            .order_by(models.Heartbeat.time.desc())
            .first()
        )

    def get_latest_by_origin_and_user(
        self, origin: str, user_id: str
    ) -> Optional[models.Heartbeat]:
        return (
            self.db_session.query(models.Heartbeat)
            .filter_by(user_id=user_id, origin=origin)
            .order_by(models.Heartbeat.time.desc())
            .first()
        )

    def get_all_within(
        self, from_time: datetime, to_time: datetime, user_id: str
    ) -> List[models.Heartbeat]:
        return (
            self.db_session.query(models.Heartbeat)
            .filter(
                models.Heartbeat.user_id == user_id,
                models.Heartbeat.time >= from_time,
                models.Heartbeat.time < to_time,
            )
            .order_by(models.Heartbeat.time.asc())
            .all()
        )

    def get_all_within_by_filters(
        self,
        from_time: datetime,
        to_time: datetime,
        user_id: str,
        filter_map: Dict[str, List[str]] = {},
    ) -> List[models.Heartbeat]:
        query = self.db_session.query(models.Heartbeat).filter(
            models.Heartbeat.user_id == user_id,
            models.Heartbeat.time >= from_time,
            models.Heartbeat.time < to_time,
        )
        query = self.filtered_query(query, filter_map)
        return query.order_by(models.Heartbeat.time.asc()).all()

    def get_latest_by_filters(
        self, user_id: str, filter_map: Dict[str, List[str]]
    ) -> Optional[models.Heartbeat]:
        query = self.db_session.query(models.Heartbeat).filter_by(user_id=user_id)
        query = self.filtered_query(query, filter_map)
        return query.order_by(models.Heartbeat.time.desc()).first()

    def get_first_by_users(self) -> List[models.TimeByUser]:
        subquery = (
            self.db_session.query(
                models.Heartbeat.user_id.label("user"),
                func.min(models.Heartbeat.time).label("time"),
            )
            .group_by(models.Heartbeat.user_id)
            .subquery()
        )
        # Creating an aliased object to use in the outer query
        first_time_alias = aliased(models.TimeByUser, subquery)
        result = self.db_session.query(first_time_alias).all()
        return result

    def get_last_by_users(self) -> List[models.TimeByUser]:
        subquery = (
            self.db_session.query(
                models.Heartbeat.user_id.label("user"),
                func.max(models.Heartbeat.time).label("time"),
            )
            .group_by(models.Heartbeat.user_id)
            .subquery()
        )
        # Creating an aliased object to use in the outer query
        last_time_alias = aliased(models.TimeByUser, subquery)
        result = self.db_session.query(last_time_alias).all()
        return result

    def count(self, approximate: bool = False) -> int:
        # Approximate counting seems to be a feature of some databases, but not all.
        return self.db_session.query(func.count(models.Heartbeat.id)).scalar()

    def count_by_user(self, user_id: str) -> int:
        return (
            self.db_session.query(func.count(models.Heartbeat.id))
            .filter_by(user_id=user_id)
            .scalar()
        )

    # def get_entity_set_by_user(self, entity_type: int, user_id: str) -> List[str]:
    #     # Assuming GetEntityColumn is a function that returns the name of the column to filter on based on the entity type
    #     entity_column = get_entity_column(
    #         entity_type
    #     )  # You need to implement this function
    #     results = (
    #         self.db_session.query(distinct(getattr(models.Heartbeat, entity_column)))
    #         .filter_by(user_id=user_id)
    #         .all()
    #     )
    #     return [result[0] for result in results]

    def delete_before(self, time_threshold: datetime):
        self.db_session.query(models.Heartbeat).filter(
            models.Heartbeat.time <= time_threshold
        ).delete()
        self.db_session.commit()

    def delete_by_user(self, user_id: str):
        self.db_session.query(models.Heartbeat).filter_by(user_id=user_id).delete()
        self.db_session.commit()

    def delete_by_user_before(self, user_id: str, time_threshold: datetime):
        self.db_session.query(models.Heartbeat).filter(
            models.Heartbeat.user_id == user_id, models.Heartbeat.time <= time_threshold
        ).delete()
        self.db_session.commit()

    def filtered_query(self, query: Query[T], filter_map: Dict[str, List[str]]):
        for col, vals in filter_map.items():
            column_attribute: InstrumentedAttribute = getattr(models.Heartbeat, col)
            conditions = [
                column_attribute.in_([val if val != "-" else "" for val in vals])
            ]
            query = query.filter(or_(*conditions))
        return query
