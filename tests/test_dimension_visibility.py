from bsm.quantum_state import (
    QuantumStateFactory
)

from interference.beam_splitter import (
    BeamSplitter
)

bs = BeamSplitter()

print()
print("="*70)
print("DIMENSION DEPENDENT HOM VISIBILITY")
print("="*70)

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

    result = (
        bs.interfere(
            a,
            b
        )
    )

    print()

    print(
        f"d={d}"
    )

    print(
        f"Vcoh={result.coherence_visibility:.6f}"
    )

    print(
        f"Vtotal={result.total_visibility:.6f}"
    )