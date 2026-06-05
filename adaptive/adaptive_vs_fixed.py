"""
adaptive_vs_fixed.py

Main Experiment

Compare:

Fixed d=2
Fixed d=4
Fixed d=8
Fixed d=16

vs

Adaptive Dimension Selection
"""

import numpy as np

from adaptive.channel_state import (
    ChannelState
)

from adaptive.adaptive_scheduler import (
    AdaptiveScheduler
)

scheduler = AdaptiveScheduler()

N = 10000

adaptive_total = 0

fixed = {

    2: 0,
    4: 0,
    8: 0,
    16: 0
}

selection_counts = {

    2: 0,
    4: 0,
    8: 0,
    16: 0
}

rng = np.random.default_rng(42)

for _ in range(N):

    state = ChannelState(

        loss_db=rng.uniform(
            0,
            20
        ),

        phase_noise_rad=rng.uniform(
            0.02,
            0.20
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

    decision = (

        scheduler.choose_dimension(
            state
        )
    )

    adaptive_total += (
        decision.predicted_skr
    )

    selection_counts[
        decision.selected_dimension
    ] += 1

    for d in [

        2,
        4,
        8,
        16

    ]:

        fixed[d] += (

            scheduler.evaluate_dimension(
                d,
                state
            )
        )

print()
print("="*80)
print("ADAPTIVE HD-MDI-QKD")
print("="*80)

print()

print(
    "Adaptive Total SKR:",
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

print()
print("Dimension Usage")

for d in [

    2,
    4,
    8,
    16

]:

    print(
        f"d={d}:",
        selection_counts[d]
    )

print()
print("="*80)

best_fixed = max(
    fixed.values()
)

improvement = (

    adaptive_total

    -

    best_fixed

) / best_fixed * 100

print(
    f"Improvement = "
    f"{improvement:.2f}%"
)