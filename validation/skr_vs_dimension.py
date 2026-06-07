import numpy as np
import matplotlib.pyplot as plt

from adaptive.channel_state import ChannelState
from adaptive.real_scheduler import RealScheduler

scheduler = RealScheduler()

state = ChannelState(
    loss_db=5,
    phase_noise_rad=0.08,
    timing_jitter_ps=20,
    polarization_drift_deg=2
)

dims = np.array([2,4,8,16])

_, scores = scheduler.choose_dimension(
    state
)

skr = np.array([
    scores[2],
    scores[4],
    scores[8],
    scores[16]
])

# smooth interpolation

xfine = np.linspace(
    2,
    16,
    500
)

coeff = np.polyfit(
    dims,
    skr,
    3
)

yfine = np.polyval(
    coeff,
    xfine
)

plt.figure(figsize=(8,5))

plt.plot(
    xfine,
    yfine,
    linewidth=3,
    label="Interpolated"
)

plt.scatter(
    dims,
    skr,
    s=100
)

plt.xlabel("Dimension d")
plt.ylabel("Secret Key Rate")
plt.title("SKR vs Dimension")
plt.grid(True)

plt.show()