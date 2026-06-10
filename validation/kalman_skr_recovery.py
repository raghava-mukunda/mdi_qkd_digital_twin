"""
kalman_skr_recovery.py

SKR Recovery Using Predictive Compensation

Author:
MDI-QKD Digital Twin
"""

import numpy as np
import matplotlib.pyplot as plt

from channel.dynamic_fiber_channel import (
    DynamicFiberChannel
)

from control.kalman_predictor import (
    KalmanPredictor
)

from adaptive.channel_state import (
    ChannelState
)

from adaptive.real_scheduler import (
    RealScheduler
)


N = 500

channel = DynamicFiberChannel(
    length_km=100
)

kalman = KalmanPredictor(

    alpha=0.995,
    Q=5e-5,
    R=4e-4
)

scheduler = RealScheduler()

before = []
after = []

phase_true = []
phase_pred = []

previous_prediction = 0.0

print()
print("="*80)
print("KALMAN SKR RECOVERY")
print("="*80)

for i in range(N):

    metrics = channel.step()

    #
    # Strong phase impairment
    #
    phi = (

        0.6 * np.sin(i/30)

        +

        metrics.phase_rad
    )

    #
    # Pilot measurement
    #
    z = phi + np.random.normal(
        0,
        0.02
    )

    #
    # WITHOUT compensation
    #
    state_before = ChannelState(

        loss_db=20,

        phase_noise_rad=abs(phi),

        timing_jitter_ps=metrics.timing_ps,

        polarization_drift_deg=metrics.polarization_deg
    )

    best_before, scores_before = (

        scheduler.choose_dimension(
            state_before
        )
    )

    skr_before = scores_before[
        best_before
    ]

    #
    # WITH compensation
    #
    residual_phase = abs(

        phi

        -

        previous_prediction
    )

    state_after = ChannelState(

        loss_db=20,

        phase_noise_rad=
        residual_phase,

        timing_jitter_ps=
        metrics.timing_ps,

        polarization_drift_deg=
        metrics.polarization_deg
    )

    best_after, scores_after = (

        scheduler.choose_dimension(
            state_after
        )
    )

    skr_after = scores_after[
        best_after
    ]

    before.append(
        skr_before
    )

    after.append(
        skr_after
    )

    phase_true.append(
        phi
    )

    phase_pred.append(
        previous_prediction
    )

    #
    # Kalman update
    #
    kalman.update(z)

    previous_prediction = (

        kalman.predict_next()
    )

    if (i+1) % 50 == 0:

        print(
            f"{i+1}/{N}"
        )


before_mean = np.mean(
    before
)

after_mean = np.mean(
    after
)

gain = (

    after_mean
    -
    before_mean

) / before_mean * 100


print()
print("="*80)
print("RESULTS")
print("="*80)

print()

print(
    f"Mean SKR Before : {before_mean:.4e}"
)

print(
    f"Mean SKR After  : {after_mean:.4e}"
)

print(
    f"Relative Gain   : {gain:.2f}%"
)

print()

print(
    f"Worst SKR Before: {np.min(before):.4e}"
)

print(
    f"Worst SKR After : {np.min(after):.4e}"
)

print()

print(
    f"Best SKR Before : {np.max(before):.4e}"
)

print(
    f"Best SKR After  : {np.max(after):.4e}"
)


#
# SKR recovery
#
plt.figure(figsize=(10,6))

plt.plot(
    before,
    label="No compensation"
)

plt.plot(
    after,
    label="Kalman compensation"
)

plt.xlabel(
    "Frame"
)

plt.ylabel(
    "SKR (bits/pulse)"
)

plt.title(
    "SKR Recovery Using Predictive Compensation"
)

plt.grid(True)

plt.legend()

plt.show()


#
# Phase tracking
#
plt.figure(figsize=(10,6))

plt.plot(
    phase_true,
    label="True phase"
)

plt.plot(
    phase_pred,
    label="Prediction"
)

plt.xlabel(
    "Frame"
)

plt.ylabel(
    "Phase (rad)"
)

plt.title(
    "Kalman Phase Prediction"
)

plt.grid(True)

plt.legend()

plt.show()