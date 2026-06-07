import numpy as np
import matplotlib.pyplot as plt

from adaptive.channel_state import ChannelState
from adaptive.real_scheduler import RealScheduler

scheduler = RealScheduler()

distances = np.arange(
    0,
    101,
    2
)

skr_values = []

for distance in distances:

    loss = distance * 0.2

    state = ChannelState(
        loss_db=loss,
        phase_noise_rad=0.08,
        timing_jitter_ps=20,
        polarization_drift_deg=2
    )

    best, scores = scheduler.choose_dimension(
        state
    )

    skr_values.append(
        scores[best]
    )

plt.figure(figsize=(8,5))

plt.semilogy(
    distances,
    skr_values,
    linewidth=3
)

plt.xlabel("Distance (km)")
plt.ylabel("SKR")
plt.title("Adaptive SKR vs Distance")
plt.grid(True)

plt.show()