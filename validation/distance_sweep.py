import numpy as np
import matplotlib.pyplot as plt

from adaptive.real_scheduler import RealScheduler
from adaptive.channel_state import ChannelState
from channel.dynamic_fiber_channel import DynamicFiberChannel


RUNS = 100
FRAMES = 500

DISTANCES = [50, 100, 150, 200, 250, 300]

RATE_MAP = {

    2: 500e6,
    4: 250e6,
    8: 125e6,
    16: 62.5e6

}


scheduler = RealScheduler(
    fast_mode=True
)


def throughput(skr, d):

    return (

        skr

        *

        np.log2(d)

        *

        RATE_MAP[d]

        /

        1000

    )


d2_results = []
d4_results = []
d8_results = []
d16_results = []
adaptive_results = []

adaptive_histograms = {}


print()
print("="*80)
print("DISTANCE SWEEP")
print("="*80)


for length_km in DISTANCES:

    print(f"\nDistance = {length_km} km")

    loss_db = 0.2 * length_km

    d2_mc = []
    d4_mc = []
    d8_mc = []
    d16_mc = []
    adaptive_mc = []

    chosen = []

    for run in range(RUNS):

        channel = DynamicFiberChannel(
            length_km=length_km
        )

        t2 = 0
        t4 = 0
        t8 = 0
        t16 = 0
        ta = 0

        for frame in range(FRAMES):

            metrics = channel.step()

            state = ChannelState(

                loss_db=loss_db,

                phase_noise_rad=
                abs(metrics.phase_rad),

                timing_jitter_ps=
                metrics.timing_ps,

                polarization_drift_deg=
                metrics.polarization_deg

            )

            #
            # Fixed
            #

            best_adaptive = -1
            best_dimension = None

            for d in [2,4,8,16]:

                skr = scheduler.evaluate_dimension(
                    d,
                    state
                )

                kbps = throughput(
                    skr,
                    d
                )

                if d == 2:
                    t2 += kbps

                elif d == 4:
                    t4 += kbps

                elif d == 8:
                    t8 += kbps

                else:
                    t16 += kbps

                #
                # Adaptive
                #

                if kbps > best_adaptive:

                    best_adaptive = kbps
                    best_dimension = d

            ta += best_adaptive

            chosen.append(best_dimension)

        d2_mc.append(t2/FRAMES)
        d4_mc.append(t4/FRAMES)
        d8_mc.append(t8/FRAMES)
        d16_mc.append(t16/FRAMES)
        adaptive_mc.append(ta/FRAMES)

    d2_results.append(np.mean(d2_mc))
    d4_results.append(np.mean(d4_mc))
    d8_results.append(np.mean(d8_mc))
    d16_results.append(np.mean(d16_mc))
    adaptive_results.append(np.mean(adaptive_mc))

    adaptive_histograms[length_km] = chosen


print()
print("="*80)
print("FINAL RESULTS")
print("="*80)

print()

print(
    f"{'Distance':<12}"
    f"{'d=2':>10}"
    f"{'d=4':>10}"
    f"{'d=8':>10}"
    f"{'d=16':>10}"
    f"{'Adaptive':>12}"
)

print("-"*64)

for i, dist in enumerate(DISTANCES):

    print(

        f"{dist:<12}"

        f"{d2_results[i]:>10.2f}"

        f"{d4_results[i]:>10.2f}"

        f"{d8_results[i]:>10.2f}"

        f"{d16_results[i]:>10.2f}"

        f"{adaptive_results[i]:>12.2f}"

    )


plt.figure(figsize=(10,6))

plt.plot(
    DISTANCES,
    d2_results,
    marker='o',
    label='d=2'
)

plt.plot(
    DISTANCES,
    d4_results,
    marker='o',
    label='d=4'
)

plt.plot(
    DISTANCES,
    d8_results,
    marker='o',
    label='d=8'
)

plt.plot(
    DISTANCES,
    d16_results,
    marker='o',
    label='d=16'
)

plt.plot(
    DISTANCES,
    adaptive_results,
    marker='o',
    linewidth=3,
    label='Adaptive'
)

plt.xlabel(
    "Fiber Length (km)"
)

plt.ylabel(
    "Throughput (kbps)"
)

plt.title(
    "Distance Sweep"
)

plt.grid(True)

plt.legend()

plt.show()


for dist in DISTANCES:

    plt.figure(figsize=(6,4))

    plt.hist(

        adaptive_histograms[dist],

        bins=[1,3,5,9,17],

        rwidth=0.8

    )

    plt.xticks(
        [2,4,8,16]
    )

    plt.title(
        f"Adaptive Usage ({dist} km)"
    )

    plt.xlabel(
        "Chosen Dimension"
    )

    plt.ylabel(
        "Occurrences"
    )

    plt.grid(True)

    plt.show()