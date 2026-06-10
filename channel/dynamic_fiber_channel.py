"""
dynamic_fiber_channel.py

Realistic time-varying fiber channel.

Models:
1. Slow thermal drift
2. Mechanical vibration
3. Correlated stochastic phase noise
4. Rare phase slips
5. Correlated timing jitter
6. Correlated polarization drift

Author:
MDI-QKD Digital Twin
"""

from dataclasses import dataclass
import numpy as np

from channel.fiber_channel import FiberChannel


@dataclass(slots=True)
class DynamicMetrics:

    phase_rad: float

    timing_ps: float

    polarization_deg: float


class DynamicFiberChannel(FiberChannel):

    def __init__(
        self,
        length_km,
        phase_alpha=0.9995,
        timing_alpha=0.995,
        pol_alpha=0.998,
        slip_probability=5e-3,
        slip_std=0.50,
    ):

        super().__init__(length_km)

        self.phase_alpha = phase_alpha
        self.timing_alpha = timing_alpha
        self.pol_alpha = pol_alpha

        self.slip_probability = slip_probability
        self.slip_std = slip_std

        self.frame = 0

        #
        # Correlated random components
        #

        self.phase_state = 0.0
        self.timing_state = 0.0
        self.pol_state = 0.0

    def step(self):

        self.frame += 1

        #
        # Slow thermal drift
        #
        # Large timescale
        #

        thermal_phase = (

            0.10

            *

            np.sin(

                2*np.pi

                *

                self.frame

                /

                2000
            )
        )

        #
        # Mechanical vibration
        #
        # Smaller amplitude
        #

        vibration_phase = (

            0.05

            *

            np.sin(

                2*np.pi

                *

                self.frame

                /

                500
            )
        )

        #
        # Correlated stochastic phase
        #

        self.phase_state = (

            self.phase_alpha

            *

            self.phase_state

            +

            self.rng.normal(

                0,

                0.01
            )
        )

        #
        # Rare phase slips
        #

        phase_slip = 0.0

        if self.rng.random() < self.slip_probability:

            phase_slip = self.rng.normal(

                0,

                self.slip_std
            )

        phase = (

            thermal_phase

            +

            vibration_phase

            +

            self.phase_state

            +

            phase_slip
        )

        #
        # Timing jitter
        #

        self.timing_state = (

            self.timing_alpha

            *

            self.timing_state

            +

            self.rng.normal(

                0,

                5.0
            )
        )

        #
        # Polarization drift
        #

        self.pol_state = (

            self.pol_alpha

            *

            self.pol_state

            +

            self.rng.normal(

                0,

                1.00
            )
        )

        return DynamicMetrics(

            phase_rad=float(
                phase
            ),

            timing_ps=float(
                self.timing_state
            ),

            polarization_deg=float(
                self.pol_state
            )
        )