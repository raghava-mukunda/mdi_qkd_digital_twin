import numpy as np
import matplotlib.pyplot as plt

from channel.dynamic_fiber_channel import (
    DynamicFiberChannel
)

from adaptive.channel_state import (
    ChannelState
)

from adaptive.real_scheduler import (
    RealScheduler
)

RUNS = 1000
FRAMES = 1000

LENGTH_KM = 100

LOSS_DB = 20

BASELINE_KBPS = 25.317
def throughput_kbps(
    skr_per_pulse,
    d,
    rate_hz
):

    return (

        skr_per_pulse

        *

        np.log2(d)

        *

        rate_hz

        /

        1000.0

    )


RATE_MAP = {

    2: 500e6,
    4: 250e6,
    8: 125e6,
    16: 62.5e6

}
scheduler = RealScheduler(
    fast_mode=True
)

adaptive_results = []

adaptive_availability = []

chosen_dimensions = []

print()
print("="*80)
print("ADAPTIVE DIMENSION MONTE CARLO")
print("="*80)

for run in range(RUNS):

    if (run+1)%50 == 0:

        print(
            f"{run+1}/{RUNS}"
        )

    channel = DynamicFiberChannel(
        length_km=LENGTH_KM
    )

    total = 0

    available = 0

    dims = []

    for frame in range(FRAMES):

        metrics = channel.step()

        state = ChannelState(

            loss_db=LOSS_DB,

            phase_noise_rad=
            abs(metrics.phase_rad),

            timing_jitter_ps=
            metrics.timing_ps,

            polarization_drift_deg=
            metrics.polarization_deg

        )

        best_d = None
        best_kbps = -1

        for d in [2,4,8,16]:

            skr = scheduler.evaluate_dimension(

                d,

                state

            )

            kbps = throughput_kbps(

                skr,

                d,

                RATE_MAP[d]

            )

            if kbps > best_kbps:

                best_kbps = kbps
                best_d = d

        total += best_kbps

        dims.append(best_d)

        if best_kbps > 0:

            available += 1

    adaptive_results.append(

        total / FRAMES

    )

    adaptive_availability.append(

        available / FRAMES

    )

    chosen_dimensions.extend(
        dims
    )
mean = np.mean(
    adaptive_results
)

std = np.std(
    adaptive_results
)

ci = (

    1.96

    *

    std

    /

    np.sqrt(RUNS)

)

availability = np.mean(
    adaptive_availability
)

gain = (

    (mean - BASELINE_KBPS)

    /

    BASELINE_KBPS

) * 100

print()
print("="*80)
print("RESULTS")
print("="*80)

print()

print(
    f"Mean Throughput : {mean:.3f} kbps"
)

print(
    f"95% CI          : ±{ci:.3f}"
)

print(
    f"Availability    : "
    f"{availability*100:.2f}%"
)

print(
    f"Gain vs d=4@250 : "
    f"{gain:.2f}%"
)
plt.figure(figsize=(8,5))

plt.hist(

    chosen_dimensions,

    bins=[1,3,5,9,17],

    rwidth=0.8

)

plt.xticks(
    [2,4,8,16]
)

plt.xlabel(
    "Chosen Dimension"
)

plt.ylabel(
    "Occurrences"
)

plt.title(
    "Adaptive Dimension Usage"
)

plt.grid(True)

plt.show()