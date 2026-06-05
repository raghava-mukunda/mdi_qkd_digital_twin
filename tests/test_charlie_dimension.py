from bsm.quantum_state import (
    QuantumStateFactory
)

from bsm.charlie_receiver import (
    CharlieReceiver
)

charlie = CharlieReceiver()

for d in [

    2,
    4,
    8,
    16

]:

    a = (
        QuantumStateFactory.create(
            d,
            "X",
            0
        )
    )

    b = (
        QuantumStateFactory.create(
            d,
            "X",
            0
        )
    )

    success = 0

    N = 10000

    for _ in range(N):

        result = (

            charlie.process_trial(
                a,
                b
            )
        )

        if result.psi_minus:

            success += 1

    print()

    print(
        f"d={d}"
    )

    print(
        f"BSM={success/N:.6f}"
    )