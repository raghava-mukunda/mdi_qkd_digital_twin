"""
dimension_sweep.py
"""

from skr.secret_key_rate import (
    SecretKeyRate
)

from statistics.x_basis_error import (
    XBasisErrorModel
)

from statistics.q11_model import (
    Q11Model
)

skr = SecretKeyRate()

xerr = XBasisErrorModel()

q11model = Q11Model()

print()
print("="*80)
print("HD-MDI-QKD DIMENSION SWEEP")
print("="*80)

for d in [

    2,
    4,
    8,
    16

]:

    x = xerr.calculate(

        dimension=d,

        visibility=0.995
    )

    q11 = q11model.calculate(
        d
    )

    result = skr.calculate(

        dimension=d,

        q11_z=q11.gain,

        ex11=x.error_rate,

        leak_ec=1e-8
    )

    print()

    print(
        f"d={d}"
    )

    print(
        f"Q11={q11.gain:.3e}"
    )

    print(
        f"EX11={x.error_rate:.5f}"
    )

    print(
        f"SKR={result.secret_key_rate:.3e}"
    )