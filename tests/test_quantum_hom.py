from bsm.quantum_state import (
    QuantumStateFactory
)

from interference.beam_splitter import (
    BeamSplitter
)

bs = BeamSplitter()

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

m1 = bs.interfere(
    a,
    b
)

print()
print("f0 vs f0")
print(m1)

#
# orthogonal states
#

c = QuantumStateFactory.create(
    8,
    "X",
    1
)

m2 = bs.interfere(
    a,
    c
)

print()
print("f0 vs f1")
print(m2)

#
# z basis mismatch
#

d = QuantumStateFactory.create(
    8,
    "Z",
    2
)

e = QuantumStateFactory.create(
    8,
    "Z",
    6
)

m3 = bs.interfere(
    d,
    e
)

print()
print("t2 vs t6")
print(m3)