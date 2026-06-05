"""
adaptive_vs_fixed_real.py

Real Digital Twin Comparison

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

scheduler = RealScheduler()

rng = np.random.default_rng(42)

N = 100

adaptive_total = 0.0

fixed = {

    2: 0.0,
    4: 0.0,
    8: 0.0,
    16: 0.0
}

usage = {

    2: 0,
    4: 0,
    8: 0,
    16: 0
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

    best, results = (

        scheduler.choose_dimension(
            state
        )
    )

    adaptive_total += (
        results[best]
    )

    usage[best] += 1

    for d in [

        2,
        4,
        8,
        16

    ]:

        fixed[d] += (
            results[d]
        )

print()
print("="*80)
print("REAL DIGITAL TWIN")
print("="*80)

print()

print(
    "Adaptive:",
    adaptive_total
)

print()

for d in [

    2,
    4,
    8,
    16

]:

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

print()
print("Dimension Usage")

for d in [

    2,
    4,
    8,
    16

]:

    print(
        d,
        usage[d]
    )