import numpy as np

from adaptive.real_scheduler import (
    RealScheduler
)

from adaptive.channel_state import (
    ChannelState
)

scheduler = RealScheduler()

distances = np.arange(
    0,
    201,
    10
)

d2 = []
d4 = []
d8 = []
d16 = []
adaptive = []

for distance in distances:

    print(
        f"Distance {distance} km"
    )

    loss_db = (
        distance
        *
        0.2
    )

    state = ChannelState(

        loss_db=loss_db,

        phase_noise_rad=0.10,

        timing_jitter_ps=20,

        polarization_drift_deg=2

    )

    _, results = (
        scheduler.choose_dimension(
            state
        )
    )

    d2.append(results[2])
    d4.append(results[4])
    d8.append(results[8])
    d16.append(results[16])

    adaptive.append(
        max(
            results.values()
        )
    )

np.savez(

    "validation/distance_curve.npz",

    distances=distances,

    d2=np.array(d2),

    d4=np.array(d4),

    d8=np.array(d8),

    d16=np.array(d16),

    adaptive=np.array(adaptive)

)

print()
print("Saved:")
print("validation/distance_curve.npz")