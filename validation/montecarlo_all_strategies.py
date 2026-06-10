"""
validation/montecarlo_all_strategies.py

Master Monte Carlo

Same channel realization for ALL strategies.

Strategies:
1) Fixed d=4
2) Adaptive
3) Fixed d=4 + Kalman
4) Adaptive + Kalman
"""

import numpy as np
import matplotlib.pyplot as plt
from collections import deque

from channel.dynamic_fiber_channel import DynamicFiberChannel
from control.kalman_predictor import KalmanPredictor
from adaptive.channel_state import ChannelState
from adaptive.real_scheduler import RealScheduler


# =====================================================
# SETTINGS
# =====================================================

MC_RUNS = 1000
FRAMES = 1000

LOSS_DB = 20
LENGTH_KM = 100

PILOT_SIGMA = 0.05
PILOT_INTERVAL = 5
LATENCY = 1

JUMP_PROBABILITY = 0.01
JUMP_STD = 0.5

FIXED_D = 4
FIXED_CLOCK = 250e6

RATE_MAP = {

    2: 500e6,
    4: 250e6,
    8: 125e6,
    16: 62.5e6

}


# =====================================================
# SCHEDULER
# =====================================================

scheduler = RealScheduler(

    fast_mode=True

)


# =====================================================
# RESULTS STORAGE
# =====================================================

fixed_results = []

adaptive_results = []

fixed_kalman_results = []

adaptive_kalman_results = []


adaptive_choices = []

adaptive_kalman_choices = []


fixed_residuals = []

adaptive_residuals = []


# =====================================================
# MONTE CARLO
# =====================================================

print()
print("=" * 80)
print("MASTER MONTE CARLO")
print("=" * 80)


