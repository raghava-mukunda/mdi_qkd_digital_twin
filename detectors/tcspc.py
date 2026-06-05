"""
tcspc.py
"""
"""
tcspc.py

Time-Correlated Single Photon Counting

Stores timestamped SNSPD events.

Author:
MDI-QKD Digital Twin
"""

from dataclasses import dataclass
from typing import List


@dataclass(slots=True)
class TimestampEvent:

    timestamp_ps: float

    channel: int

    photon_number: float


class TCSPCModule:

    def __init__(self):

        self.events: List[
            TimestampEvent
        ] = []

    def add_event(
        self,
        timestamp_ps: float,
        channel: int,
        photon_number: float
    ):

        self.events.append(

            TimestampEvent(

                timestamp_ps=float(
                    timestamp_ps
                ),

                channel=int(
                    channel
                ),

                photon_number=float(
                    photon_number
                )
            )
        )

    def sort_events(self):

        self.events.sort(
            key=lambda e:
            e.timestamp_ps
        )

    def clear(self):

        self.events.clear()

    def get_events(self):

        self.sort_events()

        return self.events

    def event_count(self):

        return len(
            self.events
        )