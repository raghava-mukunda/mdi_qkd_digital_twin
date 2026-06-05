from adaptive.channel_state import (
    ChannelState
)

from adaptive.real_scheduler import (
    RealScheduler
)

scheduler = RealScheduler()

state = ChannelState(

    loss_db=0,

    phase_noise_rad=0.30,

    timing_jitter_ps=20,

    polarization_drift_deg=2
)

print()
print("="*70)
print("HIGH NOISE DEBUG")
print("="*70)

for d in [2,4,8,16]:

    scheduler.xerr.params.phase_noise_std_rad = (
        state.phase_noise_rad
    )

    visibility = (

        1

        -

        state.polarization_drift_deg
        /
        100
    )

    visibility = max(
        visibility,
        0.5
    )

    x = scheduler.xerr.calculate(

        dimension=d,

        visibility=visibility
    )

    q11 = scheduler.estimate_q11(
        d,
        state
    )

    skr = scheduler.evaluate_dimension(
        d,
        state
    )

    print()

    print("d =", d)
    print("Q11 =", q11)
    print("EX11 =", x.error_rate)
    print("Phase Visibility =", x.phase_visibility)
    print("SKR =", skr)