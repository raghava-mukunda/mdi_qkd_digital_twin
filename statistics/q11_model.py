"""
q11_model.py

Legacy compatibility wrapper.

Uses PhysicalQ11 internally.

Author:
MDI-QKD Digital Twin
"""

from dataclasses import dataclass

from statistics.physical_q11 import (
    PhysicalQ11
)


@dataclass(slots=True)
class Q11Metrics:

    dimension: int

    gain: float


class Q11Model:

    def __init__(self):

        self.model = PhysicalQ11()

    def calculate(

        self,

        dimension: int

    ):

        result = self.model.estimate(

            dimension=dimension,

            loss_db=5,

            phase_offset_rad=0.1,

            timing_offset_ps=20,

            polarization_offset_deg=2,

            trials=3000

        )

        return Q11Metrics(

            dimension=dimension,

            gain=result.q11

        )