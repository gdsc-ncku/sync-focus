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
        """
        Calculate durations based on a list of heartbeats.

        Args:
            heartbeats (List[schemas.Heartbeat]): A list of heartbeats.

        Returns:
            List[schemas.Duration]: A list of durations calculated from the heartbeats.
        """
        # Check if the list of heartbeats is empty, and if so, return an empty list.
        if not heartbeats:
            return []

        # Initialize variables:

        # A list to store calculated duration objects.
        durations: List[schemas.Duration] = []
        # A dictionary to map group hashes to lists of duration objects.
        mapping: Dict[str, List[schemas.Duration]] = {}
        # Stores the most recent duration object for comparison.
        latest: schemas.Duration = None

        # Iterate through each heartbeat object in the list.
        for heartbeat in heartbeats:
            # Convert the heartbeat to a duration object and apply hashing.
            duration = schemas.Duration.from_heartbeat(heartbeat).hashed()

            # Extract the group hash from the duration object for grouping.
            group_hash = duration.group_hash

            # If the group hash is not in the mapping dictionary or the list is empty,
            if group_hash not in mapping or not mapping[group_hash]:
                # Initialize the mapping with the current duration.
                mapping[group_hash] = [duration]

            # If the group hash is already present,
            else:
                # Retrieve the list of durations associated with the group hash.
                duration_list = mapping[group_hash]
                # Get the most recent duration object from the list.
                latest = duration_list[-1]

                # Determine if the current and the latest durations are on the same day.
                same_day = duration.time.date() == latest.time.date()
                # Calculate the time difference between the current duration and the latest, constrained by a threshold.
                dur = min(
                    duration.time - latest.time - latest.duration,
                    heartbeat_diff_threshold,
                )

                # If the durations are not on the same day, reset the time difference to zero.
                if not same_day:
                    dur = timedelta(0)

                # Check conditions to decide whether to create a new duration entry or update the latest duration.
                if (
                    dur >= heartbeat_diff_threshold
                    or latest.group_hash != group_hash
                    or not same_day
                ):
                    # Append the current duration as a new entry.
                    mapping[group_hash].append(duration)
                else:
                    # Increment the heartbeat counter of the latest duration.
                    latest.heartbeat_num += 1
                    # Update the duration of the latest duration object.
                    latest.duration += dur

        # Process each group of durations to finalize their values.
        for group in mapping.values():
            for duration in group:
                # If the duration is zero,
                if duration.duration == timedelta(0):
                    # Set a default duration of 500 milliseconds.
                    duration.duration = timedelta(milliseconds=500)
                # Add the finalized duration to the list of durations.
                durations.append(duration)

        # Special case handling: if there's only one heartbeat and one calculated duration, set the duration to the threshold.
        if len(heartbeats) == 1 and len(durations) == 1:
            durations[0].duration = heartbeat_diff_threshold

        # Return the list of durations, sorted by their time.
        return sorted(durations, key=lambda x: x.time)
