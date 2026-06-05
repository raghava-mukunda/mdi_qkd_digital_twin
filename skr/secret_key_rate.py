"""
secret_key_rate.py

HD-MDI-QKD Secret Key Rate

Based on IISc paper Eq. (2)

S = Q11z [log2(d) - hd(ex11)]
    - leakEC

Author:
MDI-QKD Digital Twin
"""

from dataclasses import dataclass

import numpy as np


@dataclass(slots=True)
class SKRMetrics:

    dimension: int

    gain_q11: float

    error_rate: float

    entropy_hd: float

    information_per_photon: float

    leak_ec: float

    secret_key_rate: float


class SecretKeyRate:

    def hd_entropy(
        self,
        q: float,
        d: int
    ):

        #
        # Numerical protection
        #

        q = np.clip(
            q,
            1e-12,
            1 - 1e-12
        )

        return (

            -q
            *
            np.log2(
                q / (d - 1)
            )

            -

            (1 - q)
            *
            np.log2(
                1 - q
            )
        )

    def information_capacity(
        self,
        d: int
    ):

        return (

            2

            *

            (d - 1)

            /

            d

            *

            np.log2(d)
        )

    def calculate(

        self,

        dimension: int,

        q11_z: float,

        ex11: float,

        leak_ec: float

    ):

        hd = self.hd_entropy(

            ex11,

            dimension
        )

        info = self.information_capacity(
            dimension
        )

        raw_skr = (

            q11_z

            *

            (

                np.log2(
                    dimension
                )

                -

                hd

            )

            -

            leak_ec
        )

        #
        # Security cut-off
        #
        # If X-basis error approaches
        # random guessing, no secret key.
        #

        if ex11 >= 0.45:

            raw_skr = 0.0

        #
        # Never allow negative SKR
        #

        raw_skr = max(
            raw_skr,
            0.0
        )

        return SKRMetrics(

            dimension=dimension,

            gain_q11=q11_z,

            error_rate=ex11,

            entropy_hd=hd,

            information_per_photon=info,

            leak_ec=leak_ec,

            secret_key_rate=raw_skr
        )