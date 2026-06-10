import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

from adaptive.channel_state import ChannelState
from adaptive.joint_scheduler import JointScheduler

scheduler = JointScheduler()

state = ChannelState(
    loss_db=5,
    phase_noise_rad=0.08,
    timing_jitter_ps=20,
    polarization_drift_deg=2
)

best, results = scheduler.choose_mode(state)

# ==========================================
# Extract modes
# ==========================================

x = []
y = []
z = []

labels = []

for mode, throughput in results.items():

    x.append(mode.dimension)

    y.append(mode.frequency_hz / 1e6)

    z.append(throughput)

    labels.append(
        f"d={mode.dimension}\n{mode.frequency_hz/1e6:.0f}MHz"
    )

x = np.array(x)
y = np.array(y)
z = np.array(z)

# ==========================================
# Plot
# ==========================================

fig = plt.figure(figsize=(12,8))

ax = fig.add_subplot(
    111,
    projection='3d'
)

dx = np.ones_like(x) * 0.8
dy = np.ones_like(y) * 25
dz = z

colors = []

for value in z:

    if value == np.max(z):
        colors.append("red")
    else:
        colors.append("steelblue")

ax.bar3d(
    x,
    y,
    np.zeros_like(z),
    dx,
    dy,
    dz,
    color=colors,
    shade=True
)

# ==========================================
# Labels
# ==========================================

ax.set_xlabel("Dimension (d)")
ax.set_ylabel("Clock Frequency (MHz)")
ax.set_zlabel("Secure Throughput (bits/s)")

ax.set_title(
    "HD-MDI-QKD Throughput Operating Modes"
)

ax.set_xticks([2,4,8,16])
ax.set_yticks([125,250,500])

# ==========================================
# Annotate bars
# ==========================================

for xi, yi, zi in zip(x, y, z):

    ax.text(
        xi,
        yi,
        zi + 2000,
        f"{zi/1e3:.1f}k",
        ha='center'
    )

plt.tight_layout()
plt.show()

# ==========================================
# Summary
# ==========================================

print("\nBEST MODE")

print(
    f"d = {best.dimension}"
)

print(
    f"Frequency = {best.frequency_hz/1e6:.0f} MHz"
)

print(
    f"Throughput = {results[best]:.3e} bits/s"
)