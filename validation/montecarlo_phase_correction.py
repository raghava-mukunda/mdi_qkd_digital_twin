"""
validation/montecarlo_phase_correction.py

Monte Carlo comparison:
Fixed d=4 @ 250 MHz
vs
Fixed d=4 @ 250 MHz + Kalman phase correction

Author:
MDI-QKD Digital Twin
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

DIMENSION = 4
CLOCK = 250e6

LOSS_DB = 20
LENGTH_KM = 100

PILOT_SIGMA = 0.05
LATENCY = 1
PILOT_INTERVAL = 5

JUMP_PROBABILITY = 0.01
JUMP_STD = 0.5

# =====================================================
# SCHEDULER
# =====================================================

scheduler = RealScheduler(
    fast_mode=True
)

# =====================================================
# RESULTS STORAGE
# =====================================================

throughputs_no = []
throughputs_kalman = []

mean_residuals = []
rms_residuals = []
max_residuals = []

mean_visibilities = []
worst_visibilities = []

availability_no = []
availability_kalman = []

# =====================================================
# MONTE CARLO
# =====================================================

print()
print("="*80)
print("PHASE CORRECTION MONTE CARLO")
print("="*80)

for mc in range(MC_RUNS):

    channel = DynamicFiberChannel(
        length_km=LENGTH_KM
    )

    kalman = KalmanPredictor(

        dt=1.0,

        Q_phase=1e-6,

        Q_velocity=1e-6,

        Q_acceleration=1e-7,

        R=PILOT_SIGMA**2
    )

    prediction_buffer = deque(
        [0.0] * LATENCY,
        maxlen=LATENCY
    )

    no_series = []
    kalman_series = []

    residual_series = []

    for i in range(FRAMES):

        metrics = channel.step()

        # ======================================
        # TRUE PHASE
        # ======================================

        phi = (

            0.4*np.sin(i/30)

            +

            0.2*np.sin(i/100)

            +

            metrics.phase_rad

        )

        # ======================================
        # PHASE JUMPS
        # ======================================

        if np.random.random() < JUMP_PROBABILITY:

            phi += np.random.normal(

                0,

                JUMP_STD

            )

        # ======================================
        # NO CORRECTION
        # ======================================

        state_no = ChannelState(

            loss_db=LOSS_DB,

            phase_noise_rad=abs(phi),

            timing_jitter_ps=
            metrics.timing_ps,

            polarization_drift_deg=
            metrics.polarization_deg

        )

        skr_no = scheduler.evaluate_dimension(

            DIMENSION,

            state_no

        )

        throughput_no = (

            skr_no

            *

            CLOCK

            *

            np.log2(DIMENSION)

        )

        no_series.append(
            throughput_no
        )

        # ======================================
        # KALMAN CORRECTION
        # ======================================

        prediction = prediction_buffer.popleft()

        residual = (

            phi

            -

            prediction

        )

        residual_series.append(
            residual
        )

        state_k = ChannelState(

            loss_db=LOSS_DB,

            phase_noise_rad=0.0,

            timing_jitter_ps=
            metrics.timing_ps,

            polarization_drift_deg=
            metrics.polarization_deg,

            residual_phase_rad=
            abs(residual)

        )

        skr_k = scheduler.evaluate_dimension(

            DIMENSION,

            state_k

        )

        throughput_k = (

            skr_k

            *

            CLOCK

            *

            np.log2(DIMENSION)

        )

        kalman_series.append(
            throughput_k
        )

        # ======================================
        # PILOT UPDATE
        # ======================================

        if i % PILOT_INTERVAL == 0:

            z = (

                phi

                +

                np.random.normal(

                    0,

                    PILOT_SIGMA

                )

            )

            kalman.update(z)

        prediction_buffer.append(

            kalman.predict_ahead(

                max(0, LATENCY-2)

            )

        )

    # =================================================
    # STORE RUN RESULTS
    # =================================================

    no_series = np.array(no_series)
    kalman_series = np.array(kalman_series)

    residual_series = np.array(
        residual_series
    )

    visibility = (

        np.cos(

            residual_series/2

        )**2

    )

    throughputs_no.append(

        np.mean(no_series)

    )

    throughputs_kalman.append(

        np.mean(kalman_series)

    )

    mean_residuals.append(

        np.mean(

            np.abs(residual_series)

        )

    )

    rms_residuals.append(

        np.sqrt(

            np.mean(

                residual_series**2

            )

        )

    )

    max_residuals.append(

        np.max(

            np.abs(residual_series)

        )

    )

    mean_visibilities.append(

        np.mean(visibility)

    )

    worst_visibilities.append(

        np.min(visibility)

    )

    availability_no.append(

        np.mean(no_series > 0)

    )

    availability_kalman.append(

        np.mean(kalman_series > 0)

    )

    if (mc+1) % 50 == 0:

        print(

            f"{mc+1}/{MC_RUNS}"

        )

# =====================================================
# FINAL STATISTICS
# =====================================================

throughputs_no = np.array(
    throughputs_no
)

throughputs_kalman = np.array(
    throughputs_kalman
)

gain = (np.mean(throughputs_kalman)-np.mean(throughputs_no))/np.mean(throughputs_no)* 100

ci_no = (

    1.96

    *

    np.std(

        throughputs_no

    )

    /

    np.sqrt(MC_RUNS)

)

ci_k = (

    1.96

    *

    np.std(

        throughputs_kalman

    )

    /

    np.sqrt(MC_RUNS)

)

print()
print("="*80)
print("RESULTS")
print("="*80)

print()

print(
    f"Fixed dimension : d={DIMENSION}"
)

print(
    f"Clock           : {CLOCK/1e6:.0f} MHz"
)

print()

print("NO CORRECTION")

print(
    f"Mean Throughput : "
    f"{np.mean(throughputs_no)/1e3:.3f} kbps"
)

print(
    f"95% CI          : "
    f"±{ci_no/1e3:.3f}"
)

print(
    f"Availability    : "
    f"{100*np.mean(availability_no):.2f}%"
)

print()

print("KALMAN CORRECTION")

print(
    f"Mean Throughput : "
    f"{np.mean(throughputs_kalman)/1e3:.3f} kbps"
)

print(
    f"95% CI          : "
    f"±{ci_k/1e3:.3f}"
)

print(
    f"Availability    : "
    f"{100*np.mean(availability_kalman):.2f}%"
)

print()

print(
    f"Relative Gain   : "
    f"{gain:.2f}%"
)

print()

print(
    f"Mean Residual   : "
    f"{np.mean(mean_residuals):.4f} rad"
)

print(
    f"RMS Residual    : "
    f"{np.mean(rms_residuals):.4f} rad"
)

print(
    f"Worst Residual  : "
    f"{np.max(max_residuals):.4f} rad"
)

print()

print(
    f"Mean Visibility : "
    f"{np.mean(mean_visibilities):.4f}"
)

print(
    f"Worst Visibility: "
    f"{np.min(worst_visibilities):.4f}"
)

# =====================================================
# BAR CHART
# =====================================================

plt.figure(figsize=(8,6))

plt.bar(

    [

        "Fixed d=4",

        "d=4 + Kalman"

    ],

    [

        np.mean(throughputs_no)/1e3,

        np.mean(throughputs_kalman)/1e3

    ]

)

plt.ylabel("Throughput (kbps)")

plt.title(

    "Phase Correction Gain"

)

plt.grid(True)

plt.show()