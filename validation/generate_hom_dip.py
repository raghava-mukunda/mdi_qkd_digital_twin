"""
generate_hom_dip.py

Generate HOM dip from BeamSplitter model.

Author:
MDI-QKD Digital Twin
"""

import numpy as np
import matplotlib.pyplot as plt

from bsm.quantum_state import (
    QuantumStateFactory
)

from interference.beam_splitter import (
    BeamSplitter
)

# =====================================================
# Setup
# =====================================================

beam_splitter = BeamSplitter()

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

# =====================================================
# Delay Sweep
# =====================================================

delays = np.linspace(
    -2500,
    2500,
    801
)

coincidences = []

for delay in delays:

    hom = beam_splitter.interfere(

        alice,

        bob,

        timing_offset_ps=float(delay),

        phase_offset_rad=0.0,

        polarization_offset_deg=0.0

    )

    coincidences.append(
        hom.coincidence_probability
    )

coincidences = np.array(
    coincidences
)

# =====================================================
# Experimental normalization
# =====================================================

baseline = np.mean(
    coincidences[-50:]
)

coincidences = (
    coincidences
    /
    baseline
)

# =====================================================
# Visibility
# =====================================================

c_max = np.max(
    coincidences
)

c_min = np.min(
    coincidences
)

visibility = (

    c_max
    -
    c_min

) / c_max

print()
print("=" * 60)
print("HOM VISIBILITY")
print("=" * 60)
print()

print(
    f"Visibility = {visibility:.3f}"
)

print(
    f"Min Coincidence = {c_min:.3f}"
)

print(
    f"Max Coincidence = {c_max:.3f}"
)

# =====================================================
# Save
# =====================================================

np.savez(

    "validation/hom_dip.npz",

    delays=delays,

    coincidences=coincidences,

    visibility=visibility
)

# =====================================================
# Plot
# =====================================================

plt.figure(figsize=(8,5))

plt.plot(

    delays / 1000,

    coincidences,

    linewidth=3

)

plt.title(
    f"Simulated HOM Dip (V={visibility:.2f})"
)

plt.xlabel(
    "Time Delay (ns)"
)

plt.ylabel(
    "Normalized Coincidence Counts"
)

plt.grid(True)

plt.tight_layout()

plt.show()
plt.tight_layout()

plt.savefig(
    "validation/fig1_hom_dip.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()