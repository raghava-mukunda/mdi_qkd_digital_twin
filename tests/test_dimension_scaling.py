from bsm.quantum_state import (
    QuantumStateFactory
)

from bsm.charlie_receiver import (
    CharlieReceiver
)

charlie = CharlieReceiver()

N = 10000

for d in [2,4,8,16]:

    alice = (
        QuantumStateFactory.create(
            d,
            "X",
            0
        )
    )

    bob = (
        QuantumStateFactory.create(
            d,
            "X",
            0
        )
    )

    success = 0

    for _ in range(N):

        result = charlie.process_trial(
            alice,
            bob
        )

        if result.psi_minus:
            success += 1

    print()

    print(
        f"d = {d}"
    )

    print(
        f"BSM Success = {success/N:.4f}"
    )