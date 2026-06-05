"""
spad.py
"""
"""
spad.py

SNSPD Detector Model

Models:

1. Detection efficiency
2. Dead time
3. Dark counts
4. Timing jitter
5. Timestamp generation

Author:
MDI-QKD Digital Twin
"""

from dataclasses import dataclass
from typing import Optional

import numpy as np

from config.system_params import (
    SystemParameters
)


@dataclass(slots=True)
class DetectionEvent:

    detected: bool

    timestamp_ps: float

    channel: int

    photon_number: float


@dataclass(slots=True)
class SNSPDMetrics:

    efficiency: float

    dead_time_ns: float

    dark_count_rate_hz: float

    timing_jitter_ps: float


class SNSPDDetector:

    """
    SNSPD detector.

    Click probability:

        Pclick = 1 - exp(-ημ)
    """

    def __init__(
        self,
        channel_id: int,
        params: Optional[
            SystemParameters
        ] = None
    ):

        self.params = (
            params
            if params is not None
            else SystemParameters()
        )

        self.channel_id = channel_id

        #
        # IISc values
        #

        self.efficiency = 0.95

        self.dead_time_ns = 12.0

        self.dark_count_rate_hz = 50.0

        self.timing_jitter_ps = 20.0

        self.last_click_time_ps = (
            -np.inf
        )

        self.rng = np.random.default_rng(
            self.params.random_seed
            + channel_id
        )

    def click_probability(
        self,
        mu: float
    ):

        return float(
            1
            -
            np.exp(
                -self.efficiency
                *
                mu
            )
        )

    def in_dead_time(
        self,
        timestamp_ps: float
    ):

        return (
            timestamp_ps
            -
            self.last_click_time_ps
        ) < (
            self.dead_time_ns
            * 1000
        )

    def detect(
        self,
        mu: float,
        timestamp_ps: float
    ) -> DetectionEvent:

        #
        # Dead time check
        #

        if self.in_dead_time(
            timestamp_ps
        ):

            return DetectionEvent(
                detected=False,
                timestamp_ps=timestamp_ps,
                channel=self.channel_id,
                photon_number=mu
            )

        #
        # Photon detection
        #

        p_click = (
            self.click_probability(
                mu
            )
        )

        detected = (
            self.rng.random()
            <
            p_click
        )

        #
        # Dark count
        #

        dark_prob = (
            self.dark_count_rate_hz
            *
            1e-12
        )

        dark_count = (
            self.rng.random()
            <
            dark_prob
        )

        detected = (
            detected
            or
            dark_count
        )

        if not detected:

            return DetectionEvent(
                detected=False,
                timestamp_ps=timestamp_ps,
                channel=self.channel_id,
                photon_number=mu
            )

        #
        # Timing jitter
        #

        jitter = (
            self.rng.normal(
                0,
                self.timing_jitter_ps
            )
        )

        measured_time = (
            timestamp_ps
            +
            jitter
        )

        self.last_click_time_ps = (
            measured_time
        )

        return DetectionEvent(

            detected=True,

            timestamp_ps=float(
                measured_time
            ),

            channel=int(
                self.channel_id
            ),

            photon_number=float(
                mu
            )
        )

    def metrics(
        self
    ):

        return SNSPDMetrics(

            efficiency=float(
                self.efficiency
            ),

            dead_time_ns=float(
                self.dead_time_ns
            ),

            dark_count_rate_hz=float(
                self.dark_count_rate_hz
            ),

            timing_jitter_ps=float(
                self.timing_jitter_ps
            )
        )