"""
kalman_hom_recovery.py

Kalman HOM Recovery Validation

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

from interference.beam_splitter import (
    BeamSplitter
)

from bsm.quantum_state import (
    QuantumStateFactory
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

bs = BeamSplitter()

alice = QuantumStateFactory.create(
    8,
    "X",
    0
)

bob = QuantumStateFactory.create(
    8,
    "X",
    0
)

before = []
after = []

true_phase = []
measured_phase = []
predicted_phase = []

previous_prediction = 0.0

print()
print("=" * 80)
print("KALMAN HOM RECOVERY")
print("=" * 80)

for i in range(N):

    metrics = channel.step()

    #
    # Force strong phase dynamics
    # to verify compensation path
    #
    phi = (

        0.6 * np.sin(i / 30)

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
    # HOM without compensation
    #
    hom1 = bs.interfere(

        alice,
        bob,

        timing_offset_ps=0,

        phase_offset_rad=phi,

        polarization_offset_deg=0
    )

    #
    # HOM with FPGA-style
    # 1-frame delayed prediction
    #
    hom2 = bs.interfere(

        alice,
        bob,

        timing_offset_ps=0,

        phase_offset_rad=
        phi - previous_prediction,

        polarization_offset_deg=0
    )

    before.append(
        hom1.total_visibility
    )

    after.append(
        hom2.total_visibility
    )

    true_phase.append(phi)

    measured_phase.append(z)

    predicted_phase.append(
        previous_prediction
    )

    #
    # Update filter
    #
    kalman.update(z)

    #
    # Predict next frame
    #
    previous_prediction = (
        kalman.predict_next()
    )

    if (i + 1) % 50 == 0:

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

    (after_mean - before_mean)

    /

    before_mean

) * 100

print()
print("=" * 80)
print("RESULTS")
print("=" * 80)

print(
    f"Mean HOM Before : {before_mean:.4f}"
)

print(
    f"Mean HOM After  : {after_mean:.4f}"
)

print(
    f"Relative Gain   : {gain:.2f}%"
)

print()

print(
    f"Worst HOM Before: {np.min(before):.4f}"
)

print(
    f"Worst HOM After : {np.min(after):.4f}"
)

print()

print(
    f"Best HOM Before : {np.max(before):.4f}"
)

print(
    f"Best HOM After  : {np.max(after):.4f}"
)


#
# HOM recovery plot
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
    "HOM Visibility"
)

plt.title(
    "Kalman HOM Recovery (1-Frame Prediction)"
)

plt.grid(True)

plt.legend()

plt.show()


#
# Phase tracking plot
#
plt.figure(figsize=(10,6))

plt.plot(
    true_phase,
    label="True phase"
)

plt.plot(
    measured_phase,
    alpha=0.6,
    label="Measured"
)

plt.plot(
    predicted_phase,
    linewidth=2,
    label="Kalman prediction"
)

plt.xlabel(
    "Frame"
)

plt.ylabel(
    "Phase (rad)"
)

plt.title(
    "Kalman Phase Tracking"
)

plt.grid(True)

plt.legend()

plt.show()
print()
print("Mean HOM Before :", np.mean(before))
print("Mean HOM After  :", np.mean(after))

print(
    "Absolute HOM Gain:",
    np.mean(after)-np.mean(before)
)

print(
    "Relative Gain (%):",
    (
        np.mean(after)-np.mean(before)
    )
    /
    np.mean(before)
    *100
)