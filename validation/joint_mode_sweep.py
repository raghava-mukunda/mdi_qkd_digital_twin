from adaptive.channel_state import ChannelState
from adaptive.joint_scheduler import JointScheduler

scheduler = JointScheduler()

state = ChannelState(

    loss_db=5,

    phase_noise_rad=0.08,

    timing_jitter_ps=20,

    polarization_drift_deg=2
)

best, results = (

    scheduler.choose_mode(

        state

    )

)

print()

print("="*80)
print("JOINT CLOCK–DIMENSION SWEEP")
print("="*80)

print()

for mode,value in sorted(

    results.items(),

    key=lambda x: (

        x[0].frequency_hz,

        x[0].dimension

    )

):

    print(

        f"{mode.frequency_hz/1e6:>6.0f} MHz"

        f"   d={mode.dimension:<2}"

        f"   Throughput={value:.3e} bits/s"

    )

print()

print(

    "BEST MODE: "

    f"{best.frequency_hz/1e6:.0f} MHz"

    f", d={best.dimension}"

)