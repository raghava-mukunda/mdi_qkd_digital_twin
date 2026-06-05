"""
adaptive_transmission.py

1000-frame transmission experiment

Uses actual scheduler physics.

Author:
MDI-QKD Digital Twin
"""

import numpy as np
import matplotlib.pyplot as plt

from adaptive.channel_state import ChannelState
from adaptive.real_scheduler import RealScheduler

N_FRAMES = 1000

scheduler = RealScheduler()

rng = np.random.default_rng(42)

adaptive_total = 0.0

fixed = {
    2: 0.0,
    4: 0.0,
    8: 0.0,
    16: 0.0
}

selected_dimensions = []

adaptive_history = []

fixed_histories = {
    2: [],
    4: [],
    8: [],
    16: []
}

for frame in range(N_FRAMES):

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

    selected_dimensions.append(
        best
    )

    adaptive_total += (
        scores[best]
    )

    adaptive_history.append(
        adaptive_total
    )

    for d in [2,4,8,16]:

        fixed[d] += (
            scores[d]
        )

        fixed_histories[d].append(
            fixed[d]
        )

print()
print("="*80)
print("ADAPTIVE TRANSMISSION")
print("="*80)

print()

print(
    "Adaptive:",
    adaptive_total
)

for d in [2,4,8,16]:

    print(
        f"Fixed d={d}:",
        fixed[d]
    )

best_fixed = max(
    fixed.values()
)

improvement = (

    adaptive_total

    -

    best_fixed

) / best_fixed * 100

print()
print(
    "Improvement (%):",
    improvement
)

#
# Figure 1
#

plt.figure(figsize=(12,4))

plt.plot(
    selected_dimensions
)

plt.title(
    "Selected Dimension vs Frame"
)

plt.xlabel(
    "Frame"
)

plt.ylabel(
    "Dimension"
)

plt.grid()

#
# Figure 2
#

plt.figure(figsize=(12,4))

plt.plot(
    adaptive_history,
    label="Adaptive"
)

for d in [2,4,8,16]:

    plt.plot(
        fixed_histories[d],
        label=f"d={d}"
    )

plt.title(
    "Accumulated SKR"
)

plt.xlabel(
    "Frame"
)

plt.ylabel(
    "SKR"
)

plt.legend()

plt.grid()

#
# Figure 3
#

plt.figure(figsize=(8,4))

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
    adaptive_total
]

plt.bar(
    labels,
    values
)

plt.title(
    "Final Throughput"
)

plt.ylabel(
    "Accumulated SKR"
)

plt.grid()

plt.show()