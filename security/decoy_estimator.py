"""
decoy_estimator.py

Three-intensity decoy-state estimator.

Simplified asymptotic implementation.

Author:
MDI-QKD Digital Twin
"""

from dataclasses import dataclass

import numpy as np


@dataclass(slots=True)
class DecoyMetrics:

    q_mu: float

    q_nu: float

    q_omega: float

    y11: float

    q11: float


class DecoyEstimator:

    def estimate(

        self,

        mu: float,

        nu: float,

        omega: float,

        q_mu: float,

        q_nu: float,

        q_omega: float

    ):

        numerator = (

            mu**2
            *
            np.exp(mu)

            *
            q_nu

            -

            nu**2
            *
            np.exp(nu)

            *
            q_mu

        )

        denominator = (

            mu
            *
            nu
            *
            (mu - nu)

        )

        y11 = max(

            numerator
            /
            denominator,

            0.0

        )

        q11 = (

            mu

            *
            mu

            *

            np.exp(-2*mu)

            *

            y11

        )

        return DecoyMetrics(

            q_mu=q_mu,

            q_nu=q_nu,

            q_omega=q_omega,

            y11=float(y11),

            q11=float(q11)

        )