"""
bell_state_measurement.py

Psi- Bell State Analyzer

Author:
MDI-QKD Digital Twin
"""

from dataclasses import dataclass


@dataclass(slots=True)
class BSMResult:

    success: bool

    state: str


class BellStateMeasurement:

    def analyze(

        self,

        d1: bool,

        d2: bool,

        d3: bool,

        d4: bool

    ):

        psi_minus = (

            (d1 and d4)

            or

            (d2 and d3)

        )

        if psi_minus:

            return BSMResult(

                success=True,

                state="psi_minus"
            )

        return BSMResult(

            success=False,

            state="none"
        )