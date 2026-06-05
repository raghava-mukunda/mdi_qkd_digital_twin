"""
frame_engine.py

HD-MDI-QKD Frame Simulator

One frame contains d time bins.

Author:
MDI-QKD Digital Twin
"""

from dataclasses import dataclass

import numpy as np

from bsm.charlie_receiver import (
    CharlieReceiver
)

from bsm.quantum_state import (
    QuantumStateFactory
)


@dataclass(slots=True)
class FrameResult:

    dimension: int

    windows: int

    successful_bsm: int

    q11: float


class FrameEngine:

    def __init__(self):

        self.charlie = CharlieReceiver()

    def run_frame(

        self,

        dimension: int

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

        windows = (
            dimension - 1
        )

        successes = 0

        #
        # detector availability
        #

        detector_free = True

        for w in range(windows):

            if not detector_free:

                continue

            result = (
                self.charlie.process_trial(
                    alice,
                    bob
                )
            )

            if result.psi_minus:

                successes += 1

                #
                # emulate dead time
                #

                detector_free = False

        q11 = (
            successes
            /
            windows
        )

        return FrameResult(

            dimension=dimension,

            windows=windows,

            successful_bsm=successes,

            q11=q11
        )