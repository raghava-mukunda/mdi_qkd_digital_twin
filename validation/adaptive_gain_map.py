"""
adaptive_gain_map.py

Adaptive HD-MDI-QKD Gain Map

Shows where adaptive dimension
selection outperforms fixed d.

Author:
MDI-QKD Digital Twin
"""

import numpy as np

from adaptive.channel_state import (
    ChannelState
)

from adaptive.real_scheduler import (
    RealScheduler
)

scheduler = RealScheduler()

loss_values = np.linspace(
    0,
    20,
    11
)

phase_values = np.linspace(
    0.02,
    0.30,
    15
)

print()
print("="*100)
print("ADAPTIVE GAIN MAP")
print("="*100)

print()

header = "Loss\\Phase".ljust(12)

for p in phase_values:

    header += f"{p:.02f}".rjust(8)

print(header)

for loss in loss_values:

    row = f"{loss:.1f}".ljust(12)

    for phase in phase_values:

        state = ChannelState(

            loss_db=float(loss),

            phase_noise_rad=float(phase),

            timing_jitter_ps=20,

            polarization_drift_deg=2
        )

        best_d, results = (

            scheduler.choose_dimension(
                state
            )
        )

        adaptive = results[best_d]

        fixed_best = max(
            results.values()
        )

        gain = (

            adaptive
            /
            fixed_best
        )

        row += f"{gain:.2f}".rjust(8)

    print(row)