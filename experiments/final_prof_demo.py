"""
final_prof_demo.py

ONE-SHOT PROFESSOR DASHBOARD

Shows:

1. Adaptive vs Fixed SKR
2. Dimension Usage
3. Optimal Dimension Map
4. SKR vs Dimension
5. Monte Carlo Improvements
6. Key Results Summary

Author:
MDI-QKD Digital Twin
"""

import numpy as np
import matplotlib.pyplot as plt

from adaptive.channel_state import ChannelState
from adaptive.real_scheduler import RealScheduler

scheduler = RealScheduler()

rng = np.random.default_rng(42)

# =====================================================
# MAIN EXPERIMENT
# =====================================================

N = 1000

adaptive = 0

fixed = {
    2:0,
    4:0,
    8:0,
    16:0
}

usage = {
    2:0,
    4:0,
    8:0,
    16:0
}

for _ in range(N):

    state = ChannelState(

        loss_db=rng.uniform(
            0,
            20
        ),

        phase_noise_rad=rng.uniform(
            0.02,
            0.30
        ),

        timing_jitter_ps=rng.uniform(
            10,
            50
        ),

        polarization_drift_deg=rng.uniform(
            0,
            5
        )
    )

    best, scores = (
        scheduler.choose_dimension(
            state
        )
    )

    adaptive += scores[best]

    usage[best] += 1

    for d in [2,4,8,16]:

        fixed[d] += scores[d]

best_fixed = max(
    fixed.values()
)

improvement = (
    adaptive
    -
    best_fixed
) / best_fixed * 100

# =====================================================
# REGION MAP
# =====================================================

losses = np.linspace(
    0,
    20,
    11
)

phases = np.linspace(
    0.02,
    0.30,
    15
)

region = np.zeros(
    (
        len(losses),
        len(phases)
    )
)

for i, loss in enumerate(losses):

    for j, phase in enumerate(phases):

        state = ChannelState(

            loss_db=float(loss),

            phase_noise_rad=float(phase),

            timing_jitter_ps=20,

            polarization_drift_deg=2
        )

        best, _ = (
            scheduler.choose_dimension(
                state
            )
        )

        region[i,j] = best

# =====================================================
# SKR VS DIMENSION
# =====================================================

test_state = ChannelState(

    loss_db=5,

    phase_noise_rad=0.1,

    timing_jitter_ps=20,

    polarization_drift_deg=2
)

skr_curve = []

for d in [2,4,8,16]:

    skr_curve.append(

        scheduler.evaluate_dimension(
            d,
            test_state
        )
    )

# =====================================================
# MONTE CARLO
# =====================================================

mc = []

for run in range(20):

    adaptive_run = 0

    fixed8 = 0

    local_rng = np.random.default_rng(
        run
    )

    for _ in range(300):

        state = ChannelState(

            loss_db=local_rng.uniform(
                0,
                20
            ),

            phase_noise_rad=local_rng.uniform(
                0.02,
                0.30
            ),

            timing_jitter_ps=local_rng.uniform(
                10,
                50
            ),

            polarization_drift_deg=local_rng.uniform(
                0,
                5
            )
        )

        best, scores = (
            scheduler.choose_dimension(
                state
            )
        )

        adaptive_run += scores[best]

        fixed8 += scores[8]

    gain = (

        adaptive_run
        -
        fixed8

    ) / fixed8 * 100

    mc.append(gain)

# =====================================================
# DASHBOARD
# =====================================================

fig = plt.figure(
    figsize=(16,10)
)

fig.suptitle(
    "Adaptive HD-MDI-QKD Dashboard",
    fontsize=18,
    fontweight="bold"
)

# -------------------------------------------------

ax1 = plt.subplot(
    2,3,1
)

ax1.bar(

    ["d=2","d=4","d=8","d=16","Adaptive"],

    [

        fixed[2],
        fixed[4],
        fixed[8],
        fixed[16],
        adaptive
    ]
)

ax1.set_title(
    "Total SKR"
)

# -------------------------------------------------

ax2 = plt.subplot(
    2,3,2
)

ax2.bar(

    ["2","4","8","16"],

    [

        usage[2],
        usage[4],
        usage[8],
        usage[16]
    ]
)

ax2.set_title(
    "Dimension Usage"
)

# -------------------------------------------------

ax3 = plt.subplot(
    2,3,3
)

im = ax3.imshow(

    region,

    aspect="auto",

    origin="lower"
)

ax3.set_title(
    "Optimal Dimension Map"
)

ax3.set_xlabel(
    "Phase Noise"
)

ax3.set_ylabel(
    "Loss"
)

plt.colorbar(
    im,
    ax=ax3
)

# -------------------------------------------------

ax4 = plt.subplot(
    2,3,4
)

ax4.plot(

    [2,4,8,16],

    skr_curve,

    marker="o"
)

ax4.set_title(
    "SKR vs Dimension"
)

ax4.grid()

# -------------------------------------------------

ax5 = plt.subplot(
    2,3,5
)

ax5.hist(
    mc,
    bins=8
)

ax5.set_title(
    "Monte Carlo Improvement (%)"
)

# -------------------------------------------------

ax6 = plt.subplot(
    2,3,6
)

ax6.axis("off")

summary = f"""

ADAPTIVE RESULT

Adaptive SKR:
{adaptive:.2f}

Best Fixed:
{best_fixed:.2f}

Gain:
{improvement:.2f}%


MONTE CARLO

Mean:
{np.mean(mc):.2f}%

Std:
{np.std(mc):.2f}%


BEST FIXED DIMENSION

d = {max(fixed,key=fixed.get)}

"""

ax6.text(

    0.05,
    0.95,

    summary,

    fontsize=12,

    verticalalignment="top",

    family="monospace"
)

plt.tight_layout()

plt.show()