# validation/bsm_vs_dimension.py

import matplotlib.pyplot as plt

from statistics.physical_q11 import PhysicalQ11

model = PhysicalQ11()

dims = [2,4,8,16]

bsm_2km = []
bsm_50km = []

for d in dims:

    r = model.estimate(

        dimension=d,

        loss_db=0.4,

        phase_offset_rad=0.05,

        timing_offset_ps=20,

        polarization_offset_deg=2,

        trials=5000
    )

    bsm_2km.append(
        r.bsm_probability
    )

for d in dims:

    r = model.estimate(

        dimension=d,

        loss_db=10.0,

        phase_offset_rad=0.15,

        timing_offset_ps=20,

        polarization_offset_deg=2,

        trials=5000
    )

    bsm_50km.append(
        r.bsm_probability
    )

plt.figure(figsize=(8,5))

plt.plot(
    dims,
    bsm_2km,
    marker="o",
    linewidth=2,
    label="2 km"
)

plt.plot(
    dims,
    bsm_50km,
    marker="s",
    linewidth=2,
    label="50 km"
)

plt.xticks(dims)

plt.xlabel("Dimension d")

plt.ylabel("BSM Success Probability")

plt.title(
    "BSM Success Probability vs Dimension"
)

plt.grid(True)

plt.legend()

plt.tight_layout()

plt.savefig(
    "bsm_vs_dimension.png",
    dpi=300
)

plt.show()