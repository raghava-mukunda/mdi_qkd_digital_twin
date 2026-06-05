from adaptive.channel_state import (
    ChannelState
)

from adaptive.adaptive_scheduler import (
    AdaptiveScheduler
)

scheduler = AdaptiveScheduler()

states = [

    ChannelState(
        loss_db=2,
        phase_noise_rad=0.02,
        timing_jitter_ps=20,
        polarization_drift_deg=1
    ),

    ChannelState(
        loss_db=5,
        phase_noise_rad=0.05,
        timing_jitter_ps=20,
        polarization_drift_deg=2
    ),

    ChannelState(
        loss_db=10,
        phase_noise_rad=0.10,
        timing_jitter_ps=20,
        polarization_drift_deg=3
    ),

    ChannelState(
        loss_db=15,
        phase_noise_rad=0.20,
        timing_jitter_ps=20,
        polarization_drift_deg=5
    )

]

for i, state in enumerate(states):

    decision = (
        scheduler.choose_dimension(
            state
        )
    )

    print()
    print("="*70)
    print(f"State {i+1}")
    print("="*70)

    print(
        "Selected d:",
        decision.selected_dimension
    )

    print(
        "Predicted SKR:",
        decision.predicted_skr
    )

    print(
        "All:",
        decision.all_results
    )