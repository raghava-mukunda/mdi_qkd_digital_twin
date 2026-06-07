"""
adaptive_gain_heatmap.py

Adaptive Gain Region Map

Shows where adaptive dimension
selection provides significant
benefit over the best fixed d.

Author:
MDI-QKD Digital Twin
"""

import numpy as np
import matplotlib.pyplot as plt

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
    21
)

phase_values = np.linspace(
    0.02,
    0.30,
    29
)

gain_map = np.zeros(
    (
        len(loss_values),
        len(phase_values)
    )
)

total = (
    len(loss_values)
    *
    len(phase_values)
)

counter = 0

print()
print("="*80)
print("ADAPTIVE GAIN HEATMAP")
print("="*80)

for i, loss in enumerate(loss_values):

    for j, phase in enumerate(phase_values):

        state = ChannelState(

            loss_db=float(loss),

            phase_noise_rad=float(phase),

            timing_jitter_ps=20,

            polarization_drift_deg=2

        )

        #
        # Average several evaluations
        # to reduce Monte-Carlo noise
        #

        adaptive = 0

        fixed = {
            2:0,
            4:0,
            8:0,
            16:0
        }

        N = 10

        for _ in range(N):

            best, scores = (
                scheduler.choose_dimension(
                    state
                )
            )

            adaptive += (

                scores[best]

                *

                np.log2(best)

            )

            for d in fixed:

                fixed[d] += (

                    scores[d]

                    *

                    np.log2(d)

                )

        adaptive /= N

        for d in fixed:

            fixed[d] /= N

        best_fixed = max(
            fixed.values()
        )

        gain = (

            adaptive

            -

            best_fixed

        ) / best_fixed * 100

        gain_map[i,j] = gain

        counter += 1

        if counter % 50 == 0:

            print(
                f"Progress: "
                f"{counter}/{total}"
            )

print()
print("Finished Calculations")

plt.figure(
    figsize=(10,7)
)

im = plt.imshow(

    gain_map,

    origin="lower",

    aspect="auto",

    extent=[

        phase_values[0],
        phase_values[-1],

        loss_values[0],
        loss_values[-1]

    ]

)

plt.colorbar(
    label="Adaptive Gain (%)"
)

plt.xlabel(
    "Phase Noise (rad)"
)

plt.ylabel(
    "Channel Loss (dB)"
)

plt.title(
    "Adaptive Dimension Selection Gain"
)

#
# Draw 10% contour
#

contours = plt.contour(

    phase_values,

    loss_values,

    gain_map,

    levels=[10],

    linewidths=2

)

plt.clabel(
    contours,
    inline=True,
    fontsize=10
)

plt.tight_layout()

plt.savefig(

    "adaptive_gain_heatmap.png",

    dpi=300

)

plt.show()