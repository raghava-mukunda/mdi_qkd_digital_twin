"""
validate_iisc.py
"""
"""
validate_iisc.py

Dimension Scaling Validation

Author:
MDI-QKD Digital Twin
"""

from skr.secret_key_rate import (
    SecretKeyRate
)

skr = SecretKeyRate()

print()
print("="*70)
print("HD-MDI-QKD DIMENSION SCALING")
print("="*70)

#
# same gain
# same error
#

Q11 = 1e-6

EX = 0.03

LEAK = 1e-8

for d in [

    2,
    4,
    8,
    16

]:

    result = skr.calculate(

        dimension=d,

        q11_z=Q11,

        ex11=EX,

        leak_ec=LEAK
    )

    print()

    print(
        f"d = {d}"
    )

    print(
        f"Info Capacity = "
        f"{result.information_per_photon:.4f}"
    )

    print(
        f"SKR = "
        f"{result.secret_key_rate:.6e}"
    )