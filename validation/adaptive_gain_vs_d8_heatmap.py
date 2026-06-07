import numpy as np
import matplotlib.pyplot as plt

from adaptive.channel_state import ChannelState
from adaptive.real_scheduler import RealScheduler

scheduler = RealScheduler()

loss_values = np.linspace(
    0,
    20,
    21
)

phase_values = np.linspace(
    0.02,
    0.30,
    29
)

gain_map = np.zeros(
    (
        len(loss_values),
        len(phase_values)
    )
)

total = (
    len(loss_values)
    *
    len(phase_values)
)

counter = 0

print()
print("="*80)
print("ADAPTIVE GAIN vs FIXED d=8")
print("="*80)

for i, loss in enumerate(loss_values):

    for j, phase in enumerate(phase_values):

        state = ChannelState(

            loss_db=float(loss),

            phase_noise_rad=float(phase),

            timing_jitter_ps=20,

            polarization_drift_deg=2
        )

        adaptive = 0.0

        fixed_d8 = 0.0

        N = 10

        for _ in range(N):

            best, scores = (

                scheduler.choose_dimension(
                    state
                )

            )

            adaptive += scores[best]

            fixed_d8 += scores[8]

        adaptive /= N

        fixed_d8 /= N

        gain = (

            adaptive

            -

            fixed_d8

        ) / fixed_d8 * 100

        gain_map[i, j] = gain

        counter += 1

        if counter % 50 == 0:

            print(
                f"Progress: {counter}/{total}"
            )

print()
print(
    "Max Gain:",
    np.max(gain_map)
)

print(
    "Min Gain:",
    np.min(gain_map)
)

plt.figure(
    figsize=(10,7)
)

im = plt.imshow(

    gain_map,

    origin="lower",

    aspect="auto",

    extent=[

        phase_values[0],
        phase_values[-1],

        loss_values[0],
        loss_values[-1]

    ]

)

plt.colorbar(
    label="Gain over Fixed d=8 (%)"
)

plt.xlabel(
    "Phase Noise (rad)"
)

plt.ylabel(
    "Channel Loss (dB)"
)

plt.title(
    "Adaptive Gain over Fixed d=8"
)

try:

    contours = plt.contour(

        phase_values,
        loss_values,
        gain_map,

        levels=[5,10,15],

        linewidths=2
    )

    plt.clabel(
        contours,
        inline=True,
        fontsize=9
    )

except:
    pass

plt.tight_layout()

plt.savefig(

    "adaptive_gain_vs_d8_heatmap.png",

    dpi=300

)

plt.show()