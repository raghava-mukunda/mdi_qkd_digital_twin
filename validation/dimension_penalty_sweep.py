"""
dimension_penalty_sweep.py

Investigate why d=16 drops.

Author:
MDI-QKD Digital Twin
"""

import numpy as np

from skr.secret_key_rate import (
    SecretKeyRate
)

skr = SecretKeyRate()

print()
print("="*80)
print("DIMENSION PENALTY MODEL")
print("="*80)

Q11_BASE = 1e-6

for d in [

    2,
    4,
    8,
    16

]:

    #
    # first-order penalty
    #

    penalty = np.exp(

        -(d/10.0)**2

    )

    q11 = (

        Q11_BASE

        *

        penalty
    )

    result = skr.calculate(

        dimension=d,

        q11_z=q11,

        ex11=0.03,

        leak_ec=1e-8
    )

    print()

    print(
        f"d={d}"
    )

    print(
        f"Penalty={penalty:.4f}"
    )

    print(
        f"Q11={q11:.3e}"
    )

    print(
        f"SKR={result.secret_key_rate:.3e}"
    )