for mc in range(MC_RUNS):

    #
    # SAME CHANNEL
    #

    channel = DynamicFiberChannel(

        length_km=LENGTH_KM

    )

    #
    # Independent Kalman controllers
    #

    kalman_fixed = KalmanPredictor(

        dt=1.0,

        Q_phase=1e-6,

        Q_velocity=1e-6,

        Q_acceleration=1e-7,

        R=PILOT_SIGMA**2

    )

    kalman_adaptive = KalmanPredictor(

        dt=1.0,

        Q_phase=1e-6,

        Q_velocity=1e-6,

        Q_acceleration=1e-7,

        R=PILOT_SIGMA**2

    )

    #
    # FPGA buffers
    #

    buffer_fixed = deque(

        [0.0] * LATENCY,

        maxlen=LATENCY

    )

    buffer_adaptive = deque(

        [0.0] * LATENCY,

        maxlen=LATENCY

    )

    #
    # Per-run accumulators
    #

    fixed_series = []

    adaptive_series = []

    fixed_k_series = []

    adaptive_k_series = []


    # =================================================
    # COMMON CHANNEL REALIZATION
    # =================================================

    for i in range(FRAMES):

        metrics = channel.step()

        #
        # COMMON TRUE PHASE
        #

        phi = (

            0.4 * np.sin(i / 30)

            +

            0.2 * np.sin(i / 100)

            +

            metrics.phase_rad

        )

        #
        # SAME phase jump for all strategies
        #

        if np.random.random() < JUMP_PROBABILITY:

            phi += np.random.normal(

                0,

                JUMP_STD

            )

        #
        # SAME timing and polarization
        #

        timing = metrics.timing_ps

        polarization = metrics.polarization_deg

        # =================================================
        # STRATEGY A
        # Fixed d=4
        # =================================================

        state_fixed = ChannelState(

            loss_db=LOSS_DB,

            phase_noise_rad=abs(phi),

            timing_jitter_ps=timing,

            polarization_drift_deg=polarization

        )

        skr_fixed = scheduler.evaluate_dimension(

            FIXED_D,

            state_fixed

        )

        throughput_fixed = (

            skr_fixed

            *

            np.log2(FIXED_D)

            *

            FIXED_CLOCK

        )

        fixed_series.append(

            throughput_fixed

        )


        # =================================================
        # STRATEGY B
        # Adaptive
        # =================================================

        state_adaptive = ChannelState(

            loss_db=LOSS_DB,

            phase_noise_rad=abs(phi),

            timing_jitter_ps=timing,

            polarization_drift_deg=polarization

        )

        best_d = None
        best_tp = -1.0

        for d in [2, 4, 8, 16]:

            skr = scheduler.evaluate_dimension(

                d,

                state_adaptive

            )

            tp = (

                skr

                *

                np.log2(d)

                *

                RATE_MAP[d]

            )

            if tp > best_tp:

                best_tp = tp
                best_d = d

        adaptive_series.append(

            best_tp

        )

        adaptive_choices.append(

            best_d

        )


        # =================================================
        # STRATEGY C
        # Fixed + Kalman
        # =================================================

        prediction_fixed = buffer_fixed.popleft()

        residual_fixed = (

            phi

            -

            prediction_fixed

        )

        fixed_residuals.append(

            abs(residual_fixed)

        )

        state_fixed_k = ChannelState(

            loss_db=LOSS_DB,

            phase_noise_rad=0.0,

            timing_jitter_ps=timing,

            polarization_drift_deg=polarization,

            residual_phase_rad=abs(residual_fixed)

        )

        skr_fixed_k = scheduler.evaluate_dimension(

            FIXED_D,

            state_fixed_k

        )

        throughput_fixed_k = (

            skr_fixed_k

            *

            np.log2(FIXED_D)

            *

            FIXED_CLOCK

        )

        fixed_k_series.append(

            throughput_fixed_k

        )


        # =================================================
        # STRATEGY D
        # Adaptive + Kalman
        # =================================================

        prediction_adaptive = buffer_adaptive.popleft()

        residual_adaptive = (

            phi

            -

            prediction_adaptive

        )

        adaptive_residuals.append(

            abs(residual_adaptive)

        )

        state_adaptive_k = ChannelState(

            loss_db=LOSS_DB,

            phase_noise_rad=0.0,

            timing_jitter_ps=timing,

            polarization_drift_deg=polarization,

            residual_phase_rad=abs(residual_adaptive)

        )

        best_d_k = None
        best_tp_k = -1.0

        for d in [2, 4, 8, 16]:

            skr = scheduler.evaluate_dimension(

                d,

                state_adaptive_k

            )

            tp = (

                skr

                *

                np.log2(d)

                *

                RATE_MAP[d]

            )

            if tp > best_tp_k:

                best_tp_k = tp
                best_d_k = d

        adaptive_k_series.append(

            best_tp_k

        )

        adaptive_kalman_choices.append(

            best_d_k

        )


        # =================================================
        # PILOT UPDATE
        # =================================================

        if i % PILOT_INTERVAL == 0:

            measurement = (

                phi

                +

                np.random.normal(

                    0,

                    PILOT_SIGMA

                )

            )

            kalman_fixed.update(

                measurement

            )

            kalman_adaptive.update(

                measurement

            )


        # =================================================
        # FUTURE PREDICTIONS
        # =================================================

        buffer_fixed.append(

            kalman_fixed.predict_ahead(

                max(0, LATENCY - 2)

            )

        )

        buffer_adaptive.append(

            kalman_adaptive.predict_ahead(

                max(0, LATENCY - 2)

            )

        )
    fixed_results.append(
        np.mean(fixed_series)
    )

    adaptive_results.append(
        np.mean(adaptive_series)
    )

    fixed_kalman_results.append(
        np.mean(fixed_k_series)
    )

    adaptive_kalman_results.append(
        np.mean(adaptive_k_series)
    )

    if (mc + 1) % 50 == 0:

        print(
            f"{mc+1}/{MC_RUNS}"
        )
# =====================================================
# FINAL STATISTICS
# =====================================================

fixed_results = np.array(fixed_results)

adaptive_results = np.array(adaptive_results)

fixed_kalman_results = np.array(
    fixed_kalman_results
)

adaptive_kalman_results = np.array(
    adaptive_kalman_results
)


def ci95(x):

    return (

        1.96

        *

        np.std(x)

        /

        np.sqrt(len(x))

    )


fixed_mean = np.mean(fixed_results)
adaptive_mean = np.mean(adaptive_results)

fixed_k_mean = np.mean(
    fixed_kalman_results
)

adaptive_k_mean = np.mean(
    adaptive_kalman_results
)


