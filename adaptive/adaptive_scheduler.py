"""
adaptive_scheduler.py

Adaptive Dimension Selection

Chooses d that maximizes SKR
for the current channel state.

Author:
MDI-QKD Digital Twin
"""

from dataclasses import dataclass

from adaptive.channel_state import (
    ChannelState
)

from statistics.x_basis_error import (
    XBasisErrorModel
)

from skr.secret_key_rate import (
    SecretKeyRate
)


@dataclass(slots=True)
class SchedulerDecision:

    selected_dimension: int

    predicted_skr: float

    all_results: dict


class AdaptiveScheduler:

    def __init__(self):

        self.xerr = XBasisErrorModel()

        self.skr = SecretKeyRate()

        self.dimensions = [2, 4, 8, 16]

    def estimate_q11(

        self,

        d: int,

        state: ChannelState

    ):

        #
        # First realistic model
        #
        # loss hurts gain
        #

        transmission = (

            10

            **

            (-state.loss_db / 10)

        )

        return (

            1e-6

            *

            transmission
        )

    def estimate_error(

        self,

        d: int,

        state: ChannelState

    ):

        self.xerr.params.phase_noise_std_rad = (

            state.phase_noise_rad
        )

        visibility = (

            1

            -

            state.polarization_drift_deg
            /
            100
        )

        visibility = max(
            visibility,
            0.5
        )

        result = self.xerr.calculate(

            dimension=d,

            visibility=visibility
        )

        return result.error_rate

    def evaluate_dimension(

        self,

        d: int,

        state: ChannelState

    ):

        q11 = self.estimate_q11(
            d,
            state
        )

        ex11 = self.estimate_error(
            d,
            state
        )

        result = self.skr.calculate(

            dimension=d,

            q11_z=q11,

            ex11=ex11,

            leak_ec=1e-8
        )

        return result.secret_key_rate

    def choose_dimension(

        self,

        state: ChannelState

    ):

        results = {}

        for d in self.dimensions:

            results[d] = (

                self.evaluate_dimension(
                    d,
                    state
                )
            )

        best_d = max(
            results,
            key=results.get
        )

        return SchedulerDecision(

            selected_dimension=best_d,

            predicted_skr=results[best_d],

            all_results=results
        )