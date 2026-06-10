"""
hom_recovery_demo.py

Visibility before and after compensation.
"""

import numpy as np
import matplotlib.pyplot as plt

from bsm.quantum_state import (
    QuantumStateFactory
)

from interference.beam_splitter import (
    BeamSplitter
)

from channel.dynamic_fiber_channel import (
    DynamicFiberChannel
)

from control.perfect_compensator import (
    PerfectCompensator
)

N = 500

bs = BeamSplitter()

channel = DynamicFiberChannel(
    length_km=100
)

comp = PerfectCompensator()

alice = QuantumStateFactory.create(
    8,
    "X",
    0
)

bob = QuantumStateFactory.create(
    8,
    "X",
    0
)

before = []
after = []

print()
print("="*80)
print("HOM RECOVERY DEMO")
print("="*80)

for i in range(N):

    metrics = channel.step()

    hom1 = bs.interfere(

        alice,
        bob,

        timing_offset_ps=
        metrics.timing_ps,

        phase_offset_rad=
        metrics.phase_rad,

        polarization_offset_deg=
        metrics.polarization_deg
    )

    corr = comp.compensate(
        metrics
    )

    hom2 = bs.interfere(

        alice,
        bob,

        timing_offset_ps=(
            metrics.timing_ps
            +
            corr.timing_ps
        ),

        phase_offset_rad=(
            metrics.phase_rad
            +
            corr.phase_rad
        ),

        polarization_offset_deg=(
            metrics.polarization_deg
            +
            corr.polarization_deg
        )
    )

    before.append(
        hom1.total_visibility
    )

    after.append(
        hom2.total_visibility
    )

    if (i+1) % 50 == 0:

        print(
            f"{i+1}/{N}"
        )

plt.figure(figsize=(10,6))

plt.plot(
    before,
    label="Without compensation"
)

plt.plot(
    after,
    label="Oracle compensation"
)

plt.xlabel(
    "Frame"
)

plt.ylabel(
    "HOM Visibility"
)

plt.title(
    "HOM Recovery Using Predictive Compensation"
)

plt.grid(True)

plt.legend()

plt.show()

print()

print(
    "Mean Visibility Before:",
    np.mean(before)
)

print(
    "Mean Visibility After:",
    np.mean(after)
)