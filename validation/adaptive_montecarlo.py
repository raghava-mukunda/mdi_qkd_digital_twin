"""
adaptive_montecarlo.py

Adaptive vs Fixed Dimension Study

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

results_oracle = []

results_d8 = []

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

        #
        # Balanced sampling
        #
        # d=16 region
        # d=8 region
        # d=4 region
        #

        mode = rng.integers(
            0,
            3
        )

        if mode == 0:

            loss = rng.uniform(
                0,
                4
            )

            phase = rng.uniform(
                0.02,
                0.08
            )

        elif mode == 1:

            loss = rng.uniform(
                6,
                12
            )

            phase = rng.uniform(
                0.06,
                0.12
            )

        else:

            loss = rng.uniform(
                14,
                20
            )

            phase = rng.uniform(
                0.18,
                0.30
            )

        state = ChannelState(

            loss_db=loss,

            phase_noise_rad=phase,

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

        #
        # Effective secret bits
        #
        # SKR × bits per symbol
        #

        adaptive_total += (

            scores[best]

            *

            np.log2(best)

        )

        for d in [2,4,8,16]:

            fixed[d] += (

                scores[d]

                *

                np.log2(d)

            )

    #
    # Oracle baseline
    #

    oracle_fixed = max(
        fixed.values()
    )

    gain_vs_oracle = (

        adaptive_total

        -

        oracle_fixed

    ) / oracle_fixed * 100

    results_oracle.append(
        gain_vs_oracle
    )

    #
    # Practical deployment baseline
    #
    # Fixed d = 8
    #

    fixed_d8 = fixed[8]

    gain_vs_d8 = (

        adaptive_total

        -

        fixed_d8

    ) / fixed_d8 * 100

    results_d8.append(
        gain_vs_d8
    )

print()
print("="*80)
print("ADAPTIVE vs BEST FIXED")
print("="*80)
print()

for i,val in enumerate(results_oracle):

    print(
        f"Run {i+1:02d}: "
        f"{val:.2f}%"
    )

print()

print(
    "Mean Improvement:",
    np.mean(results_oracle)
)

print(
    "Std Dev:",
    np.std(results_oracle)
)

print(
    "Min:",
    np.min(results_oracle)
)

print(
    "Max:",
    np.max(results_oracle)
)

print()
print("="*80)
print("ADAPTIVE vs FIXED d=8")
print("="*80)
print()

for i,val in enumerate(results_d8):

    print(
        f"Run {i+1:02d}: "
        f"{val:.2f}%"
    )

print()

print(
    "Mean Improvement:",
    np.mean(results_d8)
)

print(
    "Std Dev:",
    np.std(results_d8)
)

print(
    "Min:",
    np.min(results_d8)
)

print(
    "Max:",
    np.max(results_d8)
)

print()
print("="*80)
print("REFERENCE")
print("="*80)

print()

print(
    "Adaptive Total:",
    adaptive_total
)

print(
    "Fixed d=2:",
    fixed[2]
)

print(
    "Fixed d=4:",
    fixed[4]
)

print(
    "Fixed d=8:",
    fixed[8]
)

print(
    "Fixed d=16:",
    fixed[16]
)

print(
    "Best Fixed:",
    oracle_fixed
)