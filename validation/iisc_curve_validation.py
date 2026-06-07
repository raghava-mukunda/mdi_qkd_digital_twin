"""
iisc_curve_validation.py

HD-MDI-QKD Validation

Generates:

SKR vs Distance

for

d = 2
d = 4
d = 8
d = 16

similar to IISc Figure 6

Author:
MDI-QKD Digital Twin
"""

import numpy as np
import matplotlib.pyplot as plt

from adaptive.channel_state import ChannelState
from adaptive.real_scheduler import RealScheduler


scheduler = RealScheduler()

distances = np.arange(
    0,
    201,
    5
)

dimensions = [2,4,8,16]

curves = {

    2: [],
    4: [],
    8: [],
    16: []

}

adaptive_curve = []

for distance in distances:

    loss_db = 0.2 * distance

    state = ChannelState(

        loss_db=loss_db,

        phase_noise_rad=0.10,

        timing_jitter_ps=20,

        polarization_drift_deg=2

    )

    best, results = (
        scheduler.choose_dimension(
            state
        )
    )

    adaptive_curve.append(
        results[best]
    )

    for d in dimensions:

        curves[d].append(
            results[d]
        )

plt.figure(figsize=(10,6))

for d in dimensions:

    plt.semilogy(

        distances,

        curves[d],

        linewidth=2,

        label=f"d={d}"

    )

plt.semilogy(

    distances,

    adaptive_curve,

    "--",

    linewidth=3,

    label="Adaptive"

)

plt.xlabel(
    "Distance (km)"
)

plt.ylabel(
    "SKR (bits/pulse)"
)

plt.title(
    "HD-MDI-QKD Validation"
)

plt.grid(True, which="both")

plt.legend()

plt.show()