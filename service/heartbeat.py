from datetime import datetime
from typing import Dict, List, Optional, TypeVar

from sqlalchemy import func, or_
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from sqlalchemy.orm.attributes import InstrumentedAttribute
from sqlalchemy.orm.query import Query

import models as models
import schemas as schemas

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

    def get_first_by_users(self) -> List[schemas.TimeByUser]:
        """
        Retrieves the first heartbeat time for each user.

        Returns:
            A list of TimeByUser objects representing the first heartbeat time for each user.
        """
        subquery = (
            self.db_session.query(
                models.Heartbeat.user_id.label("user_id"),
                func.min(models.Heartbeat.time).label("time"),
            )
            .group_by(models.Heartbeat.user_id)
            .subquery()
        )
        result = self.db_session.query(
            subquery.c.user_id.label("user_id"),
            subquery.c.time.label("time"),
        ).all()

        return [schemas.TimeByUser(**row._asdict()) for row in result]

    def get_last_by_users(self) -> List[schemas.TimeByUser]:
        """
        Retrieves the last heartbeat time for each user.

        Returns:
            A list of TimeByUser objects representing the last heartbeat time for each user.
        """
        subquery = (
            self.db_session.query(
                models.Heartbeat.user_id.label("user_id"),
                func.max(models.Heartbeat.time).label("time"),
            )
            .group_by(models.Heartbeat.user_id)
            .subquery()
        )
        result = self.db_session.query(
            subquery.c.user_id.label("user_id"),
            subquery.c.time.label("time"),
        ).all()

        return [schemas.TimeByUser(**row._asdict()) for row in result]

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

    def get_domain_stats(
        self,
        user_id: str,
        from_time: datetime,
        to_time: datetime,
        limit: int,
        offset: int,
    ) -> List[schemas.DomainStat]:
        """
        Retrieves domain statistics for a given user within a specified time range.

        Args:
            user_id (str): The ID of the user.
            from_time (datetime): The start time of the time range.
            to_time (datetime): The end time of the time range.
            limit (int): The maximum number of domain statistics to retrieve.
            offset (int): The offset for pagination.

        Returns:
            List[schemas.DomainStat]: A list of domain statistics.

        """
        # Define the CTE for domains
        domains_cte = (
            self.db_session.query(
                models.Heartbeat.domain.label("d"),
                models.Heartbeat.user_id,
                func.min(models.Heartbeat.time).label("first_time"),
                func.max(models.Heartbeat.time).label("last_time"),
                func.count().label("count"),
            )
            .filter(
                models.Heartbeat.user_id == user_id,
                models.Heartbeat.domain != "",
                models.Heartbeat.time.between(from_time, to_time),
            )
            .group_by(models.Heartbeat.domain, models.Heartbeat.user_id)
            .order_by(func.max(models.Heartbeat.time).desc())
            .limit(limit)
            .offset(offset)
            .cte("domains")
        )

        # Main query that selects from the CTE
        domain_stats_query = (
            self.db_session.query(
                domains_cte.c.user_id.label("user_id"),
                domains_cte.c.d.label("domain"),
                func.min(domains_cte.c.first_time).label("first_time"),
                func.max(domains_cte.c.last_time).label("last_time"),
                func.sum(domains_cte.c.count).label("count"),
            )
            .group_by(domains_cte.c.d, domains_cte.c.user_id)
            .order_by(func.max(domains_cte.c.last_time).desc())
        )

        # Mapping the results to DomainStat instances
        domain_stats = [
            schemas.DomainStat(
                user_id=row.user_id,
                domain=row.domain,
                first_time=row.first_time,
                last_time=row.last_time,
                count=row.count,
            )
            for row in domain_stats_query.all()
        ]

        return domain_stats

    def filtered_query(self, query: Query[T], filter_map: Dict[str, List[str]]):
        for col, vals in filter_map.items():
            column_attribute: InstrumentedAttribute = getattr(models.Heartbeat, col)
            conditions = [
                column_attribute.in_([val if val != "-" else "" for val in vals])
            ]
            query = query.filter(or_(*conditions))
        return query
