import pandas as pd
import numpy as np

from adaptive.channel_state import ChannelState
from adaptive.real_scheduler import RealScheduler

N_SAMPLES = 10000

rng = np.random.default_rng(42)

scheduler = RealScheduler()

rows = []

print()
print("="*80)
print("GENERATING TRAINING DATA")
print("="*80)

for i in range(N_SAMPLES):

    if i % 100 == 0:

        print(
            f"\rProgress: {i}/{N_SAMPLES}",
            end=""
        )

    state = ChannelState(

        loss_db=rng.uniform(
            0,
            20
        ),

        phase_noise_rad=rng.uniform(
            0.02,
            0.30
        ),

        timing_jitter_ps=rng.uniform(
            10,
            50
        ),

        polarization_drift_deg=rng.uniform(
            0,
            5
        )
    )

    best_d, _ = scheduler.choose_dimension(
        state
    )

    rows.append([

        state.loss_db,

        state.phase_noise_rad,

        state.timing_jitter_ps,

        state.polarization_drift_deg,

        best_d
    ])

df = pd.DataFrame(

    rows,

    columns=[

        "loss_db",

        "phase_noise_rad",

        "timing_jitter_ps",

        "polarization_drift_deg",

        "optimal_d"
    ]
)
print()
print(df["optimal_d"].value_counts())
df.to_csv(

    "validation/dimension_training_data.csv",

    index=False
)

print()
print()
print("Saved:")
print(
    "validation/dimension_training_data.csv"
)