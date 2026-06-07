import numpy as np
import matplotlib.pyplot as plt

from adaptive.channel_state import ChannelState
from adaptive.real_scheduler import RealScheduler

scheduler = RealScheduler()

distances = np.arange(
    0,
    201,
    10
)

fiber_loss_db_per_km = 0.2

curves = {
    2: [],
    4: [],
    8: [],
    16: []
}

adaptive = []

for distance in distances:

    loss = distance * fiber_loss_db_per_km

    state = ChannelState(
        loss_db=loss,
        phase_noise_rad=0.08,
        timing_jitter_ps=20,
        polarization_drift_deg=2
    )

    best, results = scheduler.choose_dimension(
        state
    )

    adaptive.append(
        results[best]
    )

    for d in [2,4,8,16]:

        curves[d].append(
            results[d]
        )

plt.figure(figsize=(10,6))

for d in [2,4,8,16]:

    plt.semilogy(
        distances,
        curves[d],
        label=f"d={d}"
    )

plt.semilogy(
    distances,
    adaptive,
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
    "HD-MDI-QKD SKR vs Distance"
)

plt.grid(True)

plt.legend()

plt.show()
plt.tight_layout()

plt.savefig(
    "validation/fig2_skr_vs_distance.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()