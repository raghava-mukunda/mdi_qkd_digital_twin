"""
q11_model.py

Dimension dependent gain model

Author:
MDI-QKD Digital Twin
"""

from dataclasses import dataclass
import numpy as np


@dataclass(slots=True)
class Q11Metrics:

    dimension: int

    gain: float


class Q11Model:

    def calculate(

        self,

        dimension: int

    ):

        #
        # Frame preparation penalty
        #
        # More bins
        # harder stabilization
        #

        stabilization = np.exp(

            -dimension / 12

        )

        #
        # HD information advantage
        #

        advantage = (

            2

            *

            (dimension - 1)

            /

            dimension

        )

        gain = (

            1e-6

            *

            stabilization

            *

            advantage

        )

        return Q11Metrics(

            dimension=dimension,

            gain=float(
                gain
            )
        )