from statistics.physical_q11 import (
    PhysicalQ11
)

model = PhysicalQ11()

for d in [

    2,
    4,
    8,
    16

]:

    result = model.estimate(

        dimension=d,

        loss_db=5,

        phase_offset_rad=0.1,

        timing_offset_ps=20,

        polarization_offset_deg=2,

        trials=5000

    )

    print()
    print("d =", d)

    print(
        "Single Photon:",
        result.single_photon_probability
    )

    print(
        "BSM:",
        result.bsm_probability
    )

    print(
        "Q11:",
        result.q11
    )