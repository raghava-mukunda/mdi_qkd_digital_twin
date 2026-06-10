"""
kalman_skr_recovery_realistic.py

Realistic end-to-end SKR recovery test.

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

N = 1000

LENGTH_KM = 100

PILOT_SIGMA = 0.05

LATENCY = 1

PM_MAX_PHASE = np.pi / 2

PILOT_INTERVAL = 5

JUMP_PROBABILITY = 0.01
JUMP_STD = 0.5

LOSS_DB = 20

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

scheduler = RealScheduler()

prediction_buffer = deque(
    [0.0] * max(LATENCY, 1),
    maxlen=max(LATENCY, 1)
)

before = []
after = []

true_phase = []
pred_phase = []
residual_history = []

pilot_frames = 0

pilot_efficiency = (
    PILOT_INTERVAL - 1
) / PILOT_INTERVAL

print()
print("=" * 80)
print("REALISTIC END-TO-END STRESS TEST")
print("=" * 80)

for i in range(N):

    metrics = channel.step()

    #
    # Fiber phase evolution
    #

    phi = (

        0.4 * np.sin(i / 30)

        +

        0.2 * np.sin(i / 100)

        +

        metrics.phase_rad
    )

    #
    # Sudden disturbances
    #

    if np.random.random() < JUMP_PROBABILITY:

        phi += np.random.normal(
            0,
            JUMP_STD
        )

    #
    # Available FPGA prediction
    #

    if LATENCY == 0:

        prediction = kalman.predict_ahead(0)

    else:

        prediction = prediction_buffer.popleft()

    prediction = np.clip(

        prediction,

        -PM_MAX_PHASE,

        PM_MAX_PHASE
    )

    residual = phi - prediction

    residual_history.append(
        residual
    )

    #
    # Baseline
    #

    state_before = ChannelState(

        loss_db=LOSS_DB,

        phase_noise_rad=abs(phi),

        timing_jitter_ps=
        metrics.timing_ps,

        polarization_drift_deg=
        metrics.polarization_deg
    )

    best_before, scores_before = (

        scheduler.choose_dimension(
            state_before
        )
    )

    skr_before = (

        scores_before[
            best_before
        ]

        *

        pilot_efficiency
    )

    #
    # Kalman compensation
    #

    state_after = ChannelState(

        loss_db=LOSS_DB,

        phase_noise_rad=0.0,

        timing_jitter_ps=
        metrics.timing_ps,

        polarization_drift_deg=
        metrics.polarization_deg,

        residual_phase_rad=
        abs(residual)
    )

    best_after, scores_after = (

        scheduler.choose_dimension(
            state_after
        )
    )

    skr_after = (

        scores_after[
            best_after
        ]

        *

        pilot_efficiency
    )

    #
    # Pilot update
    #

    if i % PILOT_INTERVAL == 0:

        pilot_frames += 1

        z = phi + np.random.normal(

            0,

            PILOT_SIGMA
        )

        kalman.update(z)

    #
    # Predict future phase
    #

    if LATENCY > 0:

        prediction_buffer.append(

            kalman.predict_ahead(LATENCY)

        )

    before.append(
        skr_before
    )

    after.append(
        skr_after
    )

    true_phase.append(
        phi
    )

    pred_phase.append(
        prediction
    )

    if (i + 1) % 100 == 0:

        print(
            f"{i+1}/{N}"
        )

before_arr = np.array(before)
after_arr = np.array(after)
#
# Estimate prediction lag
#

true_arr = np.array(true_phase)
pred_arr = np.array(pred_phase)

corr = np.correlate(
    true_arr - np.mean(true_arr),
    pred_arr - np.mean(pred_arr),
    mode="full"
)

lag = (

    np.argmax(corr)

    -

    (len(true_arr)-1)

)

aligned_pred = np.roll(

    pred_arr,

    lag

)

print()
print("="*80)
print("LAG ANALYSIS")
print("="*80)

print(f"Prediction lag = {lag} frames")
print()
print("=" * 80)
print("RESULTS")
print("=" * 80)

before_mean = np.mean(
    before_arr
)

after_mean = np.mean(
    after_arr
)

gain = (

    after_mean
    -
    before_mean

) / before_mean * 100

print()

print(
    f"Pilot Noise       : {PILOT_SIGMA:.2f} rad"
)

print(
    f"FPGA Latency      : {LATENCY} frames"
)

print(
    f"Pilot Interval    : {PILOT_INTERVAL}"
)

print(
    f"Pilot Overhead    : "
    f"{100*(1-pilot_efficiency):.1f}%"
)

print(
    f"Jump Probability  : "
    f"{JUMP_PROBABILITY:.2f}"
)

print()

print(
    f"Mean SKR Before : "
    f"{before_mean:.4e}"
)

print(
    f"Mean SKR After  : "
    f"{after_mean:.4e}"
)

print(
    f"Relative Gain   : "
    f"{gain:.2f}%"
)

print()

print(
    f"Worst Before : "
    f"{np.min(before_arr):.4e}"
)

print(
    f"Worst After  : "
    f"{np.min(after_arr):.4e}"
)

print()

print(
    f"Best Before : "
    f"{np.max(before_arr):.4e}"
)

print(
    f"Best After  : "
    f"{np.max(after_arr):.4e}"
)

#
# Residual analysis
#

residual_arr = (true_arr-aligned_pred)

phase_visibility = (

    np.cos(
        residual_arr / 2
    ) ** 2
)

print()
print("=" * 80)
print("PHASE RESIDUAL ANALYSIS")
print("=" * 80)

print()

print(
    f"Mean Residual : "
    f"{np.mean(np.abs(residual_arr)):.4f} rad"
)

print(
    f"RMS Residual  : "
    f"{np.sqrt(np.mean(residual_arr**2)):.4f} rad"
)

print(
    f"Max Residual  : "
    f"{np.max(np.abs(residual_arr)):.4f} rad"
)

print()

print(
    f"Mean Phase Visibility : "
    f"{np.mean(phase_visibility):.4f}"
)

print(
    f"Worst Phase Visibility: "
    f"{np.min(phase_visibility):.4f}"
)

#
# Availability
#

threshold = 1e-5

availability_before = np.mean(
    before_arr > threshold
)

availability_after = np.mean(
    after_arr > threshold
)

print()
print("=" * 80)
print("LINK AVAILABILITY ANALYSIS")
print("=" * 80)

print()

print(
    f"Availability Before : "
    f"{availability_before*100:.2f}%"
)

print(
    f"Availability After  : "
    f"{availability_after*100:.2f}%"
)

#
# Plots
#

plt.figure(figsize=(10, 6))

plt.plot(
    before_arr,
    label="No compensation"
)

plt.plot(
    after_arr,
    label="Kalman"
)

plt.xlabel("Frame")
plt.ylabel("SKR")
plt.title("End-to-End SKR Recovery")
plt.grid(True)
plt.legend()

plt.show()

plt.figure(figsize=(10, 6))

plt.plot(
    true_phase,
    label="True Phase"
)

plt.plot(
    aligned_pred,
    label=f"Predicted Phase (lag={lag})"
)

plt.xlabel("Frame")
plt.ylabel("Phase (rad)")
plt.title("Phase Tracking")
plt.grid(True)
plt.legend()

plt.show()

plt.figure(figsize=(10, 6))

plt.plot(
    residual_arr,
    label="Residual"
)

plt.axhline(
    0.1,
    linestyle="--"
)

plt.axhline(
    -0.1,
    linestyle="--"
)

plt.xlabel("Frame")
plt.ylabel("Residual Phase (rad)")
plt.title("Phase Compensation Residual")
plt.grid(True)
plt.legend()

plt.show()