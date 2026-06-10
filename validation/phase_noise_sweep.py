import numpy as np
import matplotlib.pyplot as plt

from channel.dynamic_fiber_channel import DynamicFiberChannel
from adaptive.channel_state import ChannelState
from adaptive.real_scheduler import RealScheduler
RUNS = 100
FRAMES = 500

LOSS_DB = 20

PHASE_NOISES = np.arange(
    0.05,
    0.35,
    0.05
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
adaptive_results = []
for sigma in PHASE_NOISES:

    print(f"\nPhase noise = {sigma:.2f} rad")

    d2_mc = []
    d4_mc = []
    d8_mc = []
    adaptive_mc = []

    for run in range(RUNS):

        channel = DynamicFiberChannel(
            length_km=100
        )

        t2 = 0
        t4 = 0
        t8 = 0
        ta = 0

        for frame in range(FRAMES):

            metrics = channel.step()

            #
            # Inject controllable phase noise
            #

            phase = (

                metrics.phase_rad

                +

                np.random.normal(
                    0,
                    sigma
                )

            )

            state = ChannelState(

                loss_db=LOSS_DB,

                phase_noise_rad=
                abs(phase),

                timing_jitter_ps=
                metrics.timing_ps,

                polarization_drift_deg=
                metrics.polarization_deg

            )

            #
            # Fixed d
            #

            for d in [2,4,8]:

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

                else:
                    t8 += kbps

            #
            # Adaptive
            #

            best = 0

            for d in [2,4,8,16]:

                skr = scheduler.evaluate_dimension(
                    d,
                    state
                )

                kbps = throughput(
                    skr,
                    d
                )

                best = max(
                    best,
                    kbps
                )

            ta += best

        d2_mc.append(t2/FRAMES)
        d4_mc.append(t4/FRAMES)
        d8_mc.append(t8/FRAMES)
        adaptive_mc.append(ta/FRAMES)

    d2_results.append(
        np.mean(d2_mc)
    )

    d4_results.append(
        np.mean(d4_mc)
    )

    d8_results.append(
        np.mean(d8_mc)
    )

    adaptive_results.append(
        np.mean(adaptive_mc)
    )
plt.figure(figsize=(10,6))

plt.plot(
    PHASE_NOISES,
    d2_results,
    marker='o',
    label='d=2'
)

plt.plot(
    PHASE_NOISES,
    d4_results,
    marker='o',
    label='d=4'
)

plt.plot(
    PHASE_NOISES,
    d8_results,
    marker='o',
    label='d=8'
)

plt.plot(
    PHASE_NOISES,
    adaptive_results,
    marker='o',
    linewidth=3,
    label='Adaptive'
)

plt.xlabel(
    "Injected Phase Noise (rad)"
)

plt.ylabel(
    "Throughput (kbps)"
)

plt.title(
    "Phase Noise Sweep"
)

plt.grid(True)

plt.legend()

plt.show()