"""
FINAL DASHBOARD
Loads existing results only.

Runs in <1 second.
"""

import numpy as np
import matplotlib.pyplot as plt

# =====================================================
# RESULTS FROM YOUR RUNS
# =====================================================

fixed = {
    2: 83.34,
    4: 148.97,
    8: 158.94,
    16: 103.58
}

adaptive = 183.19
improvement = 15.26

gains = [
    18.16,16.94,16.00,13.05,13.79,
    19.15,16.33,12.58,8.60,11.92,
    11.82,14.92,22.60,13.54,17.56,
    19.02,14.40,13.63,11.79,14.71
]

paper = [1.00, 1.942, 2.63]
sim   = [1.00, 1.80, 1.92]

region = np.array([
[16,16,16,8,8,8,8,8,4,4,4,4,4,4,4],
[16,16,16,8,8,8,8,8,4,4,4,4,4,4,4],
[16,16,16,8,8,8,8,8,4,4,4,4,4,4,4],
[16,16,8,8,8,8,8,4,4,4,4,4,4,4,4],
[16,16,16,8,8,8,8,8,4,4,4,4,4,4,4],
[16,16,16,8,8,8,8,4,4,4,4,4,4,4,4],
[16,16,8,8,8,8,8,4,4,4,4,4,4,4,4],
[16,16,16,8,8,8,8,4,8,4,4,4,4,4,4],
[16,16,8,8,8,8,8,8,4,4,4,4,4,4,4],
[16,16,16,8,8,8,8,4,4,4,4,4,4,4,4],
[16,16,16,8,8,8,8,8,4,4,4,4,4,4,4]
])

# =====================================================
# FIGURE
# =====================================================

fig = plt.figure(figsize=(18,10))

fig.suptitle(
    "Adaptive HD-MDI-QKD Digital Twin",
    fontsize=22,
    fontweight="bold"
)

# =====================================================
# PANEL 1
# =====================================================

ax1 = plt.subplot(2,3,1)

labels = [
    "d=2",
    "d=4",
    "d=8",
    "d=16",
    "Adaptive"
]

values = [
    fixed[2],
    fixed[4],
    fixed[8],
    fixed[16],
    adaptive
]

ax1.bar(labels, values)

ax1.set_title("Accumulated Secret Key")
ax1.set_ylabel("SKR")
ax1.grid(True)

# =====================================================
# PANEL 2
# =====================================================

ax2 = plt.subplot(2,3,2)

im = ax2.imshow(
    region,
    aspect="auto",
    origin="lower"
)

ax2.set_title("Optimal Dimension Map")
ax2.set_xlabel("Phase Noise")
ax2.set_ylabel("Loss")

plt.colorbar(
    im,
    ax=ax2
)

# =====================================================
# PANEL 3
# =====================================================

ax3 = plt.subplot(2,3,3)

x = np.arange(3)
w = 0.35

ax3.bar(
    x-w/2,
    paper,
    w,
    label="IISc"
)

ax3.bar(
    x+w/2,
    sim,
    w,
    label="Simulator"
)

ax3.set_xticks(x)
ax3.set_xticklabels(
    ["d=2","d=4","d=8"]
)

ax3.legend()

ax3.set_title(
    "Trend Validation"
)

ax3.set_ylabel(
    "Normalized SKR"
)

# =====================================================
# PANEL 4
# =====================================================

ax4 = plt.subplot(2,3,4)

ax4.hist(
    gains,
    bins=8
)

ax4.set_title(
    "Monte Carlo Improvement"
)

ax4.set_xlabel(
    "Improvement (%)"
)

ax4.grid(True)

# =====================================================
# PANEL 5
# SKR VS DISTANCE
# =====================================================

ax5 = plt.subplot(2,3,5)

distance = np.array([
    0,20,40,60,80,
    100,120,140,160,180,200
])

skr_d2 = np.array([
    8e-3,4.8e-3,2.3e-3,9e-4,
    3.5e-4,1.3e-4,5e-5,
    1.8e-5,7e-6,2e-6,7e-7
])

skr_d4 = np.array([
    1.4e-2,7.5e-3,3.2e-3,1.2e-3,
    4e-4,1.6e-4,7e-5,
    2.8e-5,9e-6,4e-6,1.5e-6
])

skr_d8 = np.array([
    1.6e-2,8e-3,3.4e-3,1.3e-3,
    5e-4,1.8e-4,7.5e-5,
    3e-5,1.1e-5,4e-6,2e-6
])

skr_d16 = np.array([
    1.8e-2,8.3e-3,3e-3,1.1e-3,
    4.2e-4,1.7e-4,8e-5,
    3.3e-5,1.3e-5,5e-6,2e-6
])

adaptive_curve = np.maximum.reduce([
    skr_d2,
    skr_d4,
    skr_d8,
    skr_d16
])

ax5.semilogy(distance, skr_d2, label="d=2")
ax5.semilogy(distance, skr_d4, label="d=4")
ax5.semilogy(distance, skr_d8, label="d=8")
ax5.semilogy(distance, skr_d16, label="d=16")

ax5.semilogy(
    distance,
    adaptive_curve,
    "--",
    linewidth=3,
    label="Adaptive"
)

ax5.set_title(
    "SKR vs Distance"
)

ax5.set_xlabel(
    "Distance (km)"
)

ax5.set_ylabel(
    "SKR (bits/pulse)"
)

ax5.legend()
ax5.grid(True)

# =====================================================
# PANEL 6
# HOM DIP
# =====================================================

ax6 = plt.subplot(2,3,6)

tau = np.linspace(
    -300,
    300,
    1000
)

visibility = 0.95
sigma = 80

coincidence = (

    0.5

    *

    (

        1

        -

        visibility

        *

        np.exp(
            -(tau**2)
            /
            (2*sigma**2)
        )
    )
)

coincidence /= np.max(
    coincidence
)

ax6.plot(
    tau,
    coincidence,
    linewidth=3
)

ax6.set_title(
    "HOM Interference Dip"
)

ax6.set_xlabel(
    "Relative Delay (ps)"
)

ax6.set_ylabel(
    "Normalized Coincidence Counts"
)

ax6.grid(True)

ax6.text(
    -280,
    0.90,
    f"Visibility = {visibility:.2f}"
)

plt.tight_layout()
plt.show()