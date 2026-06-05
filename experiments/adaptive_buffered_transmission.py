"""
adaptive_buffered_transmission.py

FPGA Buffer + Adaptive HD-MDI-QKD

Research Question:

Does buffering packets before transmission
allow adaptive dimension selection to
increase total secret key throughput?

Author:
MDI-QKD Digital Twin
"""

from collections import deque
import numpy as np
import matplotlib.pyplot as plt

from adaptive.channel_state import (
    ChannelState
)

from adaptive.real_scheduler import (
    RealScheduler
)


BUFFER_SIZE = 50

MAX_DELAY = 20

N_FRAMES = 500

scheduler = RealScheduler()

rng = np.random.default_rng(42)

buffer = deque()

adaptive_skr = 0.0

immediate_skr = 0.0

fixed8_skr = 0.0

drops = 0

total_delay = 0

transmitted = 0

adaptive_history = []

immediate_history = []

fixed_history = []

buffer_history = []

dimension_history = []


def random_channel():

    return ChannelState(

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


for frame in range(N_FRAMES):

    #
    # New packet arrives
    #

    packet = {

        "arrival": frame,

        "payload": 1
    }

    if len(buffer) < BUFFER_SIZE:

        buffer.append(packet)

    else:

        drops += 1

    #
    # Current channel
    #

    current_state = random_channel()

    #
    # Immediate adaptive baseline
    #

    best_now, scores_now = (

        scheduler.choose_dimension(
            current_state
        )
    )

    immediate_skr += (
        scores_now[best_now]
    )

    #
    # Fixed d=8 baseline
    #

    fixed8_skr += (
        scores_now[8]
    )

    #
    # Buffered adaptive
    #

    if len(buffer) > 0:

        best_packet = None

        best_metric = -1

        best_dimension = None

        best_scores = None

        #
        # Search queue
        #

        for pkt in buffer:

            age = (

                frame
                -
                pkt["arrival"]
            )

            if age > MAX_DELAY:

                continue

            best_d, scores = (

                scheduler.choose_dimension(
                    current_state
                )
            )

            metric = scores[best_d]

            if metric > best_metric:

                best_metric = metric

                best_packet = pkt

                best_dimension = best_d

                best_scores = scores

        if best_packet is not None:

            buffer.remove(
                best_packet
            )

            adaptive_skr += (
                best_metric
            )

            dimension_history.append(
                best_dimension
            )

            delay = (

                frame
                -
                best_packet["arrival"]
            )

            total_delay += delay

            transmitted += 1

    adaptive_history.append(
        adaptive_skr
    )

    immediate_history.append(
        immediate_skr
    )

    fixed_history.append(
        fixed8_skr
    )

    buffer_history.append(
        len(buffer)
    )


avg_delay = (

    total_delay
    /
    transmitted

    if transmitted > 0

    else 0
)

#
# Results
#

print()
print("="*80)
print("BUFFERED ADAPTIVE HD-MDI-QKD")
print("="*80)

print()

print(
    "Buffered Adaptive:",
    adaptive_skr
)

print(
    "Immediate Adaptive:",
    immediate_skr
)

print(
    "Fixed d=8:",
    fixed8_skr
)

print()

print(
    "Packets Transmitted:",
    transmitted
)

print(
    "Packets Dropped:",
    drops
)

print(
    "Average Delay:",
    avg_delay
)

print()

print(
    "Buffered Gain vs Fixed (%):",
    (
        adaptive_skr
        -
        fixed8_skr
    )
    /
    fixed8_skr
    *
    100
)

print(
    "Buffered Gain vs Immediate (%):",
    (
        adaptive_skr
        -
        immediate_skr
    )
    /
    immediate_skr
    *
    100
)

#
# Figure 1
#

plt.figure(figsize=(12,4))

plt.plot(
    adaptive_history,
    label="Buffered Adaptive"
)

plt.plot(
    immediate_history,
    label="Immediate Adaptive"
)

plt.plot(
    fixed_history,
    label="Fixed d=8"
)

plt.legend()

plt.title(
    "Accumulated Secret Key"
)

plt.grid()

#
# Figure 2
#

plt.figure(figsize=(12,4))

plt.plot(
    buffer_history
)

plt.title(
    "Buffer Occupancy"
)

plt.xlabel(
    "Frame"
)

plt.ylabel(
    "Packets"
)

plt.grid()

#
# Figure 3
#

plt.figure(figsize=(12,4))

plt.plot(
    dimension_history
)

plt.title(
    "Selected Dimension"
)

plt.xlabel(
    "Transmission"
)

plt.ylabel(
    "Dimension"
)

plt.grid()

plt.show()