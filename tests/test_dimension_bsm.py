# tests/test_dimension_bsm.py

from statistics.physical_q11 import PhysicalQ11

model = PhysicalQ11()

for d in [2,4,8,16]:

    r = model.estimate(
        dimension=d,
        loss_db=5,
        phase_offset_rad=0.1,
        timing_offset_ps=20,
        polarization_offset_deg=2,
        trials=10000
    )

    print(
        d,
        r.bsm_probability
    )