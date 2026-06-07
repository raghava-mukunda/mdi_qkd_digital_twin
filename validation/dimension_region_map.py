"""
dimension_region_map.py

Smoothed Optimal Dimension Map

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

N_AVERAGES = 10

print()
print("=" * 100)
print("OPTIMAL DIMENSION REGION MAP")
print("=" * 100)
print()

header = "Loss\\Phase".ljust(12)

for p in phase_values:

    header += f"{p:.02f}".rjust(5)

print(header)

total_points = (
    len(loss_values)
    *
    len(phase_values)
)

counter = 0

for loss in loss_values:

    row = f"{loss:.1f}".ljust(12)

    for phase in phase_values:

        counter += 1

        print(
            f"\rProgress: "
            f"{counter}/{total_points}",
            end=""
        )

        state = ChannelState(

            loss_db=float(loss),

            phase_noise_rad=float(phase),

            timing_jitter_ps=20,

            polarization_drift_deg=2

        )

        avg_scores = {

            2: 0.0,
            4: 0.0,
            8: 0.0,
            16: 0.0

        }

        for _ in range(N_AVERAGES):

            scheduler = RealScheduler()

            _, scores = (

                scheduler.choose_dimension(
                    state
                )

            )

            for d in avg_scores:

                avg_scores[d] += (
                    scores[d]
                )

        for d in avg_scores:

            avg_scores[d] /= (
                N_AVERAGES
            )

        best_d = max(

            avg_scores,

            key=avg_scores.get

        )

        row += str(best_d).rjust(5)

    print()
    print(row)

print()
print()
print("Finished.")