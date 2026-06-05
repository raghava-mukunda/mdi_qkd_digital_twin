from adaptive.channel_state import (
    ChannelState
)

from adaptive.real_scheduler import (
    RealScheduler
)

scheduler = RealScheduler()

state = ChannelState(

    loss_db=5,

    phase_noise_rad=0.1,

    timing_jitter_ps=20,

    polarization_drift_deg=2
)

best, results = (

    scheduler.choose_dimension(
        state
    )
)

print()
print("Best d =", best)

print()

for d,v in results.items():

    print(
        d,
        v
    )