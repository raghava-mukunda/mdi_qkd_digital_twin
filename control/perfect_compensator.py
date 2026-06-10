"""
perfect_compensator.py

Oracle compensation.

Applies inverse channel distortion.
"""

from dataclasses import dataclass


@dataclass(slots=True)
class Compensation:

    phase_rad: float
    timing_ps: float
    polarization_deg: float


class PerfectCompensator:

    def compensate(
        self,
        metrics
    ):

        return Compensation(

            phase_rad=(
                -metrics.phase_rad
            ),

            timing_ps=(
                -metrics.timing_ps
            ),

            polarization_deg=(
                -metrics.polarization_deg
            )
        )