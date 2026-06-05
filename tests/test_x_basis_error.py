from statistics.x_basis_error import (
    XBasisErrorModel
)

model = XBasisErrorModel()

print()
print("="*70)
print("X BASIS ERROR SCALING")
print("="*70)

for d in [

    2,
    4,
    8,
    16

]:

    result = model.calculate(

        dimension=d,

        visibility=0.995
    )

    print()

    print(
        f"d={d}"
    )

    print(
        f"Visibility={result.phase_visibility:.6f}"
    )

    print(
        f"EX11={result.error_rate:.6f}"
    )