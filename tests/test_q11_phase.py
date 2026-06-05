from statistics.physical_q11 import (
    PhysicalQ11
)

model = PhysicalQ11()

for phase in [

    0.00,
    0.05,
    0.10,
    0.15,
    0.20,
    0.25,
    0.30

]:

    result = model.estimate(

        dimension=8,

        loss_db=5,

        phase_offset_rad=phase,

        timing_offset_ps=20,

        polarization_offset_deg=2,

        trials=5000

    )

    print()

    print(
        f"Phase={phase}"
    )

    print(
        f"BSM={result.bsm_probability:.6f}"
    )

    print(
        f"Q11={result.q11:.6e}"
    )