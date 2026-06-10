"""
kalman_phase_demo.py
"""

import matplotlib.pyplot as plt
import numpy as np

from channel.dynamic_fiber_channel import (
    DynamicFiberChannel
)

from control.kalman_predictor import (
    KalmanPredictor
)

N = 500

channel = DynamicFiberChannel(
    length_km=100
)

kalman = KalmanPredictor()

true_phase = []
measured = []
predicted = []

print()
print("="*80)
print("KALMAN PHASE TRACKING")
print("="*80)

for i in range(N):

    metrics = channel.step()

    phi = metrics.phase_rad

    noise = np.random.normal(
        0,
        0.02
    )

    z = phi + noise

    kalman.update(z)

    pred = kalman.predict_next()

    true_phase.append(phi)

    measured.append(z)

    predicted.append(pred)

    if (i+1) % 50 == 0:

        print(
            f"{i+1}/{N}"
        )

plt.figure(figsize=(10,6))

plt.plot(
    true_phase,
    label="True phase"
)

plt.plot(
    measured,
    alpha=0.5,
    label="Measured"
)

plt.plot(
    predicted,
    linewidth=2,
    label="Kalman prediction"
)

plt.xlabel("Frame")
plt.ylabel("Phase (rad)")

plt.title(
    "Kalman Phase Prediction"
)

plt.grid(True)

plt.legend()

plt.show()

rmse = np.sqrt(

    np.mean(

        (

            np.array(true_phase)

            -

            np.array(predicted)

        )**2
    )
)

print()
print(
    "Prediction RMSE:",
    rmse
)