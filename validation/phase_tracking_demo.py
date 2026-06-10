"""
phase_tracking_demo.py

Demonstrate predictive compensation.

Author:
MDI-QKD Digital Twin
"""

import matplotlib.pyplot as plt
import numpy as np

from channel.dynamic_fiber_channel import (
    DynamicFiberChannel
)

from control.perfect_compensator import (
    PerfectCompensator
)

N = 500

channel = DynamicFiberChannel(
    length_km=100
)

comp = PerfectCompensator()

true_phase = []
correction = []
residual = []

print()
print("="*80)
print("PHASE TRACKING DEMO")
print("="*80)

for i in range(N):

    metrics = channel.step()

    corr = comp.compensate(
        metrics
    )

    res = (

        metrics.phase_rad

        +

        corr.phase_rad
    )

    true_phase.append(
        metrics.phase_rad
    )

    correction.append(
        corr.phase_rad
    )

    residual.append(
        res
    )

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
    correction,
    "--",
    label="Compensation"
)

plt.plot(
    residual,
    linewidth=3,
    label="Residual"
)

plt.xlabel(
    "Frame"
)

plt.ylabel(
    "Phase (rad)"
)

plt.title(
    "Oracle Phase Compensation"
)

plt.grid(True)

plt.legend()

plt.show()

print()
print(
    "Residual RMS:",
    np.sqrt(
        np.mean(
            np.array(residual)**2
        )
    )
)