"""
dimension_region_map.py

Optimal Dimension Regions

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
print("OPTIMAL DIMENSION REGION MAP")
print("="*100)

print()

header = "Loss\\Phase".ljust(12)

for p in phase_values:

    header += f"{p:.02f}".rjust(5)

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

        best_d, _ = (

            scheduler.choose_dimension(
                state
            )
        )

        row += str(best_d).rjust(5)

    print(row)