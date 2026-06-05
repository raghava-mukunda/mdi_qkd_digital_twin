"""
adaptive_montecarlo.py

Run adaptive vs fixed many times
with different random seeds.

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

N_EXPERIMENTS = 20

FRAMES_PER_EXPERIMENT = 100

results = []

for seed in range(N_EXPERIMENTS):

    rng = np.random.default_rng(seed)

    scheduler = RealScheduler()

    adaptive_total = 0.0

    fixed = {
        2: 0.0,
        4: 0.0,
        8: 0.0,
        16: 0.0
    }

    for _ in range(FRAMES_PER_EXPERIMENT):

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

        adaptive_total += (
            scores[best]
        )

        for d in [2,4,8,16]:

            fixed[d] += (
                scores[d]
            )

    best_fixed = max(
        fixed.values()
    )

    improvement = (

        adaptive_total

        -

        best_fixed

    ) / best_fixed * 100

    results.append(
        improvement
    )

print()
print("="*80)
print("ADAPTIVE MONTE CARLO")
print("="*80)

print()

for i,val in enumerate(results):

    print(
        f"Run {i+1:02d}: "
        f"{val:.2f}%"
    )

print()
print(
    "Mean Improvement:",
    np.mean(results)
)

print(
    "Std Dev:",
    np.std(results)
)

print(
    "Min:",
    np.min(results)
)

print(
    "Max:",
    np.max(results)
)