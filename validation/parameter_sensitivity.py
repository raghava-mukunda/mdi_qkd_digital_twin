"""
parameter_sensitivity.py

Determine which physical parameter
creates the d=16 degradation.

Author:
MDI-QKD Digital Twin
"""

from skr.secret_key_rate import (
    SecretKeyRate
)

from statistics.x_basis_error import (
    XBasisErrorModel
)

skr = SecretKeyRate()

xerr = XBasisErrorModel()

print()
print("=" * 80)
print("PHASE NOISE SENSITIVITY")
print("=" * 80)

for sigma in [

    0.02,
    0.05,
    0.10,
    0.20,
    0.30

]:

    xerr.params.phase_noise_std_rad = sigma

    print()
    print(
        f"Sigma = {sigma}"
    )

    for d in [2,4,8,16]:

        x = xerr.calculate(
            dimension=d,
            visibility=0.995
        )

        r = skr.calculate(

            dimension=d,

            q11_z=1e-6,

            ex11=x.error_rate,

            leak_ec=1e-8
        )

        print(

            f"d={d:<3}"

            f" EX11={x.error_rate:.4f}"

            f" SKR={r.secret_key_rate:.3e}"
        )