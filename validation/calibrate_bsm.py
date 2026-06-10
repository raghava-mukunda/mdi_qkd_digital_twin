"""
calibrate_bsm.py

Calibrate nominal BSM probabilities
using the full CharlieReceiver simulation.

Author:
MDI-QKD Digital Twin
"""

from statistics.physical_q11 import PhysicalQ11

LOSS_DB = 20
TRIALS = 10000

q11 = PhysicalQ11()

print()
print("=" * 80)
print("BSM CALIBRATION")
print("=" * 80)
print()

print(f"Loss      : {LOSS_DB} dB")
print(f"Trials    : {TRIALS}")
print()

P_BSM = {}

for d in [2, 4, 8, 16]:

    result = q11.estimate(

        dimension=d,

        loss_db=LOSS_DB,

        phase_offset_rad=0.0,

        timing_offset_ps=0.0,

        polarization_offset_deg=0.0,

        trials=TRIALS

    )

    P_BSM[d] = result.bsm_probability

    print(
        f"d={d:<2}  "
        f"BSM Probability = {result.bsm_probability:.6f}"
    )

print()
print("=" * 80)
print("COPY THIS INTO fast_q11()")
print("=" * 80)
print()

print("P_BSM = {")

for d in [2, 4, 8, 16]:

    print(
        f"    {d}: {P_BSM[d]:.6f},"
    )

print("}")

print()
print("=" * 80)