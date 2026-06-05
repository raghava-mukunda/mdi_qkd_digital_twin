"""
charlie_receiver.py

Dimension-Aware Charlie Receiver

HD-MDI-QKD Bell-State Measurement

Author:
MDI-QKD Digital Twin
"""

from dataclasses import dataclass

import numpy as np

from interference.beam_splitter import (
    BeamSplitter
)

from bsm.quantum_state import (
    QuantumState
)

from bsm.bell_state_measurement import (
    BellStateMeasurement
)


@dataclass(slots=True)
class CharlieTrial:

    dimension: int

    visibility: float

    psi_probability: float

    coincidence_probability: float

    d1: bool

    d2: bool

    d3: bool

    d4: bool

    psi_minus: bool


class CharlieReceiver:

    """
    Charlie Bell-State Analyzer

    Visibility comes from HOM interference.

    Dimension dependence should emerge
    through coherence degradation in the
    HOM model, not through artificial
    Charlie penalties.
    """

    def __init__(self):

        self.bs = BeamSplitter()

        self.bsm = BellStateMeasurement()

        self.rng = np.random.default_rng()

    def process_trial(

        self,

        alice_state: QuantumState,

        bob_state: QuantumState,

        timing_offset_ps: float = 0,

        phase_offset_rad: float = 0,

        polarization_offset_deg: float = 0

    ):

        hom = self.bs.interfere(

            alice_state,

            bob_state,

            timing_offset_ps,

            phase_offset_rad,

            polarization_offset_deg
        )

        visibility = float(
            hom.total_visibility
        )

        dimension = (
            alice_state.dimension
        )

        #
        # Bell-state projection probability
        #
        # Maximum Psi- success = 50%
        #

        psi_probability = (

            0.5

            *

            visibility

        )

        psi_probability = np.clip(

            psi_probability,

            0.0,

            0.5
        )

        #
        # Residual coincidences
        #

        coincidence_probability = (

            0.5

            *

            (

                1.0

                -

                visibility

            )

        )

        coincidence_probability = np.clip(

            coincidence_probability,

            0.0,

            0.5
        )

        r = self.rng.random()

        d1 = False
        d2 = False
        d3 = False
        d4 = False

        #
        # Successful Psi-
        #

        if r < psi_probability:

            if self.rng.random() < 0.5:

                d1 = True
                d4 = True

            else:

                d2 = True
                d3 = True

        #
        # Non-Bell coincidence
        #

        elif r < (

            psi_probability

            +

            coincidence_probability

        ):

            pairs = [

                (1, 2),

                (1, 3),

                (2, 4),

                (3, 4)

            ]

            pair = pairs[

                self.rng.integers(
                    len(pairs)
                )

            ]

            if 1 in pair:
                d1 = True

            if 2 in pair:
                d2 = True

            if 3 in pair:
                d3 = True

            if 4 in pair:
                d4 = True

        result = self.bsm.analyze(

            d1,

            d2,

            d3,

            d4

        )

        return CharlieTrial(

            dimension=dimension,

            visibility=visibility,

            psi_probability=float(
                psi_probability
            ),

            coincidence_probability=float(
                coincidence_probability
            ),

            d1=d1,

            d2=d2,

            d3=d3,

            d4=d4,

            psi_minus=result.success

        )