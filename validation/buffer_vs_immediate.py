"""
buffer_vs_immediate.py

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

from adaptive.fpga_buffer import (
    FPGABuffer
)

rng = np.random.default_rng(42)

scheduler = RealScheduler()

buffer = FPGABuffer()

immediate_skr = 0

N = 200

for t in range(N):

    state = ChannelState(

        loss_db=rng.uniform(
            0,
            20
        ),

        phase_noise_rad=rng.uniform(
            0.02,
            0.30
        ),

        timing_jitter_ps=20,

        polarization_drift_deg=2
    )

    #
    # Immediate transmission
    #

    d, results = (

        scheduler.choose_dimension(
            state
        )
    )

    immediate_skr += (
        results[d]
    )

    #
    # Buffer transmission
    #

    buffer.enqueue(
        state,
        t
    )

    if t % 5 == 0:

        buffer.transmit_best(
            t
        )

metrics = (
    buffer.metrics()
)

print()
print("="*80)
print("BUFFER VS IMMEDIATE")
print("="*80)

print()

print(
    "Immediate SKR:",
    immediate_skr
)

print(
    "Buffered SKR:",
    metrics.total_skr
)

print(
    "Average Delay:",
    metrics.average_delay
)

print(
    "Dropped:",
    metrics.dropped_frames
)