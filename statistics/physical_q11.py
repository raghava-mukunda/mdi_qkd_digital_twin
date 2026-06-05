"""
physical_q11.py

Physical Q11 Estimation

Based on:

VOA
Fiber Loss
SNSPD Efficiency
BSM Success Probability

Author:
MDI-QKD Digital Twin
"""

from dataclasses import dataclass

import numpy as np

from config.system_params import (
    SystemParameters
)

from bsm.quantum_state import (
    QuantumStateFactory
)

from bsm.charlie_receiver import (
    CharlieReceiver
)


@dataclass(slots=True)
class PhysicalQ11Metrics:

    dimension: int

    mu_a: float

    mu_b: float

    eta_a: float

    eta_b: float

    single_photon_probability: float

    bsm_probability: float

    q11: float


class PhysicalQ11:

    def __init__(

        self,

        params: SystemParameters | None = None

    ):

        self.params = (

            params

            if params is not None

            else SystemParameters()

        )

        self.charlie = CharlieReceiver()

    def poisson_single(

        self,

        mu: float

    ):

        return (

            mu

            *

            np.exp(-mu)

        )

    def channel_transmission(

        self,

        loss_db: float

    ):

        return (

            10

            **

            (

                -loss_db

                /

                10

            )

        )

    def estimate(

        self,

        dimension: int,

        loss_db: float,

        phase_offset_rad: float,

        timing_offset_ps: float,

        polarization_offset_deg: float,

        trials: int = 5000

    ):

        mu_a = self.params.signal_mu

        mu_b = self.params.signal_mu

        p1_a = self.poisson_single(
            mu_a
        )

        p1_b = self.poisson_single(
            mu_b
        )

        eta_a = self.channel_transmission(
            loss_db / 2
        )

        eta_b = self.channel_transmission(
            loss_db / 2
        )

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

        successes = 0

        for _ in range(trials):

            result = (

                self.charlie.process_trial(

                    alice,

                    bob,

                    timing_offset_ps=
                    timing_offset_ps,

                    phase_offset_rad=
                    phase_offset_rad,

                    polarization_offset_deg=
                    polarization_offset_deg

                )

            )

            if result.psi_minus:

                successes += 1

        p_bsm = (

            successes

            /

            trials

        )

        detector_eff = (
            self.params.detector_efficiency
        )

        q11 = (

            p1_a

            *

            p1_b

            *

            eta_a

            *

            eta_b

            *

            detector_eff

            *

            detector_eff

            *

            p_bsm

        )

        return PhysicalQ11Metrics(

            dimension=dimension,

            mu_a=mu_a,

            mu_b=mu_b,

            eta_a=eta_a,

            eta_b=eta_b,

            single_photon_probability=
            p1_a * p1_b,

            bsm_probability=
            p_bsm,

            q11=q11

        )