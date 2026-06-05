from bsm.quantum_state import (
    QuantumStateFactory
)

from bsm.charlie_receiver import (
    CharlieReceiver
)

charlie = CharlieReceiver()

N = 10000

#
# identical states
#

a = QuantumStateFactory.create(
    8,
    "X",
    0
)

b = QuantumStateFactory.create(
    8,
    "X",
    0
)

success = 0

for _ in range(N):

    result = charlie.process_trial(

        a,

        b
    )

    if result.psi_minus:

        success += 1

print()
print(
    "f0 vs f0"
)

print(
    "BSM Success:",
    success/N
)

#
# orthogonal states
#

c = QuantumStateFactory.create(
    8,
    "X",
    1
)

success = 0

for _ in range(N):

    result = charlie.process_trial(

        a,

        c
    )

    if result.psi_minus:

        success += 1

print()
print(
    "f0 vs f1"
)

print(
    "BSM Success:",
    success/N
)