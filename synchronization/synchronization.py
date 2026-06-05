"""
synchronization.py
"""
"""
synchronization.py

Synchronization Controller

Responsible for:

1. Estimating Alice-Bob timing offset
2. Driving Optical Delay Line
3. Iterative alignment

Author:
MDI-QKD Digital Twin
"""

from dataclasses import dataclass
from typing import Optional

import numpy as np

from config.system_params import (
    SystemParameters
)

from synchronization.optical_delay_line import (
    OpticalDelayLine
)


@dataclass(slots=True)
class SynchronizationMetrics:

    initial_delay_ps: float

    residual_delay_ps: float

    iterations: int

    converged: bool


class SyncSystem:

    """
    Charlie Synchronization System
    """

    def __init__(
        self,
        params: Optional[
            SystemParameters
        ] = None
    ):

        self.params = (
            params
            if params is not None
            else SystemParameters()
        )

        self.odl = OpticalDelayLine(
            self.params
        )

        self.tolerance_ps = (
            self.params.synchronization_error_ps
        )

        self.max_iterations = 10

    def estimate_delay_ps(
        self,
        alice_field: np.ndarray,
        bob_field: np.ndarray
    ):

        #
        # Use optical intensity
        #

        alice_power = (
            np.abs(
                alice_field
            ) ** 2
        )

        bob_power = (
            np.abs(
                bob_field
            ) ** 2
        )

        correlation = np.correlate(
            alice_power,
            bob_power,
            mode="full"
        )

        lag = (
            np.argmax(correlation)
            -
            (
                len(alice_power)
                - 1
            )
        )

        delay_s = (
            lag
            /
            self.params.sampling_rate_hz
        )

        delay_ps = (
            delay_s
            * 1e12
        )

        return delay_ps

    def synchronize(
        self,
        alice_field: np.ndarray,
        bob_field: np.ndarray
    ):

        initial_delay = (
            self.estimate_delay_ps(
                alice_field,
                bob_field
            )
        )

        current_field = (
            bob_field.copy()
        )

        residual_delay = (
            initial_delay
        )

        converged = False

        for iteration in range(
            self.max_iterations
        ):

            current_field = (
                self.odl.apply_delay(
                    current_field,
                    -residual_delay
                )
            )

            residual_delay = (
                self.estimate_delay_ps(
                    alice_field,
                    current_field
                )
            )

            if abs(
                residual_delay
            ) <= self.tolerance_ps:

                converged = True

                break

        metrics = (
            SynchronizationMetrics(

                initial_delay_ps=float(
                    initial_delay
                ),

                residual_delay_ps=float(
                    residual_delay
                ),

                iterations=int(
                    iteration + 1
                ),

                converged=bool(
                    converged
                )
            )
        )

        return (
            current_field,
            metrics
        )