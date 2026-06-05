from source.laser import CWLaser

from synchronization.optical_delay_line import (
    OpticalDelayLine
)

laser = CWLaser()

odl = OpticalDelayLine()

field = laser.generate_field(
    duration_s=1e-6,
    sampling_rate_hz=20e9
)

delayed = odl.apply_delay(
    field,
    delay_ps=250
)

corrected, metrics = (
    odl.auto_align(
        field,
        delayed
    )
)

print()
print(metrics)