from statistics.physical_q11 import (
    PhysicalQ11
)

model = PhysicalQ11()

for loss in [

    0,
    5,
    10,
    15,
    20,
    25,
    30

]:

    result = model.estimate(

        dimension=8,

        loss_db=loss,

        phase_offset_rad=0.1,

        timing_offset_ps=20,

        polarization_offset_deg=2,

        trials=5000

    )

    print()

    print(
        f"Loss={loss} dB"
    )

    print(
        f"Q11={result.q11:.6e}"
    )