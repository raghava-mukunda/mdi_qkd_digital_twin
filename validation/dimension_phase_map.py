"""
dimension_phase_map.py

Find optimal dimension across
channel conditions.

Author:
MDI-QKD Digital Twin
"""

from adaptive.channel_state import (
    ChannelState
)

from adaptive.real_scheduler import (
    RealScheduler
)

scheduler = RealScheduler()

print()
print("="*90)
print("OPTIMAL DIMENSION MAP")
print("="*90)

for loss in [

    0,
    2,
    5,
    10,
    15,
    20

]:

    print()
    print(f"\nLOSS = {loss} dB")
    print("-"*90)

    for phase_noise in [

        0.02,
        0.05,
        0.10,
        0.15,
        0.20,
        0.25,
        0.30

    ]:

        state = ChannelState(

            loss_db=loss,

            phase_noise_rad=phase_noise,

            timing_jitter_ps=20,

            polarization_drift_deg=2
        )

        best, results = (

            scheduler.choose_dimension(
                state
            )
        )

        print(

            f"Phase={phase_noise:.2f}"

            f"  Best d={best}"

        )