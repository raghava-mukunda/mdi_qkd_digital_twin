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

    def __init__(self):

        self.q11_model = PhysicalQ11()

        self.xerr = XBasisErrorModel()

        self.skr = SecretKeyRate()

        self.decoy = DecoyEstimator()

    def evaluate_dimension(

        self,

        dimension,

        state,

        trials=1000

    ):

        q_mu = self.q11_model.estimate(

            dimension,

            state.loss_db,

            state.phase_noise_rad,

            state.timing_jitter_ps,

            state.polarization_drift_deg,

            trials=1000

        )

        q_nu = 0.25 * q_mu.q11

        q_omega = 0.01 * q_mu.q11

        decoy = self.decoy.estimate(

            mu=0.4,

            nu=0.1,

            omega=0,

            q_mu=q_mu.q11,

            q_nu=q_nu,

            q_omega=q_omega

        )

        self.xerr.params.phase_noise_std_rad = (

            state.phase_noise_rad

        )

        x = self.xerr.calculate(

            dimension,

            visibility=0.95

        )

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

        for d in [2,4,8,16]:

            results[d] = (

                self.evaluate_dimension(

                    d,

                    state

                )

            )

            effective_bits[d] = (

                results[d]

                *

                np.log2(d)

            )

        best = max(

            effective_bits,

            key=results.get

        )

        return best, results