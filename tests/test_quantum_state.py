from bsm.quantum_state import (
    QuantumStateFactory
)

#
# Same state
#

a = (
    QuantumStateFactory.create(
        8,
        "X",
        0
    )
)

b = (
    QuantumStateFactory.create(
        8,
        "X",
        0
    )
)

print()

print(
    "f0 vs f0:",
    a.overlap(b)
)

#
# Orthogonal
#

c = (
    QuantumStateFactory.create(
        8,
        "X",
        1
    )
)

print(
    "f0 vs f1:",
    a.overlap(c)
)

#
# Z basis
#

d = (
    QuantumStateFactory.create(
        8,
        "Z",
        3
    )
)

e = (
    QuantumStateFactory.create(
        8,
        "Z",
        3
    )
)

f = (
    QuantumStateFactory.create(
        8,
        "Z",
        4
    )
)

print(
    "t3 vs t3:",
    d.overlap(e)
)

print(
    "t3 vs t4:",
    d.overlap(f)
)