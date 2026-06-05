"""
frame_yield_model.py

HD-MDI-QKD Frame Yield Model
"""

import numpy as np

from skr.secret_key_rate import (
    SecretKeyRate
)

skr = SecretKeyRate()

print()
print("="*80)
print("FRAME-LEVEL YIELD MODEL")
print("="*80)

BASE_VISIBILITY = 0.95

for d in [2,4,8,16]:

    windows = d - 1

    #
    # detector saturation
    #

    detector_availability = np.exp(
        -windows / 8
    )

    #
    # visibility degradation
    #

    visibility = (
        BASE_VISIBILITY
        *
        np.exp(
            -d/20
        )
    )

    #
    # effective yield
    #

    q11 = (
        windows
        *
        0.5
        *
        visibility
        *
        detector_availability
        /
        d
    )

    result = skr.calculate(

        dimension=d,

        q11_z=q11,

        ex11=0.03,

        leak_ec=1e-4*q11
    )

    print()

    print(
        f"d={d}"
    )

    print(
        f"windows={windows}"
    )

    print(
        f"availability={detector_availability:.4f}"
    )

    print(
        f"visibility={visibility:.4f}"
    )

    print(
        f"Q11={q11:.6f}"
    )

    print(
        f"SKR={result.secret_key_rate:.6f}"
    )