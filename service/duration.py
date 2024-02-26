from datetime import datetime, timedelta
from typing import Dict, Final, List

from sqlalchemy.orm import Session

import models as models
import schemas as schemas

from .heartbeat import HeartbeatService

heartbeat_diff_threshold: Final[timedelta] = timedelta(minutes=2)


class DurationService:
    db_session: Session = None
    heartbeat_service: HeartbeatService = None

    def __init__(self, db_session: Session, heartbeat_service: HeartbeatService):
        self.db_session = db_session
        self.heartbeat_service = heartbeat_service

    def get(
        self, from_time: datetime, to_time: datetime, user_id: str
    ) -> List[schemas.Duration]:
        heartbeat_models: List[
            models.Heartbeat
        ] = self.heartbeat_service.get_all_within(from_time, to_time, user_id)
        heartbeats: list[schemas.Heartbeat] = [
            schemas.Heartbeat.model_validate(heartbeat)
            for heartbeat in heartbeat_models
        ]
        durations = self._calculate_durations(heartbeats)
        return durations

    def _calculate_durations(
        self, heartbeats: List[schemas.Heartbeat]
    ) -> List[schemas.Duration]:
        if not heartbeats:
            return []

        # Initialize
        durations: List[schemas.Duration] = []
        mapping: Dict[str, List[schemas.Duration]] = {}
        latest: schemas.Duration = None

        for heartbeat in heartbeats:
            duration = schemas.Duration.from_heartbeat(heartbeat).hashed()
            group_hash = duration.group_hash

            if group_hash not in mapping or not mapping[group_hash]:
                mapping[group_hash] = [duration]
            else:
                duration_list = mapping[group_hash]
                latest = duration_list[-1]

                same_day = duration.time.date() == latest.time.date()
                dur = min(
                    duration.time - latest.time - latest.duration,
                    heartbeat_diff_threshold,
                )

                if not same_day:
                    dur = timedelta(0)

                if (
                    dur >= heartbeat_diff_threshold
                    or latest.group_hash != group_hash
                    or not same_day
                ):
                    mapping[group_hash].append(duration)
                else:
                    latest.heartbeat_num += 1
                    latest.duration += dur

        for group in mapping.values():
            for duration in group:
                if duration.duration == timedelta(0):
                    duration.duration = timedelta(milliseconds=500)
                durations.append(duration)

        if len(heartbeats) == 1 and len(durations) == 1:
            durations[0].duration = heartbeat_diff_threshold

        return sorted(durations, key=lambda x: x.time)
