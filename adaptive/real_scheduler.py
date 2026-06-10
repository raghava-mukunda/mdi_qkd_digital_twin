"""
real_scheduler.py

Physical HD-MDI-QKD Scheduler
"""

from adaptive.channel_state import ChannelState

from statistics.physical_q11 import PhysicalQ11

from statistics.x_basis_error import XBasisErrorModel

from skr.secret_key_rate import SecretKeyRate

from security.decoy_estimator import DecoyEstimator

import numpy as np


class RealScheduler:

    def __init__(
        self,
        fast_mode=False
    ):

        self.fast_mode = fast_mode

        self.q11_model = PhysicalQ11()

        self.xerr = XBasisErrorModel()

        self.skr = SecretKeyRate()

        self.decoy = DecoyEstimator()

    def fast_q11(
        self,
        dimension,
        state
    ):

        P_BSM = {

            2: 0.4782,
            4: 0.4486,
            8: 0.3946,
            16: 0.3068,

        }

        mu = 0.20

        p1 = mu * np.exp(-mu)

        eta = 10 ** (

            -state.loss_db / 20

        )

        phase_vis = np.cos(

            state.phase_noise_rad / 2

        ) ** 2

        timing_vis = np.exp(

            -(state.timing_jitter_ps ** 2)

            /

            (2 * 250 ** 2)

        )

        pol_vis = np.cos(

            np.deg2rad(
                state.polarization_drift_deg
            )

        ) ** 2

        visibility = (

            phase_vis
            *
            timing_vis
            *
            pol_vis

        )

        detector_eff = 0.95

        q11 = (

            p1
            *
            p1
            *
            eta
            *
            eta
            *
            detector_eff
            *
            detector_eff
            *
            P_BSM[dimension]
            *
            visibility

        )

        return q11

    def evaluate_dimension(
        self,
        dimension,
        state,
        trials=100
    ):

        #
        # Q11 estimation
        #

        if self.fast_mode:

            q_mu_value = self.fast_q11(
                dimension,
                state
            )

        else:

            q_mu_result = self.q11_model.estimate(

                dimension,

                state.loss_db,

                state.phase_noise_rad,

                state.timing_jitter_ps,

                state.polarization_drift_deg,

                trials=trials

            )

            q_mu_value = q_mu_result.q11

        #
        # Decoy gains
        #

        q_nu = 0.25 * q_mu_value

        q_omega = 0.01 * q_mu_value

        decoy = self.decoy.estimate(

            mu=0.4,

            nu=0.1,

            omega=0,

            q_mu=q_mu_value,

            q_nu=q_nu,

            q_omega=q_omega

        )

        #
        # X-basis error
        #

        if state.residual_phase_rad is not None:

            x = self.xerr.calculate(

                dimension,

                visibility=0.95,

                residual_phase=
                state.residual_phase_rad

            )

        else:

            self.xerr.params.phase_noise_std_rad = (

                state.phase_noise_rad

            )

            x = self.xerr.calculate(

                dimension,

                visibility=0.95

            )

        #
        # Secret key rate
        #

        result = self.skr.calculate(

            dimension=dimension,

            q11_z=decoy.q11,

            ex11=x.error_rate,

            leak_ec=1e-4 * decoy.q11

        )

        return result.secret_key_rate

    def choose_dimension(
        self,
        state
    ):

        results = {}

        effective_bits = {}

        for d in [2, 4, 8, 16]:

            results[d] = self.evaluate_dimension(

                d,

                state

            )

            effective_bits[d] = (

                results[d]

                *

                np.log2(d)

            )

        best = max(

            effective_bits,

            key=effective_bits.get

        )

        return best, results