fixed_ci = ci95(
    fixed_results
)

adaptive_ci = ci95(
    adaptive_results
)

fixed_k_ci = ci95(
    fixed_kalman_results
)

adaptive_k_ci = ci95(
    adaptive_kalman_results
)


fixed_gain = 0.0

adaptive_gain = (

    adaptive_mean
    -
    fixed_mean

) / fixed_mean * 100

fixed_k_gain = (

    fixed_k_mean
    -
    fixed_mean

) / fixed_mean * 100

adaptive_k_gain = (

    adaptive_k_mean
    -
    fixed_mean

) / fixed_mean * 100
print()
print("="*80)
print("FINAL COMPARISON")
print("="*80)

print()

print(
    f"{'Strategy':<30}"
    f"{'Mean (kbps)':>15}"
    f"{'95% CI':>15}"
    f"{'Gain':>12}"
)

print("-"*72)

print(
    f"{'Fixed d=4':<30}"
    f"{fixed_mean/1e3:>15.3f}"
    f"{fixed_ci/1e3:>15.3f}"
    f"{fixed_gain:>11.2f}%"
)

print(
    f"{'Adaptive':<30}"
    f"{adaptive_mean/1e3:>15.3f}"
    f"{adaptive_ci/1e3:>15.3f}"
    f"{adaptive_gain:>11.2f}%"
)

print(
    f"{'Fixed d=4 + Kalman':<30}"
    f"{fixed_k_mean/1e3:>15.3f}"
    f"{fixed_k_ci/1e3:>15.3f}"
    f"{fixed_k_gain:>11.2f}%"
)

print(
    f"{'Adaptive + Kalman':<30}"
    f"{adaptive_k_mean/1e3:>15.3f}"
    f"{adaptive_k_ci/1e3:>15.3f}"
    f"{adaptive_k_gain:>11.2f}%"
)
print()
print("="*80)
print("ADAPTIVE DIMENSION USAGE")
print("="*80)

for d in [2,4,8,16]:

    frac = (

        np.mean(

            np.array(adaptive_choices) == d

        )

        * 100

    )

    print(
        f"Adaptive d={d}: {frac:.2f}%"
    )


print()

for d in [2,4,8,16]:

    frac = (

        np.mean(

            np.array(
                adaptive_kalman_choices
            ) == d

        )

        * 100

    )

    print(
        f"Adaptive+Kalman d={d}: {frac:.2f}%"
    )
fixed_residuals = np.array(
    fixed_residuals
)

adaptive_residuals = np.array(
    adaptive_residuals
)

print()
print("="*80)
print("RESIDUAL ANALYSIS")
print("="*80)

print()

print(
    f"Fixed+Kalman Mean Residual : "
    f"{np.mean(fixed_residuals):.4f} rad"
)

print(
    f"Fixed+Kalman RMS Residual  : "
    f"{np.sqrt(np.mean(fixed_residuals**2)):.4f} rad"
)

print(
    f"Adaptive+Kalman Mean Residual : "
    f"{np.mean(adaptive_residuals):.4f} rad"
)

print(
    f"Adaptive+Kalman RMS Residual  : "
    f"{np.sqrt(np.mean(adaptive_residuals**2)):.4f} rad"
)
plt.figure(figsize=(10,6))

means = [

    fixed_mean/1e3,

    adaptive_mean/1e3,

    fixed_k_mean/1e3,

    adaptive_k_mean/1e3

]

labels = [

    "Fixed",

    "Adaptive",

    "Fixed\n+Kalman",

    "Adaptive\n+Kalman"

]

plt.bar(
    labels,
    means
)

plt.ylabel(
    "Throughput (kbps)"
)

plt.title(
    "Final Strategy Comparison"
)

plt.grid(True)

plt.show()
plt.figure(figsize=(8,5))

plt.hist(

    adaptive_choices,

    bins=[1,3,5,9,17],

    alpha=0.5,

    label="Adaptive"

)

plt.hist(

    adaptive_kalman_choices,

    bins=[1,3,5,9,17],

    alpha=0.5,

    label="Adaptive + Kalman"

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
    "Dimension Usage"
)

plt.legend()

plt.grid(True)

plt.show()