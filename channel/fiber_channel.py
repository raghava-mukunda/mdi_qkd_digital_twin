"""
fiber_channel.py
"""
"""
fiber_channel.py

Optical Fiber Channel

Models:

1. Fiber attenuation
2. Timing jitter
3. Phase drift
4. Polarization mismatch

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
class ChannelMetrics:

    transmission: float

    loss_db: float

    timing_offset_ps: float

    phase_offset_rad: float

    polarization_offset_deg: float


class FiberChannel:

    """
    Optical Fiber Channel
    """

    def __init__(
        self,
        length_km: float,
        params: Optional[
            SystemParameters
        ] = None
    ):

        self.params = (
            params
            if params is not None
            else SystemParameters()
        )

        self.length_km = length_km

        self.loss_db_per_km = (
            self.params.fiber_loss_db_per_km
        )

        self.timing_jitter_ps = (
            self.params.timing_jitter_ps
        )

        self.phase_drift_std_rad = (
            self.params.phase_drift_std_rad
        )

        self.polarization_drift_deg = (
            self.params.polarization_drift_deg
        )

        self.rng = np.random.default_rng(
            self.params.random_seed
        )

    @property
    def total_loss_db(self):

        return (
            self.length_km
            *
            self.loss_db_per_km
        )

    @property
    def transmission(self):

        return (
            10
            **
            (
                -self.total_loss_db
                / 10
            )
        )

    def apply_loss(
        self,
        field: np.ndarray
    ) -> np.ndarray:

        return (
            field
            *
            np.sqrt(
                self.transmission
            )
        )

    def apply_phase_drift(
        self,
        field: np.ndarray
    ):

        phase_offset = (
            self.rng.normal(
                0,
                self.phase_drift_std_rad
            )
        )

        output = (
            field
            *
            np.exp(
                1j *
                phase_offset
            )
        )

        return (
            output,
            phase_offset
        )

    def apply_timing_jitter(
        self,
        field: np.ndarray
    ):

        timing_offset_ps = (
            self.rng.normal(
                0,
                self.timing_jitter_ps
            )
        )

        shift_samples = int(
            round(
                timing_offset_ps
                /
                self.params.time_bin_spacing_ps
            )
        )

        shifted = np.roll(
            field,
            shift_samples
        )

        return (
            shifted,
            timing_offset_ps
        )

    def propagate(
        self,
        field: np.ndarray
    ):

        field = self.apply_loss(
            field
        )

        field, phase_offset = (
            self.apply_phase_drift(
                field
            )
        )

        field, timing_offset = (
            self.apply_timing_jitter(
                field
            )
        )

        polarization_offset = (
            self.rng.normal(
                0,
                self.polarization_drift_deg
            )
        )

        metrics = ChannelMetrics(

            transmission=float(
                self.transmission
            ),

            loss_db=float(
                self.total_loss_db
            ),

            timing_offset_ps=float(
                timing_offset
            ),

            phase_offset_rad=float(
                phase_offset
            ),

            polarization_offset_deg=float(
                polarization_offset
            )
        )

        return (
            field,
            metrics
        )