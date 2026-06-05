"""
real_scheduler.py

Uses actual digital twin modules
to estimate achievable SKR.

Author:
MDI-QKD Digital Twin
"""

from adaptive.channel_state import (
    ChannelState
)

from bsm.quantum_state import (
    QuantumStateFactory
)

from bsm.charlie_receiver import (
    CharlieReceiver
)

from statistics.x_basis_error import (
    XBasisErrorModel
)

from skr.secret_key_rate import (
    SecretKeyRate
)


class RealScheduler:

    def __init__(self):

        self.charlie = CharlieReceiver()

        self.xerr = XBasisErrorModel()

        self.skr = SecretKeyRate()

    def estimate_q11(

        self,

        dimension,

        state,

        trials=500

    ):

        alice = (
            QuantumStateFactory.create(
                dimension,
                "X",
                0
            )
        )

        bob = (
            QuantumStateFactory.create(
                dimension,
                "X",
                0
            )
        )

        success = 0

        for _ in range(trials):

            result = (

                self.charlie.process_trial(

                    alice,

                    bob,

                    timing_offset_ps=
                    state.timing_jitter_ps,

                    phase_offset_rad=
                    state.phase_noise_rad,

                    polarization_offset_deg=
                    state.polarization_drift_deg
                )
            )

            if result.psi_minus:

                success += 1

        transmission = (

            10

            **

            (-state.loss_db/10)
        )

        return (

            success

            /

            trials

            *

            transmission
        )

    def evaluate_dimension(

        self,

        dimension,

        state

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

        x = self.xerr.calculate(

            dimension,

            visibility
        )

        q11 = self.estimate_q11(

            dimension,

            state
        )

        result = self.skr.calculate(

            dimension=dimension,

            q11_z=q11,

            ex11=x.error_rate,

            leak_ec=1e-4*q11
        )

        return result.secret_key_rate

    def choose_dimension(

        self,

        state

    ):

        results = {}

        for d in [

            2,
            4,
            8,
            16

        ]:

            results[d] = (

                self.evaluate_dimension(
                    d,
                    state
                )
            )

        best = max(
            results,
            key=results.get
        )

        return best, results