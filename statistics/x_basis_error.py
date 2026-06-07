"""
x_basis_error.py

Dimension-dependent X-basis error model

Author:
MDI-QKD Digital Twin
"""

from dataclasses import dataclass
import numpy as np

from config.system_params import (
    SystemParameters
)


@dataclass(slots=True)
class XBasisMetrics:

    dimension: int

    phase_visibility: float

    error_rate: float


class XBasisErrorModel:

    def __init__(
        self,
        params: SystemParameters | None = None
    ):

        self.params = (
            params
            if params is not None
            else SystemParameters()
        )

    def calculate(

        self,

        dimension: int,

        visibility: float

    ):

        #
        # Stronger accumulation
        #
        # Coherent phase errors
        # grow approximately
        # with total frame span.
        #

        sigma_phi = (

            self.params.phase_noise_std_rad

            *

            (dimension**0.75)
        )

        phase_visibility = (

            visibility

            *

            np.exp(
                -(sigma_phi**2)/2
            )
        )

        ex = (

            1

            -

            phase_visibility

        ) / 2

        return XBasisMetrics(

            dimension=dimension,

            phase_visibility=float(
                phase_visibility
            ),

            error_rate=float(
                ex
            )
        )